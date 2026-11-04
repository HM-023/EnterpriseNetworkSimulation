"""Deterministic VLSM planning and illustrative Cisco-style configuration export."""
import ipaddress
import json
import math
import re
import uuid
from webapp.runtime import Store, integer, now, text, serve

EXAMPLE={'name':'Three-site reference network','pool':'10.40.0.0/16','segments':[
 {'site':'HQ','name':'Operations','vlan':10,'hosts':180},
 {'site':'HQ','name':'Finance','vlan':20,'hosts':75},
 {'site':'HQ','name':'IT','vlan':30,'hosts':40},
 {'site':'HQ','name':'Guest','vlan':88,'hosts':100},
 {'site':'Branch-B','name':'Users','vlan':10,'hosts':90},
 {'site':'Branch-C','name':'Users','vlan':10,'hosts':50}]}

def safe_name(value,name):
    value=text(value,name,32)
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',value):
        raise ValueError(f'{name} must start with a letter and contain only letters, digits, _ or -')
    return value

def allocate(plan):
    if not isinstance(plan,dict):raise ValueError('Expected an object')
    name=text(plan.get('name'),'Plan name',100)
    try: pool=ipaddress.ip_network(plan.get('pool',''),strict=True)
    except ValueError: raise ValueError('Use a canonical IPv4 pool, for example 10.40.0.0/16') from None
    private=[ipaddress.ip_network(n) for n in ['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16']]
    if pool.version!=4 or not any(pool.subnet_of(p) for p in private):
        raise ValueError('Pool must be contained in RFC1918 private IPv4 space')
    segments=plan.get('segments')
    if not isinstance(segments,list) or not 1<=len(segments)<=100: raise ValueError('Provide 1 to 100 segments')
    normalized=[];seen=set();names=set()
    for item in segments:
        if not isinstance(item,dict): raise ValueError('Each segment must be an object')
        site=safe_name(item.get('site'),'Site');label=safe_name(item.get('name'),'Segment')
        vlan=integer(item.get('vlan'),'VLAN',2,4094);hosts=integer(item.get('hosts'),'Required endpoint hosts',1,65533)
        if (site.casefold(),vlan) in seen: raise ValueError('VLAN IDs must be unique within each site')
        if (site.casefold(),label.casefold()) in names: raise ValueError('Segment names must be unique within a site')
        seen.add((site.casefold(),vlan));names.add((site.casefold(),label.casefold()))
        # Reserve network, broadcast and one gateway in addition to requested endpoints.
        prefix=32-max(2,math.ceil(math.log2(hosts+3)))
        normalized.append({'site':site,'name':label,'vlan':vlan,'hosts':hosts,'prefix':prefix})
    cursor=int(pool.network_address);limit=int(pool.broadcast_address);result=[]
    for item in sorted(normalized,key=lambda s:(s['prefix'],s['site'].casefold(),s['vlan'])):
        size=2**(32-item['prefix']);cursor=((cursor+size-1)//size)*size
        if cursor+size-1>limit: raise ValueError('Address pool is too small for the requested endpoints and gateways')
        subnet=ipaddress.ip_network((cursor,item['prefix']))
        result.append({**item,'network':str(subnet),'mask':str(subnet.netmask),'gateway':str(subnet.network_address+1),
          'dhcp_start':str(subnet.network_address+2),'dhcp_end':str(subnet.broadcast_address-1),
          'usable_endpoints':subnet.num_addresses-3,'allocated_addresses':size})
        cursor+=size
    consumed=sum(s['allocated_addresses'] for s in result)
    configs={}
    for site in sorted({s['site'] for s in result}):
        segments=[s for s in result if s['site']==site]
        lines=['! Generated design example. Review platform syntax before use.',f'hostname {site}',
               '! Assumes a layer-3 switch. WAN, ACL, DHCP and routing neighbors require separate design.','ip routing']
        for s in segments:
            lines.extend([f'vlan {s["vlan"]}',f' name {s["name"]}',f'interface Vlan{s["vlan"]}',
              f' description {s["name"]}',f' ip address {s["gateway"]} {s["mask"]}',' no shutdown'])
        lines.extend(['router ospf 10',' passive-interface default'])
        for s in segments:
            n=ipaddress.ip_network(s['network']);lines.append(f' network {n.network_address} {n.hostmask} area 0')
        lines.extend(['! Configure the actual transit interface and remove its passive setting after review.',
          '! Access/trunk interfaces and security policy are not generated.'])
        configs[site]='\n'.join(lines)+'\n'
    return {'id':str(uuid.uuid4()),'created':now(),'name':name,'pool':str(pool),'segments':result,'configs':configs,
      'allocated':consumed,'pool_addresses':pool.num_addresses,'utilization':round(100*consumed/pool.num_addresses,2),
      'endpoints':sum(s['hosts'] for s in result),'sites':len(configs),
      'warnings':['Allocations are illustrative. Simulator connectivity, failover and device syntax are not verified.',
                  'One gateway is reserved per segment; DHCP ranges exclude the gateway.'],
      'source':{'name':name,'pool':str(pool),'segments':normalized}}

class Workspace:
    def __init__(self,directory):self.store=Store(directory)
    def state(self):return {'kind':'network','title':'Network Design Studio','subtitle':'Plan address space, inspect segmentation and export a reviewable configuration baseline.','category':'NETWORK ENGINEERING','example':EXAMPLE,'plans':self.store.all('plan')}
    def action(self,body):
        action=body.get('action')
        if action=='plan':return self.store.save('plan',allocate(body.get('plan',{})))
        if action=='delete':self.store.delete('plan',body.get('id'));return {'ok':True}
        raise ValueError('Unknown action')

if __name__=='__main__':serve(Workspace,8102)

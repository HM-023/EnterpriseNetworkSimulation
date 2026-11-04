import copy
import ipaddress
import tempfile
import unittest
from webapp.app import allocate,EXAMPLE,Workspace

class PlanningTests(unittest.TestCase):
    def test_allocations_are_disjoint_and_reserve_gateway(self):
        p=allocate(EXAMPLE);nets=[ipaddress.ip_network(s['network']) for s in p['segments']]
        for i,n in enumerate(nets):
            self.assertTrue(n.subnet_of(ipaddress.ip_network(EXAMPLE['pool'])))
            for other in nets[i+1:]:self.assertFalse(n.overlaps(other))
        for s in p['segments']:
            self.assertGreaterEqual(s['usable_endpoints'],s['hosts'])
            self.assertEqual(int(ipaddress.ip_address(s['dhcp_start'])),int(ipaddress.ip_address(s['gateway']))+1)
    def test_gateway_reservation_changes_exact_power_of_two_case(self):
        p=allocate({'name':'Small','pool':'10.1.0.0/24','segments':[{'site':'HQ','name':'Users','vlan':10,'hosts':6}]})
        self.assertEqual(p['segments'][0]['network'],'10.1.0.0/28')
    def test_rejects_overflow_duplicate_vlan_and_public_pool(self):
        p=copy.deepcopy(EXAMPLE);p['pool']='10.1.0.0/30'
        with self.assertRaises(ValueError):allocate(p)
        p=copy.deepcopy(EXAMPLE);p['segments'][1]['vlan']=10
        with self.assertRaises(ValueError):allocate(p)
        p=copy.deepcopy(EXAMPLE);p['pool']='8.8.8.0/24'
        with self.assertRaises(ValueError):allocate(p)
    def test_configuration_identifiers_cannot_inject_commands(self):
        p=copy.deepcopy(EXAMPLE);p['segments'][0]['site']='HQ\nusername bad'
        with self.assertRaises(ValueError):allocate(p)
    def test_plan_survives_restart_and_rebuild(self):
        with tempfile.TemporaryDirectory() as d:
            p=Workspace(d).action({'action':'plan','plan':EXAMPLE})
            self.assertEqual(Workspace(d).state()['plans'][0]['id'],p['id'])
            rebuilt=allocate(p['source']);self.assertEqual(rebuilt['segments'],p['segments'])

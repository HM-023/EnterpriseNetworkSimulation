# Manual verification plan for Cisco Packet Tracer

This is a **proposed** test plan; results have not been independently observed. Record observed outputs/screenshots separately after inspecting an anonymized `.pkt` file.

| Test | Example command/action | Expected behavior |
|---|---|---|
| Interface state | `show ip interface brief` | Intended interfaces are up/up |
| VLAN mapping | `show vlan brief` | Endpoints in intended VLANs |
| Trunks | `show interfaces trunk` | Only authorized VLANs trunked |
| Routing | `show ip route` | Branch routes learned correctly |
| OSPF | `show ip ospf neighbor` | Planned adjacencies reach FULL |
| ACL boundaries | Ping or service requests between VLANs | Allowed flows pass, restricted flows drop |
| NAT | `show ip nat translations` | Translations appear for expected traffic |
| Redundancy | `show standby brief`, simulate primary failure | Standby gateway assumes responsibility |
| EtherChannel | `show etherchannel summary` | Expected member links bundled |
| Wireless | Associate test client and verify address | Correct VLAN, scoped access |

Do not treat sample lab documentation or unverified screenshots as formal acceptance evidence.

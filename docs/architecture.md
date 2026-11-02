# Architecture and design boundaries

| Layer | Design | Validation needed |
|---|---|---|
| Sites | HQ and two branches over routed WAN connections | Packet Tracer topology |
| Segmentation | Department VLANs, isolated wireless and server segments | `show vlan brief`, ACL tests |
| Routing | OSPF between site routers; inter-VLAN L3 gateways | OSPF neighbors and route tables |
| Exposure control | Edge ACLs, NAT/PAT, logical DMZ | Positive and negative traffic tests |
| Resilience | HSRP, RSTP/STP, EtherChannel where supported | Link/gateway failover timing |
| Operations | Device naming, backup configs, audit/change log | Exported device configs and backups |

## Threat model

The design attempts to reduce lateral movement across user departments and minimize exposure of internal services. VLAN membership alone is not a security boundary; inter-VLAN policy must be enforced at routing/firewall points. Guest Wi-Fi should use dedicated access and not share trusted internal network segments.

## Improvements before deploying a real network

Use version-controlled templates without secrets, AAA with named accounts, managed configuration backups, central logs, network monitoring, updated software versions, and documented restore procedures. Avoid WEP, legacy WPA, and hidden SSID as a security control. Prefer WPA2-Enterprise/WPA3-Enterprise where supported.

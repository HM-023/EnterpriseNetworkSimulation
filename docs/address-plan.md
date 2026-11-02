# Illustrative address plan

These are **new fictional example allocations**, not an export of historic configurations. Use subnet/VLAN numbers that match the real topology when rebuilding the simulation.

| Site | Function | VLAN | Network | Gateway example |
|---|---|---:|---|---|
| A | Operations | 10 | 10.10.10.0/24 | 10.10.10.1 |
| A | Finance | 20 | 10.10.20.0/25 | 10.10.20.1 |
| A | IT | 30 | 10.10.30.0/26 | 10.10.30.1 |
| A | Wireless | 88 | 10.10.88.0/27 | 10.10.88.1 |
| A | Services | 90 | 10.10.90.0/27 | 10.10.90.1 |
| B | Users | 10 | 10.20.10.0/24 | 10.20.10.1 |
| C | Users | 10 | 10.30.10.0/24 | 10.30.10.1 |

Use 203.0.113.0/24, 198.51.100.0/24 and 192.0.2.0/24 **only** for public-facing explanatory examples (RFC 5737 TEST-NET). These documentation addresses are not routable production public IP space.

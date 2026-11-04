# Changelog

## 1.0.0 — Local workspace release (2026-11-04)

- VLSM planning: Allocate subnets from an RFC1918 pool using requested endpoint counts.
- Boundary checks: Reject duplicate per-site VLAN IDs, unsafe device identifiers and exhausted address pools.
- Gateway-aware ranges: Reserve network, broadcast and gateway addresses before calculating endpoint capacity.
- Configuration baseline: Generate reviewable Cisco-style L3 VLAN and passive OSPF configuration text by site.
- Design snapshots: Save designs locally and reopen the exact specification.
- Exports: Download a complete JSON allocation or combined configuration text.
- Added a responsive local dashboard, request-boundary validation, ignored local state, regression tests and browser workflow verification.
- Preserved the prior case-study material and its contribution/reuse limitations.

Remaining scope: This is a design planner. Generated configuration text is illustrative and is never sent to devices. The original Packet Tracer file is not distributed, and simulator execution, live connectivity, failover and platform syntax remain unverified.

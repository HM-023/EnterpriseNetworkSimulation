# Enterprise Network Simulation: workspace guide

## Start and stop

Use `python -m webapp.app` from the repository root and open the printed loopback address. Python 3.11 or later is the supported baseline. Use the virtual environment activation command for your operating system. The default port is 8102; `--port` changes it. `Ctrl+C` shuts down the server.

## Main workflow

1. Open the reference JSON specification in **Design builder**. Each segment has a site, segment name, VLAN ID and required endpoint-host count. Endpoint counts exclude the gateway.
2. Choose a canonical RFC1918 IPv4 pool. Provide 1–100 segments, host counts from 1–65,533 and VLAN IDs from 2–4094. VLAN IDs and segment names must be unique within a site. Site and segment names use ASCII letters, digits, underscores and hyphens and start with a letter.
3. Build the plan. Larger subnets are allocated first. The planner reserves network, broadcast and one gateway address and rejects pool exhaustion rather than generating an overlapping plan.
4. Inspect site allocation totals, masks, gateways, endpoint ranges and capacity. The displayed endpoint ranges are proposed DHCP ranges; no DHCP service is installed.
5. Export JSON or Cisco-style configuration text. Review commands against the actual target platform in a permitted lab. The output assumes a layer-3 switch and leaves transit interfaces, routing neighbors, ACLs, DHCP services and redundancy to a separate implementation.
6. Open a saved design to reuse its original inputs. Building again creates another snapshot. No packets are sent and no device configuration is changed.

## Local data and backups

Records live in `data/workspace.sqlite3` by default. ML model artifacts additionally live in `data/models/`. These paths are excluded from git. The file formats contain local workspace information and are not encrypted by the application. Stop the server before copying the entire data directory for a simple backup, then use `--data-dir` to reopen that copy. Deleting the data directory while the server is stopped resets the workspace. Exported files are saved wherever the browser downloads them; this app does not automatically publish them.

## Local browser boundary

Use the exact printed localhost/127.0.0.1 URL and reload after restarting the server. A new random session token is issued each time. There is no remote bind option. Host checks resist DNS rebinding, and API requests require the page's token. This is a browser-request boundary, not account authentication and not a defense against other software already running as the same operating-system user.

## Browser verification

GitHub Actions runs the end-to-end journey in `tests/browser.cjs` using pinned Playwright 1.56.1. It exercises real forms and local API actions, checks browser errors and mobile viewport fit, reloads persisted state and captures desktop/mobile PNGs. Screenshots use only synthetic or fictional inputs.

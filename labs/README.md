# Labs

Labs turn the notes into evidence: each one pairs a capture or topology with
a short written analysis. A lab is not finished until somebody else could
reproduce it from its README alone.

## Wireshark series

| Lab | Proves | Notes section | Status |
| --- | ------ | ------------- | ------ |
| DNS resolution | how a name becomes an IP address | §3 | Planned |
| DHCP DORA handshake | the four packets that configure a device | §4, §12 | Planned |
| TCP three-way handshake | how a connection is established | §5 | Planned |
| ARP in action | IP ↔ MAC resolution on the LAN | §2, §7 | Planned |
| HTTP vs HTTPS | what encryption actually hides | §7 (Layer 6) | Planned |

## Packet Tracer series

| Lab | Skill | Notes section | Status |
| --- | ----- | ------------- | ------ |
| First topology + ping | addressing and reachability | §1, §6 | Planned |
| VLANs and a switch | segmenting a LAN | §7 (Layer 2) | Planned |
| Inter-VLAN routing (router-on-a-stick) | routing between VLANs | §7 (Layer 3) | Planned |
| OSPF between routers | dynamic routing | §7 (Layer 3) | Planned |
| NAT overload + port forwarding | exactly what §10 and §15 describe | §10, §15 | Planned |
| ACLs | filtering traffic | §14 | Planned |

## Conventions

- One folder per lab (`labs/wireshark/dns-resolution/`) with its own README:
  objective → steps → observations → what I learned.
- Keep packet captures under ~5 MB before committing; prefer screenshots
  plus the written analysis.
- Capture only on a network I own or control — my own laptop and router,
  or a lab built for the purpose.

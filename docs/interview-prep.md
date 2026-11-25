# Interview Prep — Networking Fundamentals

Every answer is drawn from my own
[networking notes](../networking_basics/README.md); the bracketed § tells me
where to revise. Questions marked *(beyond the notes)* are the next
additions to make to the notes themselves.

Rehearsal method: read the question, answer out loud, then check. Repeat
until no notes are needed.

## Addressing & subnetting

### Q1. What is an IP address?

A logical address used to identify a device on a network. IPv4 addresses
are 32 bits written as four decimal numbers separated by periods (for
example `192.168.100.107`); IPv6 uses 128 bits written in hexadecimal (for
example `2001:db8::1`). [§1]

### Q2. What does a subnet mask do?

It splits an IPv4 address into a network part and a host part. The device
uses it to decide whether a destination is local (same subnet) or remote
(send it to the default gateway). [§1]

### Q3. Given `192.168.100.107/24`, what are the network, broadcast and usable hosts?

/24 means mask `255.255.255.0`. Network: `192.168.100.0`; broadcast:
`192.168.100.255`; usable hosts `.1` through `.254` = 254 hosts. [§1]
(My [subnet calculator](../projects/subnet-calculator/README.md) computes
exactly this.)

### Q4. Which IPv4 ranges are private (RFC 1918)?

`10.0.0.0–10.255.255.255`, `172.16.0.0–172.31.255.255` and
`192.168.0.0–192.168.255.255`. [§11]

### Q5. Is `172.32.1.1` private?

No — RFC 1918's second range stops at `172.31.255.255`, so `172.32.x.x` is
public. Interviewers love this boundary. [§11]

### Q6. What are documentation address ranges, and why do they exist? *(beyond the notes)*

TEST-NET-1/2/3 (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) and
IPv6 `2001:db8::/32` are reserved for documentation and examples, so no
real address is ever exposed in published material.

### Q7. What is a MAC address?

A 48-bit link-layer address associated with a network interface (for
example `1A-2B-3C-4D-5E-6F`), used to deliver frames within the local
network segment. [§2]

### Q8. IP vs MAC — why do we need both?

IP handles logical, end-to-end addressing across networks; MAC handles
delivery between devices on the same segment. ARP maps an IP address to
the MAC address needed next. [§2, §7]

## DNS & DHCP

### Q9. What does DNS do?

Translates human-readable domain names (`google.com`) into the IP
addresses computers use to route traffic. [§3]

### Q10. Describe the DHCP DORA process

Discover (the client broadcasts to find a server) → Offer (the server
proposes configuration) → Request (the client asks to use it) →
Acknowledge (the server confirms: IP, subnet mask, default gateway, DNS
servers). [§4, §12]

### Q11. What is a DHCP lease?

The period a device may keep its assigned IP address. Renewals usually
return the same address; after expiry the server may assign it elsewhere. [§12]

## Transport

### Q12. TCP vs UDP?

TCP is connection-oriented, reliable and ordered, retransmitting lost
segments (web, file transfer, SSH). UDP is connectionless with no delivery
guarantee but lower overhead and latency (gaming, live audio/video, DNS
queries). [§5]

### Q13. What does the transport layer do?

End-to-end delivery: it segments large data, reassembles it at the
receiver, and provides reliable (TCP) or fast (UDP) transfer. [§7, Layer 4]

### Q14. Describe the TCP three-way handshake *(beyond the notes)*

SYN → SYN-ACK → ACK: client and server agree on initial sequence numbers
before any data flows.

### Q15. Why can DNS use UDP? *(beyond the notes)*

A single query and response fits in one packet, and skipping connection
setup is faster; TCP is used when responses are large (such as zone
transfers).

## OSI & TCP/IP models

### Q16. Name the seven OSI layers, bottom to top

Physical, Data Link, Network, Transport, Session, Presentation,
Application. Mnemonic: "Please Do Not Throw Sausage Pizza Away". [§7]

### Q17. At which layers do switches and routers operate?

Switches at Layer 2 (they forward frames by MAC address, learning source
MACs and flooding unknown destinations); routers at Layer 3 (they forward
packets by IP address using routing tables). [§7]

### Q18. What does a router do when forwarding between networks?

It removes the incoming Ethernet frame, reads the IP packet, chooses the
next hop from its routing table, and re-encapsulates the packet in a new
frame. Before that, the sending PC used its subnet mask to decide the
destination was remote and ARPed for the gateway's MAC. [§7, Layer 3]

### Q19. How do the OSI and TCP/IP models map onto each other?

TCP/IP Application = OSI Application + Presentation + Session; Transport
stays as is; Internet = OSI Network; Network Access = OSI Data Link +
Physical. The OSI model is the reference model; TCP/IP is what the
Internet actually uses. [§8]

## Ports

### Q20. What is a port?

A logical endpoint that identifies an application or service on a device;
the operating system reads the destination port and hands the data to the
right application. [§9]

### Q21. Which port numbers are worth memorizing? *(beyond the notes)*

22 SSH, 53 DNS, 80 HTTP, 443 HTTPS, 25 SMTP, 21 FTP. (Add a small ports
table to the notes.)

## NAT, firewalls & port forwarding

### Q22. How does NAT work, step by step?

The router replaces the private source IP with its public IP before
forwarding, records the mapping in a NAT table, and uses that table to
deliver replies to the correct internal device. [§10]

### Q23. Why does NAT matter for IPv4?

It conserves scarce public addresses: many devices share a single public
IP. [§10]

### Q24. Is NAT a firewall?

No. NAT drops unsolicited inbound packets as a side effect (they match no
NAT table entry), but it applies no security policy — that is a firewall's
job. [§13, §14]

### Q25. What is port forwarding?

A router rule that directs traffic arriving on a specific public port to a
specific internal `ip:port`, which is what makes hosted services (websites,
game servers, cameras) reachable from outside. [§15]

### Q26. Can two internal devices share the same public port?

Not on the same public IP — the destination would be ambiguous. The fix is
different external ports mapping to different internal devices (or
different internal ports). [§15]

## Tools

### Q27. Does `ping` use TCP or UDP?

Neither — it uses ICMP. Its output shows replies, packet loss, and the
minimum, average and maximum round-trip times. [§6]

### Q28. tracert vs traceroute?

Same purpose — showing the hop-by-hop path to a destination — different
operating systems: `tracert` on Windows, `traceroute` on Linux/macOS.
Useful for locating where delays or failures occur. [§6]

### Q29. Which quick commands reveal local network configuration?

Windows `ipconfig`, Linux `ip addr`; `nslookup` for DNS queries; `arp -a`
for the IP→MAC table; `netstat -an` for connections and listening ports. [§6]

### Q30. How do you check which addresses on a network are already used?

Ping sweeps and ARP inspection in a lab; in production, watch the DHCP
server's lease table — which is also why DHCP prevents duplicate IP
assignment. [§6, §12]

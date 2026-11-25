# Networking Basics

A practical introduction to fundamental computer networking concepts.

## Objective

Learn and document fundamental networking concepts through practical exercises and experiments.

## Topics

- IP addresses
- MAC addresses
- DNS
- DHCP
- TCP vs UDP
- Basic networking commands

## Contents

1. [IP Addresses](#1-ip-addresses)
2. [MAC Addresses](#2-mac-addresses)
3. [DNS](#3-dns)
4. [DHCP](#4-dhcp)
5. [TCP vs UDP](#5-tcp-vs-udp)
6. [Basic Networking Commands](#6-basic-networking-commands)
7. [OSI Model](#7-osi-model)
8. [TCP/IP Model](#8-tcpip-model)
9. [Ports](#9-ports)
10. [Network Address Translation (NAT)](#10-network-address-translation-nat)
11. [Private and Public IP Addresses](#11-private-and-public-ip-addresses)
12. [Dynamic Host Configuration Protocol (DHCP)](#12-dynamic-host-configuration-protocol-dhcp)
13. [NAT and Security](#13-nat-and-security)
14. [Firewalls](#14-firewalls)
15. [Port Forwarding](#15-port-forwarding)

## 1. IP Addresses

An IP address is a logical address used to identify a device on a network.

### IPv4

IPv4 addresses contain 32 bits and are commonly written as four decimal numbers separated by periods.

Example: `192.168.1.10`

### IPv6

IPv6 uses 128 bits and was introduced to provide a much larger address space than IPv4.

Example: `2001:db8::1`

### Subnet Mask

A subnet mask determines which part of an IPv4 address represents the network and which part represents the host.

For example:

- IP address: `192.168.100.107`
- Subnet mask: `255.255.255.0`
- Network: `192.168.100.0/24`
- Host: `107`

Devices such as `192.168.100.25` are on the same /24 network, while `192.168.101.25` is on a different network.

## 2. MAC Addresses

A MAC (Media Access Control) address is a link-layer address associated with a network interface.

Example: `1A-2B-3C-4D-5E-6F`

Unlike an IP address, which is used for logical addressing and routing, a MAC address is used for delivering frames within the local network segment.

## 3. DNS

DNS (Domain Name System) translates human-readable domain names into IP addresses that computers use to communicate.

For example: `google.com` → the IP address of a Google server.

DNS makes it easier for people to access Internet services without having to remember numerical IP addresses.

## 4. DHCP

DHCP (Dynamic Host Configuration Protocol) automatically provides network configuration to devices when they join a network.

It can assign:

- IP address
- Subnet mask
- Default gateway
- DNS server

This reduces the need to manually configure every device and helps prevent configuration errors.

### DHCP Process

The basic DHCP process is commonly summarized as DORA:

1. Discover
2. Offer
3. Request
4. Acknowledge

The DORA process is described in more detail in [section 12](#12-dynamic-host-configuration-protocol-dhcp).

## 5. TCP vs UDP

TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) are transport-layer protocols.

### TCP

TCP establishes a connection and provides reliable, ordered delivery of data. Lost data can be retransmitted.

Common uses:

- Web browsing
- File transfers
- SSH

### UDP

UDP sends data without establishing a connection and does not guarantee delivery or ordering. It has lower overhead and is useful when low latency is more important than perfect delivery.

Common uses:

- Online gaming
- Live audio/video
- DNS queries

### Key Difference

TCP prioritizes reliability, while UDP often prioritizes speed and low latency.

## 6. Basic Networking Commands

### ping

The `ping` command tests network reachability and measures round-trip time (RTT).

Example:

```bash
ping 8.8.8.8
```

The results show whether replies were received, packet loss, and the minimum, maximum, and average round-trip times.

Ping uses ICMP, not TCP or UDP.

### tracert / traceroute

The `tracert` (Windows) and `traceroute` (Linux/macOS) commands show the path that packets take from a computer to a destination.

Example:

```bash
tracert 8.8.8.8     # Windows
traceroute 8.8.8.8  # Linux / macOS
```

Each numbered line represents a hop (a router or network device that forwards the packet).

Traceroute is useful for:

- Identifying where delays occur.
- Seeing the path packets take across networks.
- Troubleshooting connectivity issues.

### ipconfig / ip addr

Displays the local IP configuration, such as the IP address, subnet mask, and default gateway.

```bash
ipconfig  # Windows
ip addr   # Linux
```

### nslookup

Queries DNS to find the IP address associated with a domain name.

```bash
nslookup google.com
```

### arp

Displays the ARP table, which maps IP addresses to MAC addresses on the local network.

```bash
arp -a
```

### netstat

Displays active network connections and listening ports.

```bash
netstat -an
```

## 7. OSI Model

The OSI (Open Systems Interconnection) model describes how network communication is organized into seven layers.

### Layer 1 (Physical Layer)

Responsible for transmitting raw bits (0s and 1s) and defining how data travels through the physical medium.

Examples:

- Ethernet cables
- Fibre optic cables
- Wi-Fi radio signals
- Network Interface Card (NIC)
- Hubs

#### Key Points

- No MAC addresses or IP addresses are used at this layer.
- If the physical connection fails (e.g., an unplugged cable), communication cannot occur.
- The NIC converts digital data into electrical, optical, or radio signals and vice versa.

### Layer 2 (Data Link Layer)

Provides communication between devices on the same local network (LAN). Uses MAC addresses to identify devices.

Examples:

- Ethernet
- Switches
- ARP
- MAC addresses

#### Key Points

- Data is transmitted as Ethernet frames.
- Switches learn MAC addresses by observing the source MAC address of incoming frames.
- If the destination MAC address is unknown, the switch floods the frame to all ports except the incoming port.
- Switches forward frames based on MAC addresses.
- MAC table entries are automatically removed after a period of inactivity (MAC aging).

### Layer 3 (Network Layer)

The network layer is responsible for delivering packets between different networks. It uses IP addresses to identify devices and to choose the best path to the destination.

Functions:

- Uses IP addresses to identify devices on different networks.
- Determines whether the destination is on the local network or a remote network.
- Chooses the best path for packets to travel.
- Forwards packets between different networks.
- Uses routing tables to determine the next hop.

#### Key Points

- Routers operate at Layer 3 because they make forwarding decisions using IP addresses.
- Your PC is the first device to determine whether the destination is local or remote by comparing the destination IP with its subnet mask.
- If the destination is on another network, your PC sends the frame to the default gateway.
- Before sending the frame, ARP is used (if necessary) to obtain the MAC address of the default gateway.
- The router removes the Ethernet frame, reads the IP packet, and forwards it to the next network.

### Layer 4 (Transport Layer)

Responsible for end-to-end communication between devices. It ensures that data is delivered reliably when required and divides large amounts of data into smaller segments for transmission.

Protocols:

- TCP
- UDP

Functions:

- Segments large data into small pieces.
- Reassembles data at the receiving device.
- Provides reliable or fast data transmission.
- Detects lost segments and retransmits them (TCP).
- Ensures data arrives in the correct order (TCP).

#### TCP

Characteristics:

- Connection-oriented.
- Reliable.
- Acknowledges received data.
- Retransmits lost segments.
- Ensures data arrives in order.

Examples:

- File downloads
- Web browsing (HTTP/HTTPS)
- Email
- Messaging applications

#### UDP

Characteristics:

- Connectionless.
- Faster than TCP.
- Does not retransmit lost data.
- No guarantee of delivery or order.

Examples:

- Live video streaming
- Voice calls
- Online gaming
- Video conferencing

#### Key Points

- TCP prioritizes reliability over speed.
- UDP prioritizes speed over reliability.
- Large files are divided into smaller segments before transmission.
- TCP retransmits only the missing segments instead of restarting the entire transfer.

### Layer 5 (Session Layer)

The session layer is responsible for establishing, managing, and terminating communication sessions between applications.

Functions:

- Establishes communication sessions.
- Maintains active communication between devices.
- Terminates communication between applications.
- Helps recover interrupted sessions when possible.

Examples:

- Video conferencing (Zoom, Microsoft Teams)
- Remote desktop sessions
- Database connections

#### Key Points

- Responsible for the beginning, maintenance, and end of a communication session.
- Keeps communication organized between two applications.
- Manages long-running communication such as video calls or large file transfers.

### Layer 6 (Presentation Layer)

Responsible for formatting, translating, encrypting, decrypting, compressing, and decompressing data so that it can be correctly understood by the receiving device.

Functions:

- Encrypts data before transmission.
- Decrypts received data.
- Compresses data to reduce its size.
- Decompresses received data.
- Translates data into a format understood by the receiving application.

Examples:

- SSL/TLS encryption
- HTTPS encryption
- JPEG image compression
- MP3 audio compression
- MPEG video compression

### Layer 7 (Application Layer)

The closest layer to the user; it provides network services that allow applications to communicate over a network.

Protocols:

- HTTP (HyperText Transfer Protocol)
- HTTPS (HTTP Secure)
- DNS (Domain Name System)
- DHCP (Dynamic Host Configuration Protocol)
- FTP (File Transfer Protocol)
- SMTP (Simple Mail Transfer Protocol)

Functions:

- Provides network services to applications.
- Allows users to access network resources.
- Handles communication between software applications.
- Provides services such as web browsing, email, file transfer, and name resolution.

Examples:

- Opening a website using HTTPS.
- Sending an email using SMTP.
- Resolving a domain name using DNS.
- Automatically receiving an IP address using DHCP.

#### Key Points

- The application layer does not move packets or choose routes.
- It provides services that applications use to communicate.
- Protocols like DNS, HTTP, and DHCP operate at this layer.
- Lower layers handle the actual transmission of data.

## 8. TCP/IP Model

The TCP/IP model is the networking model used on the Internet. It groups networking functions into four layers.

Layers:

1. Application
2. Transport
3. Internet
4. Network Access

### Layer Responsibilities

#### Application Layer

Provides networking services to applications. Combines the OSI Application, Presentation, and Session layers.

Examples:

- HTTP
- HTTPS
- DNS
- DHCP
- FTP
- SMTP

#### Transport Layer

Provides end-to-end communication. Segments and reassembles data. Ensures reliable or fast transmission.

Protocols:

- TCP
- UDP

#### Internet Layer

Uses IP addresses. Routes packets between different networks. Determines the best path for packets.

Protocols:

- IP
- ICMP

#### Network Access Layer

Handles communication on the local network. Uses MAC addresses. Transmits bits through the physical medium.

Examples:

- Ethernet
- Wi-Fi
- Switches
- NICs

### Key Points

- The TCP/IP model has 4 layers.
- It is the model used by the Internet.
- The OSI model has 7 layers and is mainly used as a reference model.
- The TCP/IP Application layer combines the OSI Application, Presentation, and Session layers.
- The TCP/IP Network Access layer combines the OSI Data Link and Physical layers.

## 9. Ports

Ports are logical communication endpoints that allow multiple applications on the same device to communicate over a network simultaneously.

### Functions

- Identify the destination application on a device.
- Allow multiple network applications to run at the same time.
- Work together with IP addresses to deliver data to the correct application.

### Key Points

- An IP address identifies a device running on the network.
- A port number identifies an application or service running on that device.
- The operating system reads the destination port and delivers the data to the correct application.
- Switches use MAC addresses.
- Routers use IP addresses.
- Operating systems use port numbers.

## 10. Network Address Translation (NAT)

Network Address Translation (NAT) is the process by which a router translates private IP addresses into public IP addresses when accessing the Internet.

### Functions

- Translates private IP addresses into public IP addresses.
- Allows multiple devices to share one public IP address.
- Conserves public IPv4 addresses.
- Maintains a NAT table to keep track of active connections.
- Translates incoming packets back to the correct private device.

### Key Points

- Devices inside a local network use private IP addresses.
- The Internet only sees the router's public IP address.
- The router replaces the private source IP with its public IP before sending the packets to the Internet.
- The router uses a NAT table to determine which internal device should receive returning packets.
- NAT helps conserve the limited number of available IPv4 public addresses.

### Example

A laptop with the private IP address `192.168.100.107` sends a request to Google.

```text
Before NAT:
  Source IP: 192.168.100.107

After NAT:
  Source IP: 203.0.113.50
```

Google responds to the router's public IP address, and the router uses its NAT table to forward the response to the correct device on the local network.

(The public IP used here, `203.0.113.50`, comes from a range reserved for documentation examples, so no real address is shown.)

## 11. Private and Public IP Addresses

IP addresses are divided into private and public addresses based on where they are used.

### Private IP Addresses

Private IP addresses are used inside local networks and are not routable on the Internet.

Private IPv4 ranges:

- `10.0.0.0` – `10.255.255.255`
- `172.16.0.0` – `172.31.255.255`
- `192.168.0.0` – `192.168.255.255`

### Public IP Addresses

Public IP addresses are globally unique and are assigned by Internet Service Providers (ISPs). They allow communication over the Internet.

### Key Differences

| Private IP | Public IP |
| ---------- | --------- |
| Used inside local networks | Used on the Internet |
| Cannot be reached directly from the Internet | Can be reached over the Internet |
| Reused by many different networks | Globally unique |
| Works together with NAT | Assigned by an ISP |

### Key Points

- Devices inside a LAN use private IP addresses.
- Routers use NAT to translate private IP addresses into a public IP address.
- Multiple devices can share one public IP address through NAT.

## 12. Dynamic Host Configuration Protocol (DHCP)

Dynamic Host Configuration Protocol (DHCP) is a network protocol that automatically assigns network configuration information to devices joining a network.

### Functions

- Assigns IP addresses automatically.
- Assigns subnet masks.
- Provides the default gateway address.
- Provides DNS server addresses.
- Prevents IP address conflicts.

### Key Points

- A DHCP server automatically configures devices on a network.
- In most home networks, the router acts as the DHCP server.
- Devices request an IP address when they connect to the network.
- DHCP reduces manual configuration and minimizes configuration errors.

### Information Provided by DHCP

- IP address
- Subnet mask
- Default gateway
- DNS server address

### Benefits

- Automatic network configuration.
- Prevents duplicate IP addresses.
- Simplifies network administration.
- Allows devices to join the network quickly.

### DHCP DORA Process

The DHCP process follows four steps, commonly remembered as DORA.

#### 1. Discover

The client broadcasts a DHCP Discover message to locate a DHCP server.

#### 2. Offer

The DHCP server offers an available IP address and other network configuration information.

#### 3. Request

The client requests to use the offered IP address.

#### 4. Acknowledge

The DHCP server confirms the assignment and provides:

- IP address
- Subnet mask
- Default gateway
- DNS server

### DHCP Lease

A DHCP lease is the amount of time a device is allowed to use an assigned IP address.

#### Key Points

- DHCP assigns IP addresses for a limited period called a lease.
- A device usually keeps getting the same IP address while the lease is valid.
- When reconnecting to the same network before the lease expires, the device will usually receive the same IP address.
- After the lease expires, the DHCP server may assign the IP address to another device.

## 13. NAT and Security

NAT only forwards incoming packets if they match an existing entry in the NAT table. Packets that do not match any entry in the NAT table are dropped. This prevents most unsolicited connections from reaching devices on the local network.

NAT provides a basic level of protection, but it is not a replacement for a [firewall](#14-firewalls). A firewall applies security rules to determine whether traffic should be allowed or blocked.

## 14. Firewalls

A firewall is a security system that monitors and controls incoming and outgoing network traffic according to predefined rules.

### Functions

- Allows legitimate traffic.
- Blocks unauthorized traffic.
- Protects devices from unsolicited connections.
- Works together with NAT to improve network security.

### Key Points

- Knowing a router's public IP address does not automatically allow access to devices inside the network.
- NAT forwards only traffic that matches an existing NAT table entry.
- A firewall applies rules to determine whether traffic should be allowed or blocked.
- Outbound connections initiated by devices inside the network are generally allowed, and their replies are permitted.
- Unsolicited inbound connections are typically blocked unless explicitly allowed (for example, through port forwarding or firewall rules).

## 15. Port Forwarding

Port forwarding is a router feature that directs incoming traffic on a specific port to a specific device on the local network.

### Functions

- Allows external devices to access services hosted inside a private network.
- Works together with NAT to direct incoming traffic.
- Enables hosting of websites, game servers, security cameras, and other network services.

### Key Points

- Without port forwarding, unsolicited incoming traffic is usually dropped.
- A port forwarding rule tells the router which private IP address should receive traffic arriving on a specific port.
- After the internal device responds, NAT tracks the ongoing connection.

### Example

| Public Port | Forward To |
| ----------- | ---------- |
| 80 (HTTP) | `192.168.100.107:80` |
| 443 (HTTPS) | `192.168.100.107:443` |
| 25565 (Minecraft) | `192.168.100.107:25565` |

### Port Forwarding with Multiple Devices

A router cannot normally forward the same public IP and public port combination to two different internal devices, because the destination would be ambiguous. Different external ports can be used to reach different internal devices.

#### Example

```text
Public Port 80
      ↓
192.168.100.107:80

Public Port 8080
      ↓
192.168.100.120:80
```

### External and Internal Ports

A port forwarding rule can map an external/public port to a different internal port.

```text
Public IP:8080
      ↓
    Router
      ↓
192.168.100.120:80
```

The external port identifies the incoming connection, while the internal port identifies the service on the destination device.

### Port Forwarding and Unsolicited Traffic

Without a port-forwarding rule, an unsolicited incoming connection normally has no internal destination. For example:

```text
Public:2222
      ↓
    Router
      ↓
❌ No forwarding rule
      ↓
Packet dropped
```

A configured rule provides the destination:

```text
Public:2222
      ↓
192.168.100.120:22
```

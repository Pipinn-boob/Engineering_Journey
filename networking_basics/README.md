# Networking Basics
A practical introduction to fundamental computer networking concepts.
## Objective
Learn and document fundamental networking concepts through practical exercises and experiments.
## Topics 
- IP addresses 
- MAC addreddes
- DNS
- DCHP
- TCP vs UDP
- Basic networking commands.
## 1. IP Addresses
An IP address is a logical address used to identify a device on a network.
### IPv4
IPv4 addresses contains 32 bits and are commonly written as four decimal numbers separated by periods.
Example:
'192.168.1.10'
### IPv6
IPv6 uses 128 bits and was introduced to provide a much larger address space than IPv4.
Example:
'2001:db8::1'
### Subnet Mask
A subnet mask determines which part of an IPv4 address represents the network and which part represents the host.
For example: 
- IP address: '192.168.100.107
- Subnet mask: '255.255.255.0'
- Network: '192.168.100.0/24'
- Host: '107'
Devices such as '192.168.100.25' are om the same /24 network while '192.168.101.25' is om a different network.
## 2. MAC Addresses
A MAC (Media Access Control) address is a link-layer address associated with a network interface.
Example: 
'1A-2B-3C-4D-5E'
Unlike an IP address, which is used for logical addressing and routing, a MAC address is used for delivering frames within  the local network segment.
## 3. DNS
DNS (Domain Name System) translates human-readable domain names into IP addresses that computers use to communicate.
For example:
'google.com' ~ IP address 
DNS makes it easier for people to access Internet services without having to remember numerical IP addresses.
## 4. DHCP
DCHP (Dynamic Host Configuration Portocol) automatically provides network configuration to devices when they join a network.
It can assign:
- IP address
- Subnet mask
- Default gateway
- DNS server
This reduces the need to manually configure every device and helps prevent configuration errors.
### DHCP Process
The basic DCHP process is commonly summarizes as DORA:
1. Discover
2. Offer
3. Request 
4. Acknowledge
## 5. TCP vs UDP
TCP (Transmission Control Protocol) and UDP(User Datagram Protocol) are transport-layer protocols.
### TCP
TCP establishes a connection and provides reliable, ordered delivery of data. Lost data can retransmitted.
Common uses:
- Web browsing
- File transfers
- SSH
### UDP
UDP sends data without establishing a connection and soes not guarantee delivery or ordering. It has lower overhead and is useful low latency is more important than perfect delivery. 
Common uses: 
- Online gaming
- Live audio/video
- DNS queries
### Key Difference
TCP prioritizes reliability, while UDP often prioritizes speed and low latency. 
### Ping
The 'Ping' command can be used to test network reachability and measure round-trip time(RTT).
Example:
'Ping 8.8.8.8'
The results show whether packets replies, packet loss, and the minimum, maximum, and average round-trip times.
Ping uses ICMP, not TCP or UDP.
## 6.Traceout(tracert)
The 'tracert' command shows the path that packets take from a computer to a destination.
Example:
```bash
tracert 8.8.8.8
```
Each numbered line represents a hop (a router or network device that forwards the packet).
Traceroute is useful for:
- Identifying where delays occur.
- Seeing the path packets take across networks.
- Troubleshooting connectivity issues.
## 7. OSI Model
### OSI Model Layer 1(Physical Layer)
It is responsible for transmitting raw bits(0s and1s) and defines how data travels through physical medium.
Examples:
- Ethernet cables
- Fibre optic cables
- Wi-Fi radio signals
- Network Interface Card(NIC)
- Hubs
#### Key Points
No MAC address or IP addresses are used at this layer. 
If the physical connection fails(e.g., unplugged cable), communication can not occur.
The NIC converts digital data into electrical, optical or radio signals and vice versa.
### OSI Model- Layer 2(Data Link Layer)
It provides communication between devices on the same local network(LAN).
Uses MAC addresses to identify devices.
Examples:
- Ethernet
- Switch
- ARP
- MAC addresses
#### Key Points
Data is transmitted as Ethernet frames.
Switch learn MAC by observing the source MAC address of becoming of incoming frames.
If the destination MAC address is unknown, the switch the frame to all ports except the incoming port.
Switches forward frames based on MAC addresses.
MAC table entries are automatically removed after a period if inactivity(MAC aging).
### OSI Model- Layer 3(Network Layer)
The network layer is responsible for delivering packets between different networks. It uses IP addresses to identify devices the best path to the destination.
Example:
- Uses IP addresses yo identify devices on different network.
- Determined whether the detsination is on the local network or a remote network.
- Chooses the best path for packets to travel.
Forwards packets between different networks.
- Uses routomg tanles to determine the next hop.
#### Key Points
Routers iperate at Layer 3 because they make forwarding decisions using IP addresses.
Your PC is the first device to determine whether the destination is local or remote by comparing the destination IP with its subnet mask.
If the destinatiom is on another netwok, your PC sends the frame to the default gateway.
Before sending the framem ARP is used(if necessary) to obtain the MAC address of the default gateway.
The router removes the ethernet frame, reads the IP packet, and forwards it to the next network.
### OSI Model- Layer 4(Transport Layer)
It is responsible for end-to-end communication between devices. It ensures that data is delivered reliably when required and divides large amounts of data into smaller segments for transmission.
Protocols:
- TCP
- UDP
Functions:
- Segments large data into small pieces.
- Reassembles data at the receiving device.
- Provides reliable or fast data transmission.
- Detects lost segmenys and retransmits them(TCP)
- Ensures rata arrives in the correct order.(TCP)
#### TCP
Characteristics:
- Connection-oriented.
- Reliable.
- Acknowledges received data.
- Retransmits lost segments.
- Ensures data arrives in order.
Examples 
- File downloads
- Web browsing(HTTP/HTTPS)
- Emails
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
##### Key Points
TCP prioritizes reliability over speed.
UDP prioritizes speed over reliabilty.
Large files are divided into smaller segments before transmission.
TCP only retransmits the missing segments instead of restarting the entire transfer.
### OSI Model Layer 5(Session Layer)
The session layer is responsible for establishing, managing and terminating communication sessions between applications.
Functions:
- Establishes communication sessions.
- Maintains active communication betwen devices.
- Terminates communication between applications.
- Helps recover interrupted sessions when possible.
Examples:
- Video conferencing(Zoom, Microsoft Teams)
- Remote desktop sessions
- Database connections
#### Key Points
Responsible for the beginning, maintenance and end of a communcation session.
Keeps communication organized between two applications.
Manages long-running communcation such as video calls or large file transfers.
### OSI Model Layer 6(Presentation Layer)
It is responsible for formatting, translating, encrypting, decrypting, compressing and decompressing data so that it can be correctly understood by the receiving device.
Functions:
- Encrypts data before transmission.
- Decrpts received data.
- Compresses data to reduce its size.
- Decompresses received data.
- Translates data into a format understood by the receiving application.
Examples:
- SSL/TLS encryption
- HTTPS encryption
- JPEG image compression
- MP3 audio compression
- MPEG video compression
### OSI Model Layer 7(Application Layer)
It is the closest layer to the user and provides network services that allow applications to communicate over a network.
Protocols:
- HTTP(HyperText Transfer Protocol)
- HTTPS(HTTP Secure)
- DNS(Domain Name System)
- DHCP(Dynamic Host Configuration Protocol)
- FTP(File Transfer Protocol)
- SMTP(Simple Mail Transfer Protocol)
Functions:
- Provides network services to applications.
- Allows users to access network resources.
- Handles communication between software applications.
- Provides services such as web browsing, email, file transfer and name resolution.
Examples:
- Opening a website using HTTPS.
- Sending an email using SMTP.
-  Resolving a domain name using DNS.
- Automatically receiving an IP address using DHCP.
#### Key Points
The application layer does not move packets or choose routes.
It provides services that application use to communication. 
Protocols like DNS,HTTP,DHCP operate at this layer.
Lower layers handle the actual transmission of data.
## 8. TCP/IP
The TCP/IP is the networking model used on the internet. It groups networking functions into four layers.

Layers:
1. Appllication
2. Transport
3. Internet
4. Network Access
### Layer responsibilities
#### Application Layer
Provides networking services to applications.
Combines the OSI Application, Presentation, and Session layers.
Examples:
- HTTP
- HTTPS
- DNS
- DHCP
- FTP
- SMTP
#### Transport Layer
Provides end-to-end communication.
Segments and reassembles data.
Ensures reliable or fast transmission.
Protocols:
- TCP
- UDP
#### Internet Layer
Uses IP addresses.
Routes packets between different networks.
Determines the best path for packets.
Protocols:
- IP
- ICMP
#### Network Access Layer
Handles communication on the local network.
Uses MAC addresses.
Transmits bits through the physical medium.
Examples:
- Ethernet
- Wi-Fi
- Switches
- NICs
### Key Points
The TCP/IP model has 4 layers.
It is the model used by the internet. 
The OSI model has 7 layers and is mainly used as a reference model.
The TCP/IP Application layer combines the OSI Application, Presentation, and Session layers.
The TCP/IP Network Access Layer combine the OSI Data Link and Physical Layers.
## 9. Ports
Ports are logical communication endpints that allow multiple applictaions on the same device to communicate multiple applications on the same device over a network simoultaneously.
### Functions
- Identify the destination application on a device.
- Allow Multiple network appllications to run at the same time.
- Work together with IP addresses to deliver data to the correct appliication.
### Key Points
An IP address identifies a device running on the network.
A port number identifies an application or service running on that network.
The oprating system reads the destination port and delivers the data to the correct aaplication.
Switches use MAC addresses.
Routers use IP addresses.
Operating systems use port numbers.
## 10. Network Address Translation
Network Address Translation(NAT) is the process by which a router translates private IP addresses into a public IP addresses when accessing the internet. 
### Functions
- Translates private IP addresses into public IP addresses.
- Allows multiple devices to share one IP address.
Conserves public IPv4 addresses.
- Maintains a NAT table to keep track of active connections.
- Translates incoming packets back to the correct private device.
### Key Points
Devices inside a local network use private IP addresses.
The internet only ees the router's public IP address.
The router replaces the private source IP with its public IP before sending the packets to the internet.
The router uses a NAT table to determine which internal device should receive returning packets.
NAT helps conserbe the limited number of available IPv4 public addresses.
### Example
A laptop with the private IP addresses 192.168.100.107 sends a request to Google.
Before NAT:
Source IP:192.168.100.107
After NAT:
Source IP: 102.45.18.73Google responds to the router's public IP address, and the router uses its NAT table to forward the response to the correct device on the local network.
## 11. Private and Public IP Addresses
IP addresses are divided into private and public addresses based on where they are used.
### Private IP Addresses
Private IP addresses are used inside local networks and are not routable on the Internet.
Private IPv4 ranges:
- 10.0.0.0 - 10.255.255.255
- 172.16.0.0 - 172.31.255.255
192.168.0.0 - 192.168.255.255
### Public IP addresses
Public IP addresses are globally unique and are assigned by Internet Service Providers(ISPS)
They allow communication over the Internet.
### Key Differences
| Private IP | Public IP |
| -----------|-----------|
| Used inside local networks | Used on the Internet |
| Cannot be reached directly from the Internet | Can be reached over the Internet |
| Reused by many different networks | Globally unique |
| Works together with NAT | Assigned by an ISP |
### Key Points
- Devices inside a LAN use private IP addresses.
- Routers use NAT to translate private IP addresses into a public IP address.
- Multiple devices can share can share one public IP address through NAT.
## 12. Dynamic Host Configuration Protocol
Dynamic Hist Cofiguration Protocol (DHCP) is a network protocol that automatically assigns network configuration information to devices joining a network.
### Functions
- Assigns IP addresses automatically.
- Assigns subnet masks.
- Provides the default gateway address.
- Provides DNS server addresses.
- Prevents IP address conflicts.
#### Key Points
- A DHCP server automatically configure devices on a network.
- In most home networks, the router acts as the DHCP server.
- Devices request an IP address when they connect to the network.
- DHCP reduces manual configuration and minimizes configuration errors.
### Information Provided by DHCP
- IP address
- Subnet Mask
- Default Gateway
- DNS Server Address
#### Benefits
Automatic network configuration.
Prevents duplicate IP addresses.
Simplifies network network administration.
Allows devices to join the network quickly.
### DHCP DORA Process
The DHCP process follows four steps, commonly remembered as DORA.
#### 1. Discover
The client broadcasts a DHCP Discover message to locate a DHCP server.
#### 2. Offer
The DHCP server offers an available IP address and other network configuration information.
#### 3. Request
The client requests to use the offered IP address.
#### Acknowledge
The DHCP server confirms the assignment and provides:
- IP Address
- Subnet Mask
- Default Gateway
- DNS Server
### DHCP Lease
A DHCP lease is the amount of time a device is allowed to use an assigned IP address.
#### Key Points
- DHCP assigns IP addresses for a limited period called a lease.
- A device usually keeps getting the same IP address while the lease is valid.
- When reconnecting to the same network before the lease expires, the device will usually receive the same IP address.
- After the lease expires, the DHCP server may assign the IP address to another device.
## 13. NAT and Security
Nat only forwards incoming packets if the match an existing entry on the NAT table.
Packets that do not match any entry on the NAT table are dropped.
This prevents most unsolicited connections from reaching devices on the local network.
NAT provides a basic level of protection, but it is not a replacement for a firewall.
A firewall applies security rules to determine whether traffic should be allowed or blocked.
## 14. Firewalls
A firewall is a security system that monitors and controls incoming and outgoing network traffic according to predefined rules.
### Functions
- Allows legitimate traffic.
- Blocks unauthorized traffic.
- Protects device from unsolicited connections.
- Works together with NAT to improve network security.
### Key Points
Knowing a router public IP address does not automatically allow access to devices inside the network.
NAT forwards only traffic that matches an existing NAT table entry.
A firewall applies rules to determine whether traffic should be allowed or blocked.
Outbound connections initiated by devices inside the networks are generally allowed and their replies are permitted.
Unsolicited inbound connections are typically blocked unless explicitly allowed( for example, through port forwadding or firewall rules)
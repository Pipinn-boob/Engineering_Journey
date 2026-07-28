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

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
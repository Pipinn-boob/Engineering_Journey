#!/usr/bin/env python3
"""subnetcalc - a small subnet calculator CLI.

Project #1 of the Engineering Journey, grown directly out of the networking
notes in networking_basics/README.md:

- section 1  (IP addresses, subnet masks and /24 notation)
- section 11 (private and public IP address ranges)

Examples:
    python3 subnetcalc.py 192.168.100.107/24
    python3 subnetcalc.py 192.168.100.107 255.255.255.0
    python3 subnetcalc.py 10.0.0.0/8 --json
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys

# Special-purpose IPv4 ranges, most specific first. The RFC 1918 entries come
# from section 11 of the networking notes; the rest are the other ranges worth
# knowing for interviews and real-world troubleshooting.
IPV4_SPECIAL_RANGES: list[tuple[str, str]] = [
    ("0.0.0.0/8", "reserved (this network)"),
    ("10.0.0.0/8", "private (RFC 1918)"),
    ("100.64.0.0/10", "CGNAT / shared address space (RFC 6598)"),
    ("127.0.0.0/8", "loopback"),
    ("169.254.0.0/16", "link-local (APIPA)"),
    ("172.16.0.0/12", "private (RFC 1918)"),
    ("192.0.0.0/24", "reserved (IANA special-purpose)"),
    ("192.0.2.0/24", "documentation (TEST-NET-1, RFC 5737)"),
    ("192.88.99.0/24", "reserved (former 6to4 relay, RFC 7526)"),
    ("192.168.0.0/16", "private (RFC 1918)"),
    ("198.18.0.0/15", "benchmarking (RFC 2544)"),
    ("198.51.100.0/24", "documentation (TEST-NET-2, RFC 5737)"),
    ("203.0.113.0/24", "documentation (TEST-NET-3, RFC 5737)"),
    ("224.0.0.0/4", "multicast"),
    ("240.0.0.0/4", "reserved (formerly class E)"),
]

IPV6_SPECIAL_RANGES: list[tuple[str, str]] = [
    ("::/128", "unspecified"),
    ("::1/128", "loopback"),
    ("::ffff:0:0/96", "IPv4-mapped"),
    ("fc00::/7", "unique local (private)"),
    ("fe80::/10", "link-local"),
    ("2001:db8::/32", "documentation (RFC 3849)"),
    ("ff00::/8", "multicast"),
]

_IPV4_SPECIAL = [
    (ipaddress.ip_network(network), label) for network, label in IPV4_SPECIAL_RANGES
]
_IPV6_SPECIAL = [
    (ipaddress.ip_network(network), label) for network, label in IPV6_SPECIAL_RANGES
]

Network = ipaddress.IPv4Network | ipaddress.IPv6Network
Address = ipaddress.IPv4Address | ipaddress.IPv6Address


def classify(address: Address) -> str:
    """Return a human-readable scope label for *address*."""
    ranges = _IPV4_SPECIAL if address.version == 4 else _IPV6_SPECIAL
    for network, label in ranges:
        if address in network:
            return label
    return "public" if address.version == 4 else "global unicast"


def parse_network(address: str, mask: str | None = None) -> Network:
    """Parse 'ip/prefix' (or 'ip dotted-mask') into a network object.

    Host bits are accepted and collapsed (strict=False), so a query for a
    workstation address such as 192.168.100.107/24 still describes its /24.
    """
    text = f"{address}/{mask}" if mask else address
    try:
        return ipaddress.ip_network(text, strict=False)
    except ValueError as exc:
        raise ValueError(f"cannot parse {text!r} as a network") from exc


def usable_hosts(net: Network) -> int:
    """Number of addresses that can actually be assigned to hosts on *net*."""
    if net.version == 4:
        if net.prefixlen <= 30:
            return net.num_addresses - 2  # network and broadcast are reserved
        if net.prefixlen == 31:
            return 2  # RFC 3021 point-to-point link: both addresses usable
        return 1  # /32 single-host route
    return net.num_addresses  # IPv6 has no network/broadcast overhead


def host_range(net: Network) -> tuple[str, str]:
    """First and last assignable host addresses on *net*, as strings."""
    first = net.network_address
    last = net.network_address + (net.num_addresses - 1)
    if net.version == 4 and net.prefixlen <= 30:
        first += 1
        last -= 1
    return str(first), str(last)


def describe(net: Network, queried: Address | None = None) -> dict[str, str | int]:
    """Build the report dictionary for *net*.

    If *queried* is a host address that differs from the network address
    (e.g. 192.168.100.107 inside 192.168.100.0/24), it is recorded too.
    """
    info: dict[str, str | int] = {
        "network": f"{net.network_address}/{net.prefixlen}",
        "prefix length": net.prefixlen,
        "netmask": str(net.netmask),
        "wildcard mask": str(net.hostmask),
    }
    if net.version == 4:
        info["broadcast"] = str(net.broadcast_address)
    first, last = host_range(net)
    info["first host"] = first
    info["last host"] = last
    info["total addresses"] = net.num_addresses
    info["usable hosts"] = usable_hosts(net)
    info["scope"] = classify(net.network_address)
    if queried is not None and queried != net.network_address:
        info["queried address"] = str(queried)
    return info


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subnetcalc",
        description=(
            "Show network, broadcast, host range and scope "
            "for an IPv4/IPv6 subnet."
        ),
        epilog=(
            "examples:\n"
            "  %(prog)s 192.168.100.107/24\n"
            "  %(prog)s 192.168.100.107 255.255.255.0\n"
            "  %(prog)s 10.0.0.0/8 --json\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "address", help="IP address, optionally with a /prefix length"
    )
    parser.add_argument(
        "mask", nargs="?", help="optional dotted subnet mask (e.g. 255.255.255.0)"
    )
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        net = parse_network(args.address, args.mask)
        queried = ipaddress.ip_address(args.address.split("/")[0])
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    info = describe(net, queried)
    if args.json:
        print(json.dumps(info, indent=2))
    else:
        width = max(len(key) for key in info)
        for key, value in info.items():
            print(f"{key:<{width}} : {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

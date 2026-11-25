"""Tests for subnetcalc - the Engineering Journey's first project.

Run with:  python3 -m pytest -v
"""

import ipaddress
import json

import pytest

from subnetcalc import classify, describe, host_range, main, parse_network, usable_hosts


# --- parsing ----------------------------------------------------------------

def test_slash_24_basics():
    net = parse_network("192.168.100.107/24")  # the example from the notes
    assert str(net.network_address) == "192.168.100.0"
    assert str(net.broadcast_address) == "192.168.100.255"
    assert usable_hosts(net) == 254
    assert host_range(net) == ("192.168.100.1", "192.168.100.254")


def test_dotted_mask_input():
    net = parse_network("10.1.2.3", "255.255.0.0")
    assert str(net) == "10.1.0.0/16"
    assert usable_hosts(net) == 65534


def test_slash_30_has_two_usable_hosts():
    net = parse_network("192.168.1.4/30")
    assert usable_hosts(net) == 2
    assert host_range(net) == ("192.168.1.5", "192.168.1.6")


def test_slash_31_is_point_to_point_rfc3021():
    net = parse_network("10.0.0.0/31")
    assert usable_hosts(net) == 2
    assert host_range(net) == ("10.0.0.0", "10.0.0.1")


def test_slash_32_is_a_single_host():
    net = parse_network("8.8.8.8")  # no prefix -> /32
    assert net.prefixlen == 32
    assert usable_hosts(net) == 1
    assert host_range(net) == ("8.8.8.8", "8.8.8.8")


# --- scope classification (section 11 of the notes) -------------------------

@pytest.mark.parametrize(
    ("address", "expected"),
    [
        ("10.0.0.1", "private (RFC 1918)"),
        ("172.16.0.1", "private (RFC 1918)"),
        ("172.31.255.255", "private (RFC 1918)"),
        ("172.32.0.1", "public"),  # just outside RFC 1918 - classic trap
        ("192.168.100.107", "private (RFC 1918)"),
        ("203.0.113.50", "documentation (TEST-NET-3, RFC 5737)"),
        ("8.8.8.8", "public"),
        ("127.0.0.1", "loopback"),
        ("169.254.10.20", "link-local (APIPA)"),
        ("239.1.2.3", "multicast"),
        ("100.64.0.1", "CGNAT / shared address space (RFC 6598)"),
    ],
)
def test_classification(address, expected):
    assert classify(ipaddress.ip_address(address)) == expected


# --- reports ----------------------------------------------------------------

def test_describe_contains_the_key_fields():
    info = describe(parse_network("192.168.100.0/24"))
    for key in (
        "network",
        "netmask",
        "wildcard mask",
        "broadcast",
        "first host",
        "last host",
        "usable hosts",
        "scope",
    ):
        assert key in info


def test_describe_records_the_queried_host():
    info = describe(
        parse_network("192.168.100.107/24"),
        ipaddress.ip_address("192.168.100.107"),
    )
    assert info["queried address"] == "192.168.100.107"


def test_ipv6_documentation_prefix():
    info = describe(parse_network("2001:db8::/32"))
    assert info["scope"] == "documentation (RFC 3849)"
    assert "broadcast" not in info  # IPv6 has no broadcast address
    net = parse_network("2001:db8::/32")
    assert usable_hosts(net) == net.num_addresses


# --- command-line behaviour --------------------------------------------------

def test_json_output(capsys):
    assert main(["192.168.100.0/24", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["network"] == "192.168.100.0/24"
    assert payload["usable hosts"] == 254


def test_plain_output_is_aligned(capsys):
    assert main(["192.168.100.107/24"]) == 0
    out = capsys.readouterr().out
    assert "192.168.100.0/24" in out
    assert "queried address : 192.168.100.107" in out


def test_invalid_input_exits_with_error(capsys):
    assert main(["300.1.2.3/24"]) == 1
    assert "error" in capsys.readouterr().err

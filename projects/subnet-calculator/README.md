# subnet-calculator

A small command-line subnet calculator — Project #1 of the
[Engineering Journey](../../README.md).

It answers, for any IPv4 or IPv6 subnet, the questions posed in
[section 1](../../networking_basics/README.md#1-ip-addresses) and
[section 11](../../networking_basics/README.md#11-private-and-public-ip-addresses)
of my networking notes: network address, broadcast, usable host range,
wildcard mask, and whether the range is private, public, or otherwise
special (RFC 1918, CGNAT, TEST-NET, loopback, link-local, multicast).

Zero dependencies — Python standard library only.

## Usage

```bash
python3 subnetcalc.py 192.168.100.107/24          # ip/prefix
python3 subnetcalc.py 192.168.100.107 255.255.255.0  # ip + dotted mask
python3 subnetcalc.py 10.0.0.0/8 --json           # machine-readable
python3 subnetcalc.py --help
```

Real output — and yes, `192.168.100.107` is the same example used throughout
the networking notes:

```text
$ python3 subnetcalc.py 192.168.100.107/24
network         : 192.168.100.0/24
prefix length   : 24
netmask         : 255.255.255.0
wildcard mask   : 0.0.0.255
broadcast       : 192.168.100.255
first host      : 192.168.100.1
last host       : 192.168.100.254
total addresses : 256
usable hosts    : 254
scope           : private (RFC 1918)
queried address : 192.168.100.107
```

The documentation-range example (the same TEST-NET-3 range used in the
notes' NAT section):

```text
$ python3 subnetcalc.py 203.0.113.50/24
network         : 203.0.113.0/24
prefix length   : 24
netmask         : 255.255.255.0
wildcard mask   : 0.0.0.255
broadcast       : 203.0.113.255
first host      : 203.0.113.1
last host       : 203.0.113.254
total addresses : 256
usable hosts    : 254
scope           : documentation (TEST-NET-3, RFC 5737)
queried address : 203.0.113.50
```

Invalid input exits with code 1 and a message on stderr:

```text
$ python3 subnetcalc.py 300.1.2.3/24
error: cannot parse '300.1.2.3/24' as a network
```

## Tests

```bash
python3 -m pytest -v
```

22 tests cover /24 math, dotted-mask input, /30 and /31 (RFC 3021
point-to-point) and /32 edge cases, IPv6, scope-classification boundaries
(`172.31.255.255` is private, `172.32.0.1` is public), JSON output, and the
CLI error path.

## CI

GitHub Actions runs pytest on every push (on Python 3.11 and 3.13), plus
codespell and markdownlint for the whole repository — see
[.github/workflows/checks.yml](../../.github/workflows/checks.yml).

## What I learned

- Python's `ipaddress` module models the RFCs exactly — a /31 really does
  have two usable hosts per RFC 3021, and `strict=False` is what lets a
  workstation address like `192.168.100.107/24` be described as its /24.
- Special ranges are worth knowing as a table, not just RFC 1918: CGNAT
  (100.64/10), documentation TEST-NETs, loopback, link-local, multicast.
- The test suite caught a real bug before the first commit (I wrote
  `host_mask`; the attribute is `hostmask`) — which is the whole argument
  for writing tests in the first place.
- Edge cases are exactly where hand-written arithmetic goes wrong: the
  172.16/12 boundary and the /31//32 cases are pinned down by tests.
- Designing the output for humans *and* machines (`--json`) costs almost
  nothing when the report is just a dictionary.

## Ideas for v2

- VLSM helper: split a /24 into N right-sized subnets (extends notes §1).
- A **port-forwarding planner** that validates a table of
  `public port → internal ip:port` rules and flags ambiguous combinations —
  the topic of the newest section of my notes (§15).
- Warn when the queried address lands on the network or broadcast address.

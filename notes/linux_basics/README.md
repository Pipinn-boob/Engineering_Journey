# Linux Basics

Practical Linux notes for engineering work — the operating system underneath
almost every NOC, DevOps, cloud, and SOC role.

These notes are **not copy-pasted theory**: every command output below was
produced by actually running the command on 2026-11-25 in a Debian 12
container during a study session. Where the container behaves differently
from a full server (no root, no systemd, blocked ICMP in some
environments), that is called out explicitly — because knowing *why* a
command fails is half the skill.

## Contents

1. [The shell and the terminal](#1-the-shell-and-the-terminal)
2. [The filesystem](#2-the-filesystem)
3. [Users and groups](#3-users-and-groups)
4. [Permissions](#4-permissions)
5. [Processes](#5-processes)
6. [Pipes and redirection](#6-pipes-and-redirection)
7. [Networking commands](#7-networking-commands)
8. [Packages, sudo, and container limits](#8-packages-sudo-and-container-limits)
9. [Key takeaways](#9-key-takeaways)
10. [Practice checklist](#10-practice-checklist)
11. [Quick quiz](#11-quick-quiz)

## 1. The shell and the terminal

The shell is the program that reads your commands and asks the kernel to
execute them. Bash is the default on most distributions.

```console
$ uname -a
Linux e2b.local 6.1.158+ #1 SMP PREEMPT_DYNAMIC Mon May 11 18:48:24 UTC 2026 x86_64 GNU/Linux
$ whoami
user
$ id
uid=1001(user) gid=1001(user) groups=1001(user),27(sudo),100(users)
$ echo $SHELL
/bin/bash
```

What each line tells an engineer:

- `uname -a` — kernel version (`6.1.158+`) and architecture (`x86_64`). The
  first thing to check when a bug smells kernel-specific.
- `whoami` / `id` — which account I am and, more importantly, **which
  groups** I belong to. Note group `27(sudo)` — membership of the sudo
  group, which matters in section 8.
- `$SHELL` — which shell the login prompt hands me.

System health in one line:

```console
$ uptime
 19:37:16 up 3 min,  0 user,  load average: 0.14, 0.06, 0.01
```

The three load averages (1, 5, 15 min) roughly mean "processes wanting CPU
time". Rule of thumb: persistently above the CPU core count = overloaded.

## 2. The filesystem

Everything in Linux hangs off one root `/`. Drill: create, copy, rename,
delete.

```console
$ mkdir -p ~/linuxlab && cd ~/linuxlab && pwd
/home/user/linuxlab
$ touch report.txt && cp report.txt backup.txt && mv backup.txt renamed.txt
$ ls -l
total 0
-rw-r--r-- 1 user user 0 Nov 25 19:37 renamed.txt
-rw-r--r-- 1 user user 0 Nov 25 19:37 report.txt
$ rm renamed.txt && ls -l
total 0
-rw-r--r-- 1 user user 0 Nov 25 19:37 report.txt
```

Reading `ls -l` anatomy: `-rw-r--r-- 1 user user 0 Nov 25 19:37 renamed.txt`

| Field | Meaning |
| ----- | ------- |
| `-` | file type (`-` file, `d` directory, `l` symlink) |
| `rw-r--r--` | permissions — owner, group, others (section 4) |
| `1` | hard-link count |
| `user user` | owning user, owning group |
| `0` | size in bytes |
| date/time | last modification |

## 3. Users and groups

Linux is multi-user from the ground up; accounts live in `/etc/passwd`
with one line per user, colon-separated:
`name:password-placeholder:uid:gid:comment:home:shell`.

```console
$ cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn
     21 /usr/sbin/nologin
      3 /bin/bash
      1 /bin/sync
```

This one pipeline (section 6) counts login shells on the live system: of
25 accounts, 21 are service accounts locked out of interactive login
(`nologin`), only 3 can open a shell. On a server you administer, that
ratio is normal — and reviewing it is a basic hardening check.

## 4. Permissions

Every file carries three permission triplets — owner / group / others —
each `r`ead(4) `w`rite(2) e`x`ecute(1). The octal form sums them.

| Octal | Letters | Meaning |
| ----- | ------- | ------- |
| 644 | `rw-r--r--` | owner edits, everyone reads (typical config file) |
| 600 | `rw-------` | owner only (secrets, SSH keys) |
| 755 | `rwxr-xr-x` | owner runs/edits, others run (scripts, binaries) |
| 700 | `rwx------` | owner only, executable |

Live demonstration, including the symbolic form:

```console
$ touch newfile.txt && stat -c '%A %a %n' newfile.txt
-rw-r--r-- 644 newfile.txt
$ chmod 755 newfile.txt && stat -c '%A %a %n' newfile.txt
-rwxr-xr-x 755 newfile.txt
$ chmod u-x,g-w,o=r newfile.txt && stat -c '%A %a %n' newfile.txt
-rw-r-xr-- 654 newfile.txt
```

Notice the symbolic result: `755` → `654` — owner lost `x`, group lost `w`,
others were *set* to `r` exactly.

Why 600 matters — a secrets file nobody else can read:

```console
$ echo "db_password=changeme" > secrets.txt
$ chmod 600 secrets.txt && ls -l secrets.txt
-rw------- 1 user user 20 Nov 25 19:37 secrets.txt
```

The classic real-world pair. Both are owned by root, but:

```console
$ ls -l /etc/passwd /etc/shadow
-rw-r--r-- 1 root root   1207 Jun 15 16:59 /etc/passwd
-rw-r----- 1 root shadow  635 Jun 15 17:00 /etc/shadow
$ head -1 /etc/shadow
head: cannot open '/etc/shadow' for reading: Permission denied
$ echo $?
1
```

`/etc/passwd` is world-readable (it holds non-secret account info);
`/etc/shadow` holds password hashes and is `root:shadow` only — attempting
to read it fails with exit code 1. Exit codes are how scripts detect
failure: `0` = success, non-zero = error.

**umask** — the default permission subtractor for *new* files. Here it is
`0022`: group and others lose `w` by default, which is why `touch` gave
`644`, not `666`.

## 5. Processes

`ps -ef --forest` draws the process family tree. The interesting top of
this system:

```console
$ ps -ef --forest | head -12
UID          PID    PPID  C STIME TTY          TIME CMD
root           2       0  0 19:34 ?        00:00:00 [kthreadd]
root           3       2  0 19:34 ?        00:00:00  \_ [rcu_gp]
root           4       2  0 19:34 ?        00:00:00  \_ [rcu_par_gp]
...
root           7       2  0 19:34 ?        00:00:00  \_ [kworker/0:0H-events_highpri]
```

PID 1's children here are **kernel threads** (bracketed names) — this is
how a container looks: it shares the host kernel instead of booting its
own. On a VM you would see systemd as PID 1 with services beneath it.

Starting a process in the background, inspecting, and stopping it:

```console
$ sleep 300 & JOB=$!
$ echo $JOB
1544
$ ps -o pid,ppid,stat,etime,cmd -p $JOB
    PID    PPID STAT     ELAPSED CMD
   1544    1539 R          00:00 sleep 300
$ kill $JOB
$ ps -o pid,stat,cmd -p $JOB
    PID STAT CMD
```

`kill` sends **SIGTERM** by default — a polite "please exit" that lets the
program clean up (this is why `kill -9` is the *last* resort: SIGKILL
gives no such chance). The empty `ps` line afterwards proves the process
is gone.

## 6. Pipes and redirection

The Unix superpower: small tools chained so the output of one becomes the
input of the next. Already used above, worth naming:

- `cut -d: -f7` — take field 7 (split on `:`)
- `sort | uniq -c | sort -rn` — group, count, rank
- `wc -l` — count lines
- `grep pattern` — keep matching lines
- `awk` — column extraction

```console
$ ls -1 /usr/bin | wc -l
635
$ uptime | awk -F'load average:' '{print $2}'
 0.11, 0.05, 0.01
```

Redirection: `>` overwrites, `>>` appends, `2>` captures stderr, `|` pipes
stdout. Logs and reports are almost always built this way, e.g.
`command >> /var/log/mylog.txt 2>&1`.

## 7. Networking commands

The toolbox, verified first (see section 8 for why checking is a habit):

```console
$ for c in ip ss ping curl getent hostname; do command -v $c >/dev/null && echo "$c: installed" || echo "$c: NOT installed"; done
ip: installed
ss: installed
ping: installed
curl: installed
getent: installed
hostname: installed
```

### Addresses and routes

```console
$ ip -brief addr
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             169.254.0.21/30 fe80::fc:ff:fe00:5/64
$ ip route
default via 169.254.0.22 dev eth0
169.254.0.20/30 dev eth0 proto kernel scope link src 169.254.0.21
```

This live output ties straight into the
[networking notes](../../networking_basics/README.md):

- `lo` — loopback, `127.0.0.1/8`.
- `eth0` has **`169.254.0.21/30`** — link-local (APIPA) addressing, from
  the special-ranges table in the subnet calculator. A `/30` has exactly
  two usable hosts: `.21` (this container) and `.22` — which `ip route`
  confirms is the **default gateway**. One command pair, and the whole
  "local vs remote" decision from notes §1 is visible on a real machine.
- `fe80::...` — IPv6 link-local counterpart (notes §1, IPv6).

### Listening sockets

```console
$ ss -tln
State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
LISTEN 0      4096         0.0.0.0:111        0.0.0.0:*
LISTEN 0      4096               *:49983            *:*
LISTEN 0      4096               *:22               *:*
```

Port **22 = SSH** (notes §9/§15 territory). First command to run on any
box you inherit: what is listening, and what *should* be.

### DNS

```console
$ cat /etc/resolv.conf
nameserver 8.8.8.8
$ getent hosts github.com
172.194.155.208 github.com
```

The resolver config (here Google DNS `8.8.8.8`) plus a live name→IP
resolution — DNS from notes §3 in action. `nslookup`/`dig` do the same
job with more detail.

### When commands fail — read the error

`curl -s` silences *everything*, including errors. Two hosts, same
command, different worlds:

```console
$ curl -sS -o /dev/null -w "example.com: HTTP %{http_code}\n" --max-time 8 https://example.com
curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to example.com:443
example.com: HTTP 000
$ curl -sS -o /dev/null -w "github.com: HTTP %{http_code}\n" --max-time 8 https://github.com
github.com: HTTP 200
```

`HTTP 000` + `curl: (35)` means the TLS handshake itself failed for
`example.com` (this sandbox only allows certain destinations — the same
reason a corporate firewall blocks sites). The lesson generalizes: **use
`-sS` in scripts, never bare `-s`**, or you will debug blindfolded.

### ping

```console
$ ping -c 2 8.8.8.8
64 bytes from 8.8.8.8: icmp_seq=1 ttl=113 time=0.525 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=113 time=0.385 ms
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1010ms
rtt min/avg/max/mdev = 0.385/0.455/0.525/0.070 ms
```

Exactly the statistics described in notes §6: replies, loss %, and
min/avg/max RTT. Two things worth noticing:

- `ttl=113` — TTL started at 128 (Linux default), so ~15 hops were
  subtracted... yet the RTT is a suspicious **0.4 ms**. Real Google DNS is
  ~30–200 ms away. In this sandbox the egress proxy answers ICMP nearby.
  **When numbers look impossible, question them** — the same skill as
  reading a suspicious traceroute.
- Many container/cloud environments block raw sockets; if `ping` fails
  there with `Operation not permitted`, that is the environment, not your
  network.

`traceroute` is not installed in this container — on a real server it
shows the hop-by-hop path (notes §6), and it is one of the first tools to
install alongside `tcpdump`.

## 8. Packages, sudo, and container limits

This session ran inside a container, which teaches what **cannot** be
done without root:

- `apt install <pkg>` — requires root (`sudo`). Installing tools is a
  root job by design.
- `useradd`, `passwd <user>` — root only.
- `systemctl status ssh` — no systemd here (no PID 1 systemd, section 5).
  On a real server this is *the* service manager: `systemctl status ssh`,
  `systemctl restart nginx`, `systemctl enable --now docker`.
- `chown` — root only (file ownership changes need privilege).

`id` showed membership of group `27(sudo)` — on a normal server that
means I could run the above with `sudo <command>` after authenticating.
Habit to build from day one: run daily work as a normal user, escalate
only for admin commands.

For a Windows laptop, **WSL2** (Windows Subsystem for Linux) gives a real
Ubuntu/Debian environment with systemd support — ideal for the practice
checklist below.

## 9. Key takeaways

- `id` before `sudo`: know who you are and which groups you hold.
- Read `ls -l` as *type + triplets + owner + group*; secrets get `600`,
  shared configs `644`, executables `755`.
- Exit codes (`0`/non-zero) are how scripts know success from failure —
  check them (`echo $?`) when a command misbehaves.
- `kill` sends SIGTERM by default; SIGKILL (`-9`) is the last resort.
- Pipelines (`cut | sort | uniq -c | sort -rn`) turn raw system files into
  reports in one line.
- `ip -brief addr` + `ip route` answer "where am I and how do I reach the
  world" — and instantly reveal private vs link-local vs public
  addressing.
- `ss -tln` is the first command on any inherited server: know what is
  listening.
- `-s` hides errors; `-sS` shows them. Never debug silently.
- If a number looks impossible (0.4 ms to Google), question the
  measurement path before trusting it.

## 10. Practice checklist

Reproduce this whole session yourself — on WSL2, a VM, or any Linux box:

- [ ] `uname -a`, `id`, `uptime` — record kernel, groups, load
- [ ] Build the section 2 file drill from scratch, then `ls -l` and read
      every column aloud
- [ ] `chmod` one file through 644 → 755 → symbolic change → verify each
      with `stat -c '%A %a %n'`
- [ ] `cat /etc/shadow` — read the failure message and exit code
- [ ] Start `sleep 300 &`, find it with `ps`, kill it with SIGTERM, verify
      it is gone
- [ ] Count the login shells on your own system with the section 3
      pipeline
- [ ] `ip -brief addr` and `ip route` — identify network, /prefix, and
      gateway; confirm with the subnet calculator:
      `python3 projects/subnet-calculator/subnetcalc.py <your-ip>/<prefix>`
- [ ] `ss -tln` — list listeners and explain every port
- [ ] Break a curl on purpose (`-s`), then fix your visibility (`-sS`)

## 11. Quick quiz

1. **What does `chmod 755` mean in letters, and who can do what?**
   `rwxr-xr-x` — owner reads/writes/executes; group and others read and
   execute but cannot write.
2. **Why is `/etc/shadow` unreadable to you but `/etc/passwd` is not?**
   Password hashes are secrets: `shadow` is `root:shadow` with no
   world-read; `passwd` holds only non-secret account data.
3. **What signal does plain `kill` send, and why prefer it over `kill -9`?**
   SIGTERM — it lets the process clean up; SIGKILL cannot be caught, so
   state can be left corrupt.
4. **A `/30` network like `169.254.0.20/30` — how many usable hosts, and
   which are they?**
   Two: `.21` and `.22` (network `.20` and broadcast `.23` excluded) —
   exactly the point-to-point pair this container and its gateway use.
5. **Your script's `curl` never fails visibly but downloads nothing. Why?**
   `-s` silences errors too; use `-sS` (and check `$?` / `%{http_code}`)
   so TLS and HTTP failures surface.

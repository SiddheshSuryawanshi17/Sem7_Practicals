# CSDF Assignment 6 – Vulnerability assessment with Wireshark / SNORT

**Problem Statement:** Configure and demonstrate use of vulnerability assessment tool like Wireshark or SNORT.

Files here:
| File | Use |
|---|---|
| `Wireshark.pcapng` | Previously captured traffic. Open it in Wireshark if live capture is not allowed in the lab |
| `Screenshots/` | Capture properties, colouring rules, IO graph screenshots for the write-up |
| `local.rules` | Custom Snort rules |

---
## Part A – Wireshark (most colleges ask this)
1. Install from https://www.wireshark.org (Windows: also install **Npcap**). Linux: `sudo apt install wireshark`.
2. Open Wireshark → choose the active interface (**Wi-Fi / Ethernet**, the one with the moving graph) → click the blue fin to **start capture**.
3. Generate traffic: open a browser and visit `http://testphp.vulnweb.com` (plain HTTP), run `ping google.com`, `nslookup google.com`.
4. Click the red square to **stop**. **File → Save As** `capture.pcapng`.
5. Demonstrate **display filters** (type in the filter bar, press Enter):

| Filter | Shows |
|---|---|
| `http` | HTTP traffic |
| `dns` | DNS queries/responses |
| `icmp` | ping packets |
| `tcp.port == 443` | HTTPS traffic |
| `ip.addr == 192.168.1.5` | traffic to/from one host |
| `ip.src == 192.168.1.5 && tcp` | TCP sent by a host |
| `http.request.method == "POST"` | form submissions |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | SYN packets (port-scan detection) |
| `tcp.analysis.retransmission` | network problems |
| `arp.duplicate-address-detected` | ARP spoofing |

6. **Vulnerability demo – credentials in clear text:** on `http://testphp.vulnweb.com/login.php` log in with `test`/`test` → filter `http.request.method == "POST"` → right-click the packet → **Follow → HTTP Stream**. The username and password are visible because **HTTP is unencrypted**. Recommendation: use HTTPS.
7. **TCP 3-way handshake:** filter `tcp.stream eq 0` → show SYN → SYN-ACK → ACK.
8. **Statistics menu** (screenshots in `Screenshots/`):
   - Statistics → **Capture File Properties**
   - Statistics → **Protocol Hierarchy**
   - Statistics → **Conversations** / **Endpoints**
   - Statistics → **I/O Graph**
   - View → **Coloring Rules**
9. **Analyze → Expert Information** shows warnings/errors (malformed packets, retransmissions).

## Part B – SNORT (IDS)
**Linux (Ubuntu):**
```bash
sudo apt install snort                    # enter your network e.g. 192.168.1.0/24 when asked
sudo cp local.rules /etc/snort/rules/local.rules
sudo snort -T -c /etc/snort/snort.conf    # test configuration -> "Snort successfully validated"
ip a                                      # find interface name e.g. eth0 / wlan0 / enp0s3
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
```
From another machine (or the same machine): `ping <your-ip>`, `nmap -sS <your-ip>`. Alerts appear in the console:
```
[**] [1:1000001:1] ICMP Ping detected [**] {ICMP} 192.168.1.7 -> 192.168.1.5
```
Run Snort on the saved capture: `sudo snort -A console -q -c /etc/snort/snort.conf -r Wireshark.pcapng`

**Windows:** install Npcap + Snort 2.9 → edit `C:\Snort\etc\snort.conf` (set `HOME_NET`, rule paths) → `snort -W` lists interfaces → `snort -i 1 -c C:\Snort\etc\snort.conf -A console`.

**Snort modes:** Sniffer (`snort -v`), Packet logger (`snort -l ./log`), NIDS (`snort -c snort.conf`).
**Rule anatomy:** `alert tcp any any -> $HOME_NET 22 (msg:"..."; flags:S; sid:1000005; rev:1;)` = action, protocol, source IP/port, direction, destination IP/port, options. Custom rules use sid ≥ 1,000,000.

## Conclusion
Wireshark captured and analysed packets, which exposed clear-text credentials over HTTP. Snort detected ping, port scans and brute-force attempts using custom rules.

# CSDF Assignment 5
# Write a program to detect and prevent intrusion attempts on a Wi-Fi network
# (authentication-failure / brute-force / deauthentication flood / rogue AP detection).
#
# The program reads Wi-Fi access-point logs (wifi_auth.log, generated on first run),
# DETECTS attacks with rules, and PREVENTS them by adding the attacker's MAC to a
# blocklist (MAC filtering), so later attempts from that device are rejected.
#
# Run: python wifi_ids.py
import datetime as dt
import os
import re
from collections import defaultdict

LOG = "wifi_auth.log"
BLOCKLIST = "blocked_macs.txt"
TRUSTED_APS = {"CollegeWiFi": "AA:BB:CC:00:11:22"}   # SSID -> legitimate BSSID
FAIL_LIMIT = 5
WINDOW = dt.timedelta(minutes=2)
DEAUTH_LIMIT = 20


def create_sample_log():
    t = dt.datetime(2025, 10, 20, 10, 0, 0)
    lines = []
    add = lambda sec, ev, mac, extra="": lines.append(f"{t + dt.timedelta(seconds=sec):%Y-%m-%d %H:%M:%S} {ev} mac={mac} {extra}".strip())
    add(0, "AUTH_SUCCESS", "11:22:33:44:55:01", "ssid=CollegeWiFi")
    add(5, "AUTH_FAIL", "11:22:33:44:55:02", "ssid=CollegeWiFi reason=wrong_psk")   # one typo - normal
    add(9, "AUTH_SUCCESS", "11:22:33:44:55:02", "ssid=CollegeWiFi")
    for i in range(8):                                                              # brute force
        add(20 + i * 6, "AUTH_FAIL", "DE:AD:BE:EF:00:01", "ssid=CollegeWiFi reason=wrong_psk")
    for i in range(25):                                                             # deauth flood
        add(100 + i, "DEAUTH", "66:66:66:66:66:66", "target=11:22:33:44:55:01")
    add(130, "BEACON", "99:88:77:66:55:44", "ssid=CollegeWiFi")                    # evil twin / rogue AP
    add(140, "BEACON", "AA:BB:CC:00:11:22", "ssid=CollegeWiFi")
    add(200, "AUTH_FAIL", "DE:AD:BE:EF:00:01", "ssid=CollegeWiFi reason=wrong_psk") # attacker comes back
    with open(LOG, "w") as f:
        f.write("\n".join(lines) + "\n")


def load_blocklist():
    if not os.path.exists(BLOCKLIST):
        return set()
    with open(BLOCKLIST) as f:
        return {l.strip() for l in f if l.strip()}


def block(mac, reason, blocked):
    if mac not in blocked:
        blocked.add(mac)
        with open(BLOCKLIST, "a") as f:
            f.write(mac + "\n")
        print(f"   [PREVENT] MAC {mac} added to blocklist ({reason})")


def analyze():
    pattern = re.compile(r"(\S+ \S+) (\w+) mac=(\S+)\s*(.*)")
    blocked = load_blocklist()
    fails = defaultdict(list)
    deauths = defaultdict(int)

    print(f"{'Time':<20}{'Event':<14}{'MAC':<20}Action")
    with open(LOG) as f:
        for line in f:
            m = pattern.match(line.strip())
            if not m:
                continue
            ts, ev, mac, extra = m.groups()
            t = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

            if mac in blocked:
                print(f"{ts:<20}{ev:<14}{mac:<20}DROPPED (MAC is blocked)")
                continue
            print(f"{ts:<20}{ev:<14}{mac:<20}allowed")

            if ev == "AUTH_FAIL":
                fails[mac] = [x for x in fails[mac] if t - x <= WINDOW] + [t]
                if len(fails[mac]) >= FAIL_LIMIT:
                    print(f"   [DETECT] Brute-force on PSK: {len(fails[mac])} failures from {mac} within {WINDOW}")
                    block(mac, "brute force", blocked)
            elif ev == "DEAUTH":
                deauths[mac] += 1
                if deauths[mac] == DEAUTH_LIMIT:
                    print(f"   [DETECT] Deauthentication flood (DoS) from {mac}: {DEAUTH_LIMIT}+ frames")
                    block(mac, "deauth flood", blocked)
            elif ev == "BEACON":
                ssid = re.search(r"ssid=(\S+)", extra).group(1)
                if ssid in TRUSTED_APS and TRUSTED_APS[ssid] != mac:
                    print(f"   [DETECT] Rogue AP / Evil twin: SSID '{ssid}' broadcast by unknown BSSID {mac}")
                    block(mac, "rogue access point", blocked)


if __name__ == "__main__":
    for f in (LOG, BLOCKLIST):
        if os.path.exists(f):
            os.remove(f)
    create_sample_log()
    print(f"Analyzing {LOG} ...\n")
    analyze()
    print(f"\nBlocked devices saved in {BLOCKLIST}: {sorted(load_blocklist())}")

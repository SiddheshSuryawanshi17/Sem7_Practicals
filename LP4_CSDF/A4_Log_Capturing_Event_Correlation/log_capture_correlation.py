# CSDF Assignment 4
# Write a program for Log Capturing and Event Correlation.
#
# Part 1 - Log capturing: captures real system activity (running processes,
#          file changes in a watched folder) plus login events, and writes
#          everything to a common log file (system_events.log) in one format.
# Part 2 - Event correlation: reads the log and applies correlation rules to
#          link separate events into security incidents.
#
# Run: python log_capture_correlation.py
import datetime as dt
import os
import random
import re
import subprocess
from collections import defaultdict

LOG_FILE = "system_events.log"
WATCH_DIR = "watched_folder"


def log(f, ts, source, event, user, ip, detail):
    f.write(f"{ts:%Y-%m-%d %H:%M:%S} | {source:<8} | {event:<15} | user={user:<8} | ip={ip:<15} | {detail}\n")


# ---------------------------------------------------------------- Part 1: capture
def capture_processes():
    try:
        if os.name == "nt":
            out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.splitlines()[3:]
            return [l.split()[0] for l in out if l.strip()][:10]
        out = subprocess.run(["ps", "-eo", "comm"], capture_output=True, text=True).stdout.splitlines()[1:]
        return [os.path.basename(l.strip()) for l in out][:10]
    except Exception:
        return []


def capture_file_activity():
    os.makedirs(WATCH_DIR, exist_ok=True)
    before = set(os.listdir(WATCH_DIR))
    # simulate user activity in the watched folder
    with open(os.path.join(WATCH_DIR, "salary_data.xlsx"), "w") as f:
        f.write("confidential")
    with open(os.path.join(WATCH_DIR, "notes.txt"), "w") as f:
        f.write("hello")
    after = set(os.listdir(WATCH_DIR))
    return sorted(after - before) or sorted(after)


def capture_logs():
    base = dt.datetime.now().replace(microsecond=0) - dt.timedelta(minutes=30)
    with open(LOG_FILE, "w") as f:
        # Real process snapshot
        for p in capture_processes():
            log(f, base, "PROCESS", "PROCESS_RUNNING", os.getenv("USER", os.getenv("USERNAME", "system")), "127.0.0.1", p)

        # Normal user logins
        for i, user in enumerate(["alice", "bob", "carol"]):
            log(f, base + dt.timedelta(minutes=i), "AUTH", "LOGIN_SUCCESS", user, f"192.168.1.{10 + i}", "ssh login")

        # Attack scenario: brute force from an external IP, then success, then data theft
        attacker = "203.0.113.45"
        t = base + dt.timedelta(minutes=5)
        for i in range(6):
            log(f, t + dt.timedelta(seconds=20 * i), "AUTH", "LOGIN_FAILED", "admin", attacker, "invalid password")
        t += dt.timedelta(minutes=3)
        log(f, t, "AUTH", "LOGIN_SUCCESS", "admin", attacker, "ssh login")
        log(f, t + dt.timedelta(minutes=1), "SYSTEM", "PRIV_ESCALATION", "admin", attacker, "sudo su root")
        for name in capture_file_activity():
            log(f, t + dt.timedelta(minutes=2), "FILE", "FILE_ACCESS", "admin", attacker, os.path.join(WATCH_DIR, name))
        log(f, t + dt.timedelta(minutes=3), "NETWORK", "DATA_TRANSFER", "admin", attacker, "outbound 250 MB to 203.0.113.45:443")

        # Some random failed logins (noise, below threshold)
        for _ in range(2):
            log(f, base + dt.timedelta(minutes=random.randint(10, 20)), "AUTH", "LOGIN_FAILED", "bob", "192.168.1.11", "typo")
    print(f"[Capture] Events written to {LOG_FILE}\n")


# ---------------------------------------------------------------- Part 2: correlate
LINE_RE = re.compile(r"(\S+ \S+) \| (\S+)\s*\| (\S+)\s*\| user=(\S+)\s*\| ip=(\S+)\s*\| (.*)")


def parse_logs():
    events = []
    with open(LOG_FILE) as f:
        for line in f:
            m = LINE_RE.match(line.strip())
            if m:
                ts, src, ev, user, ip, detail = m.groups()
                events.append({"time": dt.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"), "source": src,
                               "event": ev, "user": user, "ip": ip, "detail": detail})
    return sorted(events, key=lambda e: e["time"])


def correlate(events, fail_threshold=5, window=dt.timedelta(minutes=5)):
    alerts = []
    by_ip = defaultdict(list)
    for e in events:
        by_ip[e["ip"]].append(e)

    for ip, evs in by_ip.items():
        fails = [e for e in evs if e["event"] == "LOGIN_FAILED"]

        # Rule 1: Brute force - N failed logins from same IP within the time window
        for i in range(len(fails)):
            in_window = [f for f in fails[i:] if f["time"] - fails[i]["time"] <= window]
            if len(in_window) >= fail_threshold:
                alerts.append(("HIGH", f"Brute-force attack from {ip}: {len(in_window)} failed logins within {window}"))
                break

        # Rule 2: Failed logins followed by a success -> account compromise
        if len(fails) >= fail_threshold:
            success = [e for e in evs if e["event"] == "LOGIN_SUCCESS" and e["time"] > fails[-1]["time"]]
            if success:
                alerts.append(("CRITICAL", f"Account '{success[0]['user']}' compromised from {ip} at {success[0]['time']}"))

                # Rule 3: Post-compromise activity chain (kill chain)
                after = [e for e in evs if e["time"] >= success[0]["time"]]
                chain = [e["event"] for e in after]
                if "PRIV_ESCALATION" in chain:
                    alerts.append(("CRITICAL", f"Privilege escalation by {ip} after compromise"))
                if "FILE_ACCESS" in chain and "DATA_TRANSFER" in chain:
                    files = ", ".join(e["detail"] for e in after if e["event"] == "FILE_ACCESS")
                    alerts.append(("CRITICAL", f"Data exfiltration by {ip}: accessed [{files}] then large outbound transfer"))

        # Rule 4: Login from a non-internal IP
        if not ip.startswith(("192.168.", "10.", "127.")) and any(e["event"] == "LOGIN_SUCCESS" for e in evs):
            alerts.append(("MEDIUM", f"Successful login from external IP {ip}"))
    return alerts


if __name__ == "__main__":
    capture_logs()
    events = parse_logs()
    print(f"[Parse] {len(events)} events loaded. Last 12 events:")
    for e in events[-12:]:
        print(f"  {e['time']}  {e['source']:<8} {e['event']:<16} {e['user']:<6} {e['ip']:<15} {e['detail']}")

    print("\n[Correlate] Security alerts:")
    alerts = correlate(events)
    for level, msg in alerts:
        print(f"  [{level:<8}] {msg}")
    if not alerts:
        print("  No incidents detected.")

    with open("incident_report.txt", "w") as f:
        f.write("INCIDENT REPORT\n" + "=" * 40 + "\n")
        for level, msg in alerts:
            f.write(f"[{level}] {msg}\n")
    print("\nIncident report saved to incident_report.txt")

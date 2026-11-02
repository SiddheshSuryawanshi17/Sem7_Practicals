# CSDF Assignment 1
# Write a program for Tracking Emails and Investigating Email Crimes,
# i.e. write a program to analyze an e-mail header.
#
# Run:  python email_header_analyzer.py                 (uses sample_header.txt)
#       python email_header_analyzer.py my_header.txt   (your own header)
# Get a real header: Gmail -> open mail -> 3 dots -> "Show original" -> copy all -> save as .txt
import re
import sys
from email import message_from_string
from email.utils import parseaddr

IP_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?![\d.])")


def is_private(ip):
    a, b = map(int, ip.split(".")[:2])
    return a == 10 or a == 127 or (a == 172 and 16 <= b <= 31) or (a == 192 and b == 168)


def analyze(raw):
    msg = message_from_string(raw)

    print("=" * 60)
    print("BASIC HEADER FIELDS")
    print("=" * 60)
    for field in ["From", "To", "Cc", "Subject", "Date", "Message-ID", "Return-Path",
                  "Reply-To", "MIME-Version", "Content-Type", "X-Mailer", "X-Originating-IP"]:
        if msg.get(field):
            print(f"{field:18}: {msg.get(field)}")

    print("\n" + "=" * 60)
    print("MAIL ROUTE (Received headers, oldest hop first)")
    print("=" * 60)
    received = msg.get_all("Received") or []
    public_ips = []
    for hop, r in enumerate(reversed(received), 1):
        r = " ".join(r.split())
        frm = re.search(r"from\s+(\S+)", r)
        by = re.search(r"by\s+(\S+)", r)
        date = r.split(";")[-1].strip() if ";" in r else "-"
        ips = [ip for ip in IP_RE.findall(r) if all(int(o) <= 255 for o in ip.split("."))]
        print(f"Hop {hop}: from {frm.group(1) if frm else '?'}  ->  by {by.group(1) if by else '?'}")
        print(f"        IPs: {', '.join(ips) or '-'}   Time: {date}")
        public_ips += [ip for ip in ips if not is_private(ip)]

    if public_ips:
        print(f"\nLikely originating (first public) IP: {public_ips[0]}")
        print("Trace it with: whois", public_ips[0], " or  https://www.abuseipdb.com")

    print("\n" + "=" * 60)
    print("AUTHENTICATION RESULTS (SPF / DKIM / DMARC)")
    print("=" * 60)
    auth = " ".join(msg.get_all("Authentication-Results") or []) + " " + (msg.get("Received-SPF") or "")
    results = {}
    for check in ["spf", "dkim", "dmarc"]:
        m = re.search(check + r"=(\w+)", auth, re.I)
        results[check] = m.group(1).lower() if m else "not found"
        print(f"{check.upper():6}: {results[check]}")

    print("\n" + "=" * 60)
    print("SPOOFING / PHISHING INDICATORS")
    print("=" * 60)
    warnings = []
    from_addr = parseaddr(msg.get("From", ""))[1].lower()
    from_domain = from_addr.split("@")[-1] if "@" in from_addr else ""
    rp = parseaddr(msg.get("Return-Path", ""))[1].lower()
    reply = parseaddr(msg.get("Reply-To", ""))[1].lower()

    if rp and from_domain and not rp.endswith(from_domain):
        warnings.append(f"Return-Path domain ({rp}) differs from From domain ({from_domain})")
    if reply and from_domain and not reply.endswith(from_domain):
        warnings.append(f"Reply-To ({reply}) differs from From domain ({from_domain})")
    for check, res in results.items():
        if res in ("fail", "softfail", "none", "permerror"):
            warnings.append(f"{check.upper()} check result is '{res}'")
    if not msg.get("Message-ID"):
        warnings.append("Message-ID header is missing")

    if warnings:
        for w in warnings:
            print("[!]", w)
        print("\nVERDICT: Email is SUSPICIOUS (possible spoofing / phishing)")
    else:
        print("No indicators found.\nVERDICT: Email appears legitimate")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_header.txt"
    with open(path, encoding="utf-8", errors="ignore") as f:
        analyze(f.read())

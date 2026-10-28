# LP-IV : Cyber Security and Digital Forensics (CSDF)

All programs are **Python 3 using only the standard library** (A2's image CAPTCHA uses Pillow, with a text fallback if Pillow is missing). Each folder has a `sample_output.txt`.

| # | Problem statement | Folder | Run |
|---|---|---|---|
| 1 | Tracking emails and investigating email crimes: analyze an e-mail header | `A1_Email_Header_Analysis` | `python email_header_analyzer.py` (or pass your own header .txt) |
| 2 | Generate and verify a CAPTCHA image | `A2_CAPTCHA` | `python captcha_app.py` |
| 3 | Forensic program for recovering deleted files and deleted partitions | `A3_Recover_Deleted_Files_Partitions` | `python make_test_image.py` then `python recover_deleted.py disk.img` |
| 4 | Log capturing and event correlation | `A4_Log_Capturing_Event_Correlation` | `python log_capture_correlation.py` |
| 5 | Wi-Fi intrusion detection and prevention (brute force, deauth flood, rogue AP) | `A5_WiFi_Intrusion_Detection_Prevention` | `python wifi_ids.py` |
| 6 | Configure and demonstrate a vulnerability assessment tool like Wireshark or SNORT | `A6_Wireshark_SNORT` | see its README; saved `.pcapng`, screenshots, `local.rules` |

> Assignment numbering differs slightly between colleges. Match by **title** with your journal.

## Viva quick answers
**Email forensics (A1)**
- Read `Received:` headers **bottom to top**. The lowest one is closest to the sender, and the first public IP is the likely origin.
- **SPF**: is the sending IP allowed by the domain's DNS? **DKIM**: digital signature of the mail, verified with the public key in DNS. **DMARC**: policy (none/quarantine/reject) applied when SPF/DKIM fail.
- Spoofing signs: From ≠ Return-Path / Reply-To, SPF/DKIM/DMARC fail, look-alike domains (paypa1.com).
- Tools: MXToolbox header analyzer, Google Admin Toolbox *Messageheader*, `whois`, `nslookup`.

**CAPTCHA (A2)**: Completely Automated Public Turing test to tell Computers and Humans Apart. Types: text, image, audio, math, reCAPTCHA v2 (checkbox) and v3 (score). Noise, rotation and lines defeat OCR bots. Prevents brute force, spam and bot sign-ups.

**Deleted file recovery (A3)**
- Deleting a file only removes its **file-system entry** (FAT entry / MFT record marked free). The data stays in unallocated space until overwritten.
- **File carving**: search raw bytes for magic numbers: JPG `FF D8 FF … FF D9`, PNG `89 50 4E 47`, PDF `%PDF … %%EOF`, ZIP `50 4B 03 04`.
- **MBR**: sector 0, 512 bytes, 446 bytes bootcode + 4×16-byte partition entries + `55 AA`. **GPT**: up to 128 partitions, header "EFI PART".
- Always work on a **forensic image** (`dd`, FTK Imager) and record its **hash** (MD5/SHA-256) for the **chain of custody**. Use a write blocker.
- Tools: Autopsy / The Sleuth Kit, FTK Imager, Recuva, TestDisk (partitions), PhotoRec, Foremost, Scalpel.

**Log capturing and correlation (A4)**
- Logs: Windows Event Viewer (Security event IDs **4624** logon success, **4625** logon failure, 4720 user created), Linux `/var/log/auth.log`, `syslog`, `journalctl`.
- **Correlation** links separate events from many sources into one incident (e.g. many failures → success → privilege escalation → data exfiltration).
- **SIEM** tools: Splunk, ELK (Elasticsearch-Logstash-Kibana), IBM QRadar, Wazuh. Time synchronization (NTP) is essential.

**Wi-Fi attacks (A5)**: brute-forcing the WPA2 PSK, deauthentication (DoS) flood, evil twin / rogue AP, MAC spoofing, KRACK. Prevention: WPA3, strong passphrase, 802.1X/RADIUS, 802.11w (protected management frames), WIDS/WIPS, MAC filtering, lockout. Tools: Aircrack-ng, Kismet.

**Wireshark / Snort (A6)**: Wireshark = packet analyzer (passive). Snort = signature-based NIDS/NIPS (Cisco). IDS detects, IPS also blocks. Signature-based vs anomaly-based detection. False positive vs false negative.

**General**: CIA triad. Digital forensics process: Identification → Preservation → Collection → Examination → Analysis → Reporting. Locard's exchange principle. Volatile data first (order of volatility: registers/cache → RAM → network state → disk). IT Act 2000 (India), Sections 43, 66, 66C (identity theft), 66D (cheating by impersonation).

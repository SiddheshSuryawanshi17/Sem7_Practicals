# CSDF Assignment 3
# Write a computer forensic application program in Java/Python/C++ for
# Recovering Deleted Files and Deleted Partitions.
#
# Technique 1: File carving - scan raw bytes for file signatures (magic numbers:
#              header ... footer) and rebuild files even when the file-system entry is gone.
# Technique 2: Partition table analysis - read the MBR, list partitions and flag
#              deleted / empty / suspicious entries whose data may still exist.
#
# Run:  python make_test_image.py          (creates demo disk.img)
#       python recover_deleted.py disk.img
# On a real USB (Linux, as root):  python recover_deleted.py /dev/sdb
import hashlib
import os
import struct
import sys

SIGNATURES = {
    "jpg": (b"\xff\xd8\xff", b"\xff\xd9"),
    "png": (b"\x89PNG\r\n\x1a\n", b"IEND\xaeB`\x82"),
    "pdf": (b"%PDF", b"%%EOF"),
    "gif": (b"GIF89a", b"\x00\x3b"),
    "zip": (b"PK\x03\x04", b"PK\x05\x06"),
}
MAX_FILE = 10 * 1024 * 1024

PARTITION_TYPES = {0x00: "Empty / Deleted", 0x07: "NTFS / exFAT", 0x0B: "FAT32 (CHS)", 0x0C: "FAT32 (LBA)",
                   0x83: "Linux ext", 0x82: "Linux swap", 0x05: "Extended", 0x0F: "Extended (LBA)", 0xEE: "GPT protective"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def analyze_partitions(data):
    print("=" * 70)
    print("PARTITION TABLE ANALYSIS (MBR)")
    print("=" * 70)
    if data[510:512] != b"\x55\xaa":
        print("No valid MBR signature (0x55AA) found.")
        return
    if data[512:520] == b"EFI PART":
        print("GPT disk detected (EFI PART header at LBA 1).")
    print(f"{'#':<3}{'Boot':<6}{'Type':<6}{'Description':<18}{'Start LBA':>10}{'Sectors':>10}  Status")
    for i in range(4):
        e = data[446 + i * 16: 446 + (i + 1) * 16]
        boot, ptype, start, sectors = e[0], e[4], struct.unpack("<I", e[8:12])[0], struct.unpack("<I", e[12:16])[0]
        if ptype == 0 and start == 0 and sectors == 0:
            status = "unused slot"
        elif ptype == 0:
            status = "DELETED partition - data still present, recoverable!"
        elif sectors == 0:
            status = "SUSPICIOUS (size 0 - possibly tampered)"
        else:
            status = "active" if boot == 0x80 else "valid"
        print(f"{i + 1:<3}{hex(boot):<6}{hex(ptype):<6}{PARTITION_TYPES.get(ptype, 'Unknown'):<18}{start:>10}{sectors:>10}  {status}")


def carve_files(data, out_dir):
    print("\n" + "=" * 70)
    print("FILE CARVING (recovering deleted files by signature)")
    print("=" * 70)
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for ext, (header, footer) in SIGNATURES.items():
        pos = data.find(header)
        while pos != -1:
            end = data.find(footer, pos + len(header), pos + MAX_FILE)
            if end != -1:
                end += len(footer)
                blob = data[pos:end]
                count += 1
                name = os.path.join(out_dir, f"recovered_{count}.{ext}")
                with open(name, "wb") as f:
                    f.write(blob)
                print(f"[+] {ext.upper():4} offset {pos:>8}  size {len(blob):>7} B  -> {name}")
                print(f"    SHA-256: {sha256(blob)}")
                pos = data.find(header, end)
            else:
                pos = data.find(header, pos + 1)
    print(f"\nTotal files recovered: {count}  (saved in '{out_dir}/')")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "disk.img"
    with open(src, "rb") as f:
        raw = f.read()
    print(f"Evidence source : {src}")
    print(f"Size            : {len(raw)} bytes")
    print(f"SHA-256 (image) : {sha256(raw)}   <- record for chain of custody\n")
    analyze_partitions(raw)
    carve_files(raw, "recovered_files")

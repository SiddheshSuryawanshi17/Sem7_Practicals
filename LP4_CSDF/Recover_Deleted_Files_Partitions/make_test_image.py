# CSDF Assignment 3 - helper
# Creates a small fake disk image (disk.img) for the recovery demo:
#  - an MBR partition table with 2 partitions (one marked as "deleted": type 0x00)
#  - JPEG, PNG and PDF files written into the data area with NO file system entry
#    (exactly what remains on disk after a file is deleted and the index is wiped)
#
# Run: python make_test_image.py
import os
import struct
import zlib


def make_png():
    def chunk(t, data):
        return struct.pack(">I", len(data)) + t + data + struct.pack(">I", zlib.crc32(t + data) & 0xffffffff)
    w, h = 8, 8
    raw = b"".join(b"\x00" + bytes([255, 0, 0] * w) for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def make_jpeg():
    # minimal JPEG-like blob: SOI + APP0(JFIF) + some data + EOI
    return b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00" + os.urandom(400).replace(b"\xff\xd9", b"\x00\x00") + b"\xff\xd9"


def make_pdf():
    return (b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Count 0/Kids[]>>endobj\n"
            b"%% Secret evidence: bank account 1234-5678\ntrailer<</Root 1 0 R>>\n%%EOF")


def partition_entry(boot, ptype, lba_start, sectors):
    return struct.pack("<B3sB3sII", boot, b"\x00\x00\x00", ptype, b"\x00\x00\x00", lba_start, sectors)


if __name__ == "__main__":
    size = 1024 * 1024  # 1 MB image
    disk = bytearray(size)  # zero-filled unallocated space

    # MBR (sector 0)
    mbr = bytearray(512)
    mbr[446:462] = partition_entry(0x80, 0x07, 4, 800)      # NTFS, active
    mbr[462:478] = partition_entry(0x00, 0x00, 1000, 1000)                    # deleted entry (type 0) but data remains
    mbr[478:494] = partition_entry(0x00, 0x0B, 2100, 0)                       # FAT32, size 0 -> suspicious
    mbr[510:512] = b"\x55\xaa"
    disk[0:512] = mbr

    files = [("photo.jpg", make_jpeg(), 50_000), ("image.png", make_png(), 200_000), ("evidence.pdf", make_pdf(), 600_000)]
    for name, data, offset in files:
        disk[offset:offset + len(data)] = data
        print(f"Hidden {name:13} ({len(data)} bytes) at offset {offset}")

    with open("disk.img", "wb") as f:
        f.write(disk)
    print("\nCreated disk.img (1 MB). Now run: python recover_deleted.py disk.img")

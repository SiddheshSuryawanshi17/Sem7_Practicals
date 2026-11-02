# DAA Assignment 2
# Write a program to implement Huffman Encoding using a greedy strategy.
# Run: python huffman.py
import heapq
from collections import Counter


class Node:
    def __init__(self, freq, ch, left=None, right=None):
        self.freq = freq
        self.ch = ch
        self.left = left
        self.right = right

    def __lt__(self, other):  # heapq needs this to compare nodes
        return self.freq < other.freq


def build_codes(node, code, codes):
    if node is None:
        return
    if node.left is None and node.right is None:  # leaf
        codes[node.ch] = code or "0"
        return
    build_codes(node.left, code + "0", codes)
    build_codes(node.right, code + "1", codes)


if __name__ == "__main__":
    text = input("Enter text to encode: ")
    freq = Counter(text)

    heap = [Node(f, c) for c, f in freq.items()]
    heapq.heapify(heap)

    # Greedy: always merge the two least frequent nodes
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, Node(left.freq + right.freq, left.ch + right.ch, left, right))

    codes = {}
    build_codes(heap[0], "", codes)

    print("\nChar\tFreq\tCode")
    for ch in sorted(codes):
        print(f"'{ch}'\t{freq[ch]}\t{codes[ch]}")

    encoded = "".join(codes[c] for c in text)
    print("\nEncoded string :", encoded)
    print("Original size  :", len(text) * 8, "bits")
    print("Encoded size   :", len(encoded), "bits")
    print("\nTime Complexity : O(n log n), n = number of unique characters")
    print("Space Complexity: O(n)")

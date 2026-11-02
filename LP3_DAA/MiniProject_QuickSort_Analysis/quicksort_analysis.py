# DAA Mini Project
# Write a program for analysis of quick sort by using deterministic and
# randomized variant.
# Run: python quicksort_analysis.py
import random
import sys
import time

sys.setrecursionlimit(20000)
comparisons = 0


def partition(a, low, high):
    global comparisons
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        comparisons += 1
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


def quick_sort(a, low, high):  # deterministic: last element pivot
    if low < high:
        p = partition(a, low, high)
        quick_sort(a, low, p - 1)
        quick_sort(a, p + 1, high)


def randomized_quick_sort(a, low, high):  # random pivot
    if low < high:
        r = random.randint(low, high)
        a[r], a[high] = a[high], a[r]
        p = partition(a, low, high)
        randomized_quick_sort(a, low, p - 1)
        randomized_quick_sort(a, p + 1, high)


def measure(sort_fn, data):
    global comparisons
    comparisons = 0
    arr = data[:]
    start = time.perf_counter()
    sort_fn(arr, 0, len(arr) - 1)
    return comparisons, (time.perf_counter() - start) * 1000


if __name__ == "__main__":
    arr = list(map(int, input("Enter elements separated by space: ").split()))
    a, b = arr[:], arr[:]
    quick_sort(a, 0, len(a) - 1)
    randomized_quick_sort(b, 0, len(b) - 1)
    print("Sorted (deterministic):", a)
    print("Sorted (randomized)   :", b)

    N = 2000
    tests = {
        "Random input": [random.randint(0, 100000) for _ in range(N)],
        "Sorted input (worst case for deterministic)": list(range(N)),
        "Reverse sorted input": list(range(N, 0, -1)),
    }
    print(f"\n===== Performance Analysis (N = {N}) =====")
    print(f"{'Input':45} {'Det. comps':>12} {'Det. ms':>9} {'Rand. comps':>12} {'Rand. ms':>9}")
    for name, data in tests.items():
        dc, dt = measure(quick_sort, data)
        rc, rt = measure(randomized_quick_sort, data)
        print(f"{name:45} {dc:>12} {dt:>9.2f} {rc:>12} {rt:>9.2f}")

    print("\nConclusion:")
    print("  Deterministic: Best/Avg O(n log n), Worst O(n^2) on sorted/reverse input.")
    print("  Randomized   : Expected O(n log n) for every input; worst case is very unlikely.")
    print("  Space        : O(log n) average recursion stack.")

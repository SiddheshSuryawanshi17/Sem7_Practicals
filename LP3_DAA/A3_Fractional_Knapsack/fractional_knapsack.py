# DAA Assignment 3
# Write a program to solve a fractional Knapsack problem using a greedy method.
# Run: python fractional_knapsack.py


def fractional_knapsack(values, weights, capacity):
    items = sorted(zip(values, weights, range(1, len(values) + 1)),
                   key=lambda x: x[0] / x[1], reverse=True)  # greedy: best ratio first
    total = 0.0
    print("\nItem\tValue\tWeight\tRatio\tFraction taken")
    for v, w, idx in items:
        if capacity <= 0:
            frac = 0
        elif w <= capacity:
            frac = 1
        else:
            frac = capacity / w
        total += v * frac
        capacity -= w * frac
        print(f"{idx}\t{v}\t{w}\t{v / w:.2f}\t{frac:.2f}")
    return total


if __name__ == "__main__":
    n = int(input("Enter number of items: "))
    values, weights = [], []
    for i in range(n):
        v, w = map(float, input(f"Enter value and weight of item {i + 1}: ").split())
        values.append(v)
        weights.append(w)
    capacity = float(input("Enter knapsack capacity: "))

    print("\nMaximum value in knapsack =", fractional_knapsack(values, weights, capacity))
    print("\nTime Complexity : O(n log n) (sorting)")
    print("Space Complexity: O(n)")

# Sample input: 3 items -> (60 10) (100 20) (120 30), capacity 50  => answer 240

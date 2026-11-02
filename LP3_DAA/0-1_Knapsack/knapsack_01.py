# DAA Assignment 4
# Write a program to solve a 0-1 Knapsack problem using dynamic programming
# or branch and bound strategy.   (Dynamic Programming used here)
# Run: python knapsack_01.py


def knapsack(values, weights, W):
    n = len(values)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]  # skip item i
            if weights[i - 1] <= w:  # take item i
                dp[i][w] = max(dp[i][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])

    # Backtrack for selected items
    selected, w = [], W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i)
            w -= weights[i - 1]
    return dp, dp[n][W], selected[::-1]


if __name__ == "__main__":
    n = int(input("Enter number of items: "))
    values, weights = [], []
    for i in range(n):
        v, w = map(int, input(f"Enter value and weight of item {i + 1}: ").split())
        values.append(v)
        weights.append(w)
    W = int(input("Enter knapsack capacity: "))

    dp, best, selected = knapsack(values, weights, W)
    print("\nDP Table:")
    for row in dp:
        print("\t".join(map(str, row)))
    print("\nItems selected:", selected)
    print("Maximum profit =", best)
    print("\nTime Complexity : O(n * W)")
    print("Space Complexity: O(n * W)")

# Sample input: 4 items -> (3 2) (7 2) (2 4) (9 5), capacity 10  => answer 19

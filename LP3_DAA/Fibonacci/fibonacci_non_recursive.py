# DAA Assignment 1 (Non-recursive / Iterative version)
# Write a non-recursive program to calculate Fibonacci numbers
# and analyze its time and space complexity.
# Run: python fibonacci_non_recursive.py


def fib(n):
    """Iterative Fibonacci.  Time O(n), Space O(1).
    Returns (F(n), number of loop iterations)."""
    steps = 0
    a, b = 0, 1                     # F(0), F(1)
    for _ in range(n):
        a, b = b, a + b             # slide the pair forward by one position
        steps += 1
    return a, steps


if __name__ == "__main__":
    n = int(input("Enter n: "))

    print("\nFibonacci series (non-recursive):", *[fib(i)[0] for i in range(n)])

    result, steps = fib(n)
    print(f"\nF({n}) using non-recursion = {result}")
    print(f"Steps (loop iterations)    : {steps}")

    print("\nComplexity Analysis (Non-recursive):")
    print("  Time  : O(n)  - the loop runs n times")
    print("  Space : O(1)  - only a few variables, no stack growth")

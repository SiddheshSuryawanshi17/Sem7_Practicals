# DAA Assignment 1 (Recursive version)
# Write a recursive program to calculate Fibonacci numbers
# and analyze its time and space complexity.
# Run: python fibonacci_recursive.py

calls = 0   # counts recursive calls (used for the step analysis)


def fib(n):
    """Recursive Fibonacci.  Time O(2^n), Space O(n) (recursion stack depth)."""
    global calls
    calls += 1
    if n <= 1:                      # base cases: F(0) = 0, F(1) = 1
        return n
    return fib(n - 1) + fib(n - 2)  # F(n) = F(n-1) + F(n-2)


if __name__ == "__main__":
    n = int(input("Enter n: "))

    print("\nFibonacci series (recursive):", *[fib(i) for i in range(n)])

    calls = 0
    result = fib(n)
    print(f"\nF({n}) using recursion = {result}")
    print(f"Steps (recursive calls) : {calls}")

    print("\nComplexity Analysis (Recursive):")
    print("  Time  : O(2^n)  - every call makes two more calls, so the calls double")
    print("  Space : O(n)    - maximum depth of the recursion stack is n")

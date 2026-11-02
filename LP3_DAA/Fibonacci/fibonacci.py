# DAA Assignment 1
# Write a non-recursive and recursive program to calculate Fibonacci numbers
# and analyze their time and space complexity.
# Run: python fibonacci.py

rec_steps = 0


def fib_recursive(n):
    """Time O(2^n), Space O(n) for recursion stack."""
    global rec_steps
    rec_steps += 1
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    """Time O(n), Space O(1)."""
    steps = 0
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
        steps += 1
    return a, steps


if __name__ == "__main__":
    n = int(input("Enter n: "))

    series = [fib_iterative(i)[0] for i in range(n)]
    print("\nFibonacci series:", *series)

    r = fib_recursive(n)
    i, it_steps = fib_iterative(n)
    print(f"\nF({n}) using recursion     = {r}")
    print(f"F({n}) using non-recursion = {i}")
    print(f"\nSteps (recursive calls)     : {rec_steps}")
    print(f"Steps (iterative loop runs) : {it_steps}")

    print("\nComplexity Analysis:")
    print("  Recursive     -> Time O(2^n), Space O(n) (recursion stack)")
    print("  Non-recursive -> Time O(n),   Space O(1)")

# LP-III : Design and Analysis of Algorithms (DAA)

Every assignment has a **C++** and a **Python** version (use whichever the examiner wants) plus `sample_output.txt`.

| # | Problem statement | Folder | Sample input |
|---|---|---|---|
| 1 | Non-recursive and recursive program to calculate Fibonacci numbers and analyze their time and space complexity | `A1_Fibonacci` | `10` |
| 2 | Huffman Encoding using a greedy strategy | `A2_Huffman_Encoding` | `abracadabra` |
| 3 | Fractional Knapsack using a greedy method | `A3_Fractional_Knapsack` | 3 items: `60 10`, `100 20`, `120 30`, cap `50` → **240** |
| 4 | 0-1 Knapsack using dynamic programming (or branch & bound) | `A4_0-1_Knapsack` | 4 items: `3 2`, `7 2`, `2 4`, `9 5`, cap `10` → **19** |
| 5 | n-Queens matrix with first Queen placed; backtracking places the rest | `A5_N_Queens` | n=`8`, first col=`0` |
| 6 | Mini project: analysis of Quick Sort, deterministic vs randomized | `A6_MiniProject_QuickSort_Analysis` | `8` then `23 34 54 123 34 56 676 112` |

## How to run
```bash
# C++  (Windows: use  name.exe  instead of ./name)
g++ fibonacci.cpp -o fib
./fib

# Python
python fibonacci.py
```
No g++ on the lab PC? Use an online compiler (onlinegdb.com) or run the Python version.

## Complexity table (memorize)
| Algorithm | Strategy | Time | Space |
|---|---|---|---|
| Fibonacci recursive | Divide & conquer (overlapping subproblems) | O(2ⁿ) (≈ O(φⁿ), φ=1.618) | O(n) stack |
| Fibonacci iterative | Bottom-up | O(n) | O(1) |
| Huffman coding | Greedy (min-heap) | O(n log n) | O(n) |
| Fractional knapsack | Greedy (value/weight ratio) | O(n log n) | O(1) |
| 0-1 knapsack | Dynamic programming | O(n·W) (pseudo-polynomial) | O(n·W) |
| 0-1 knapsack | Branch & bound | O(2ⁿ) worst | O(n) |
| N-Queens | Backtracking | O(n!) | O(n²) |
| Quick sort (deterministic) | Divide & conquer | Best/Avg O(n log n), Worst O(n²) (sorted input) | O(log n) |
| Randomized quick sort | Divide & conquer + random pivot | Expected O(n log n) for all inputs | O(log n) |

## Viva quick answers
- **Greedy vs DP:** greedy makes the locally best choice and never revisits it (fast, but not always optimal). DP solves overlapping subproblems once and stores results (optimal substructure + overlapping subproblems).
- **Why greedy fails for 0-1 knapsack:** items can't be split. Example: cap 50, items (60,10) (100,20) (120,30). Greedy by ratio gives 160, but optimal is 220.
- **Huffman:** prefix-free variable-length codes, so frequent characters get shorter codes. Optimal for symbol-by-symbol coding. Uses a min-heap/priority queue.
- **Backtracking:** build a solution step by step and abandon (backtrack) as soon as a constraint fails. N-Queens checks column and both diagonals.
- **Branch & bound:** like backtracking, but uses bounds to prune branches that cannot beat the best solution so far (used for optimization problems).
- **Memoization** = top-down DP (recursion + cache). **Tabulation** = bottom-up DP (table).
- **Randomized algorithms:** Las Vegas (always correct, random time, e.g. randomized quicksort) vs Monte Carlo (fixed time, may be wrong).
- **Recurrence of quicksort:** best T(n)=2T(n/2)+n → O(n log n). Worst T(n)=T(n-1)+n → O(n²).
- **Master theorem:** T(n)=aT(n/b)+f(n).

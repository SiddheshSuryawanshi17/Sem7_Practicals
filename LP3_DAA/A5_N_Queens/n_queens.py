# DAA Assignment 5
# Design n-Queens matrix having first Queen placed. Use backtracking to place
# remaining Queens to generate the final n-queen's matrix.
# Run: python n_queens.py


def is_safe(board, row, col, n):
    for i in range(row):  # column
        if board[i][col]:
            return False
    i, j = row - 1, col - 1  # upper-left diagonal
    while i >= 0 and j >= 0:
        if board[i][j]:
            return False
        i, j = i - 1, j - 1
    i, j = row - 1, col + 1  # upper-right diagonal
    while i >= 0 and j < n:
        if board[i][j]:
            return False
        i, j = i - 1, j + 1
    return True


def solve(board, row, n):
    if row == n:
        return True
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1  # place
            if solve(board, row + 1, n):
                return True
            board[row][col] = 0  # backtrack
    return False


def print_board(board):
    for r in board:
        print(" ".join("Q" if c else "." for c in r))


if __name__ == "__main__":
    n = int(input("Enter n (board size): "))
    first_col = int(input(f"Enter column (0 to {n - 1}) of first queen in row 0: "))

    board = [[0] * n for _ in range(n)]
    board[0][first_col] = 1  # first queen already placed

    print("\nInitial board (first queen placed):")
    print_board(board)

    if solve(board, 1, n):
        print(f"\nFinal {n}-Queens matrix:")
        print_board(board)
        print("\nMatrix form:")
        for r in board:
            print(*r)
    else:
        print(f"\nNo solution exists with first queen at column {first_col}")

    print("\nTime Complexity : O(n!)")
    print("Space Complexity: O(n^2) board + O(n) recursion stack")

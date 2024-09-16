def print_board(board):
    """Print the Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def find_empty_location(board):
    """Find an empty location in the board."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    # Check if num is not in the current row
    if num in board[row]:
        return False

    # Check if num is not in the current column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check if num is not in the 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):
    """Solve the Sudoku puzzle using backtracking."""
    empty = find_empty_location(board)
    if not empty:
        return True  # Puzzle solved

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            # Reset if num doesn't lead to a solution
            board[row][col] = 0

    return False

def input_board():
    """Input the Sudoku board from the user."""
    print("Enter the Sudoku board (9 lines of 9 digits, use 0 for empty cells):")
    board = []
    for _ in range(9):
        while True:
            try:
                line = input().strip()
                row = [int(num) for num in line.split()]
                if len(row) != 9:
                    raise ValueError("Each row must have exactly 9 numbers.")
                board.append(row)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter the row again.")
    return board

def main():
    # Input the Sudoku board
    board = input_board()

    print("\nOriginal Sudoku:")
    print_board(board)

    if solve_sudoku(board):
        print("\nSolved Sudoku:")
        print_board(board)
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()

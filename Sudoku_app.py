import streamlit as st 
import numpy as np

class Sudoku:
    def printsudoku(self, sudokuboard):
        for row in sudokuboard:
            print(" ".join(str(num) for num in row))
    
    def sudokusolver(self, sudokuboard, row, col):
        if row == 9:
            return True
        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)
        if sudokuboard[row][col] != 0:
            return self.sudokusolver(sudokuboard, next_row, next_col)
        for d in range(1, 10):
            if self.safe(sudokuboard, row, col, d):
                sudokuboard[row][col] = d
                if self.sudokusolver(sudokuboard, next_row, next_col):
                    return True
                sudokuboard[row][col] = 0
        return False

    def safe(self, sudokuboard, row, col, d):
        if d in sudokuboard[row]:  # Row check
            return False
        if d in [sudokuboard[i][col] for i in range(9)]:  # Column check
            return False
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if sudokuboard[i][j] == d:
                    return False
        return True

    def main(self, sudokuboard):
        self.printsudoku(sudokuboard)
        if self.sudokusolver(sudokuboard, 0, 0):
            print("Solution exists")
            self.printsudoku(sudokuboard)
        else:
            print("No solution exists")

# Streamlit UI
st.title("Sudoku Solver")
st.write("### Enter Sudoku Grid (Use 0 for empty cells)")

# Initialize a 9x9 Sudoku board
sudoku_board = []
for i in range(9):
    row = []
    cols = st.columns(9)
    for j in range(9):
        value = cols[j].number_input(f"{i+1},{j+1}", min_value=0, max_value=9, value=0, key=f"cell_{i}_{j}")
        row.append(int(value))
    sudoku_board.append(row)

# Convert to numpy array for processing
sudoku_board = np.array(sudoku_board)

# Button to solve Sudoku
if st.button("Solve Sudoku"):
    sudoku_solver = Sudoku()
    sudoku_board_list = sudoku_board.tolist()  # Convert to Python list

    st.write("### Original Sudoku Board:")
    st.text("\n".join(" ".join(str(num) for num in row) for row in sudoku_board_list))

    # Solve Sudoku
    if sudoku_solver.sudokusolver(sudoku_board_list, 0, 0):
        st.write("### Solved Sudoku Board:")
        st.text("\n".join(" ".join(str(num) for num in row) for row in sudoku_board_list))
    else:
        st.write("No solution exists for the given board.")
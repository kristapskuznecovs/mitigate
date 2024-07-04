import random #randomisation module

class mitigateGame:
    def __init__(self, board_size, numbers): #constructor method to initialize the newly created object by setting initial values for its attributes.  It is called automatically when you create a new instance of the class.
        self.board_size = board_size
        self.numbers = numbers
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.score = 0

    def display_board(self): 
        for row in self.board:
            formatted_row = []
            for cell in row:
                formatted_cell = f"[{cell:^3}]"  # Centered, with brackets
                formatted_row.append(formatted_cell)
            print(' '.join(formatted_row))
        print(f"Score: {self.score}")

    def place_number(self, num, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = num
            return True
        else:
            print("The cell is not empty. Try again.")
            return False

    def generate_random_numbers(self):
        empty_cells = [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r][c] == ' ']
        if len(empty_cells) < 3:
            return False

        for _ in range(3):
            row, col = random.choice(empty_cells)
            self.board[row][col] = random.choice(self.numbers)
            empty_cells.remove((row, col))
        return True

    def check_lines(self):
        def is_line(cells):
            first_value = self.board[cells[0][0]][cells[0][1]]
            if all(self.board[r][c] == first_value != ' ' for r, c in cells):
                for r, c in cells:
                    self.board[r][c] = ' '
                return True
            return False

        def has_matching_line(r, c):
            directions = [
                [(r + i, c) for i in range(3)],      # Horizontal
                [(r, c + i) for i in range(3)],      # Vertical
                [(r + i, c + i) for i in range(3)],  # Diagonal \
                [(r + i, c - i) for i in range(3)]   # Diagonal /
            ]
            for direction in directions:
                if all(0 <= nr < self.board_size and 0 <= nc < self.board_size for nr, nc in direction):
                    if is_line(direction):
                        return True
            return False
        
        def extend_line(r, c, dr, dc):
            value = self.board[r][c]
            line_cells = [(r, c)]
            nr, nc = r + dr, c + dc
            while 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr][nc] == value:
                line_cells.append((nr, nc))
                nr += dr
                nc += dc
            return line_cells if len(line_cells) >= 3 else []

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] != ' ':
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        line_cells = extend_line(r, c, dr, dc)
                        if line_cells:
                            for cell in line_cells:
                                self.board[cell[0]][cell[1]] = ' '
                            self.score += len(line_cells)*100
                            return True
        return False

    def is_board_full(self):
        return all(self.board[r][c] != ' ' for r in range(self.board_size) for c in range(self.board_size))

    def play(self):
        print("Welcome to Popping numbers!")
        while True:
            self.display_board()

        # Get valid number input
            while True:
                try:
                    num_str = input(f"Enter the number to place ({', '.join(map(str, self.numbers))}): ")
                    num = int(num_str)
                    if num not in self.numbers:
                        print(f"Invalid number. Choose from {', '.join(map(str, self.numbers))}.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # Get valid row and column input
            while True:
                try:
                    row_str = input(f"Enter the row (0-{self.board_size-1}): ")
                    row = int(row_str)
                    col_str = input(f"Enter the column (0-{self.board_size-1}): ")
                    col = int(col_str)
                    if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                        print(f"Invalid position. Choose row and column between 0 and {self.board_size-1}.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter numbers for row and column.")

            if self.place_number(num, row, col):
                while self.check_lines():
                 pass

                if not self.generate_random_numbers():
                    print("No more space to place numbers. Game over!")
                    break

            while self.check_lines():
                pass

            if self.is_board_full():
                print("Board is full. Game over!")
                break

        print(f"Your final score: {self.score}")

def main():
    while True:
        try:
            board_size = int(input("Enter the board size (5-25): "))
            if 5 <= board_size <= 25:
                break
            else:
                print("Invalid board size. Please enter a number between 5 and 25.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        numbers_input = input("Enter the numbers to use (choose from 0-9, e.g., 123 for numbers 1, 2, and 3): ")
        if all(ch in '0123456789' for ch in numbers_input) and numbers_input:
            numbers = list(map(int, numbers_input))
            break
        else:
            print("Invalid numbers. Please enter a string of digits between 0 and 9.")

    game = mitigateGame(board_size, numbers)
    game.play()

if __name__ == "__main__":
    main()

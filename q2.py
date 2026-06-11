def next_letter(letter):
    # Go back to a after z
    if letter == "z":
        return "a"
    else:
        return chr(ord(letter) + 1)


def make_grid(rows, cols):
    # Create an empty grid filled with spaces
    grid = []

    for i in range(rows):
        row = []

        for j in range(cols):
            row.append(" ")

        grid.append(row)

    return grid


def fill_pattern(grid, row, col, direction, letter, remaining):
    # Stop when all letters have been placed
    if remaining == 0:
        return

    grid[row][col] = letter
    letter = next_letter(letter)

    # Move upwards through the rows
    if direction == "up":
        if row == 0:
            fill_pattern(grid, row, col + 1, "down", letter, remaining - 1)
        else:
            fill_pattern(grid, row - 1, col + 1, "up", letter, remaining - 1)

    # Move downwards through the rows
    else:
        if row == len(grid) - 1:
            fill_pattern(grid, row, col + 1, "up", letter, remaining - 1)
        else:
            fill_pattern(grid, row + 1, col + 1, "down", letter, remaining - 1)


def print_grid(grid):
    # Print each row of the grid
    for row in grid:
        for letter in row:
            print(letter, end=" ")
        print()


rows = int(input("rows: "))
cycles = int(input("cycles: "))

# This gives enough columns to hold the full pattern
letters_per_cycle = rows * (rows + 1) // 2
total_letters = letters_per_cycle * cycles

grid = make_grid(rows, total_letters)

# Start from the bottom row and move upwards first
fill_pattern(grid, rows - 1, 0, "up", "a", total_letters)

print_grid(grid)

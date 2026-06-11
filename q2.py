def next_letter(letter):
    if letter == "z":
        return "a"
    else:
        return chr(ord(letter) + 1)


def make_grid(rows, cols):
    grid = []

    for i in range(rows):
        row = []

        for j in range(cols):
            row.append(" ")

        grid.append(row)

    return grid


def fill_pattern(grid, row, col, direction, letter, remaining):
    if remaining == 0:
        return

    grid[row][col] = letter
    letter = next_letter(letter)

    if direction == "up":
        if row == 0:
            fill_pattern(grid, row, col + 1, "down", letter, remaining - 1)
        else:
            fill_pattern(grid, row - 1, col + 1, "up", letter, remaining - 1)
    else:
        if row == len(grid) - 1:
            fill_pattern(grid, row, col + 1, "up", letter, remaining - 1)
        else:
            fill_pattern(grid, row + 1, col + 1, "down", letter, remaining - 1)


def print_grid(grid):
    for row in grid:
        for letter in row:
            print(letter, end=" ")
        print()


rows = int(input("rows: "))
cycles = int(input("cycles: "))

letters_per_cycle = rows * (rows + 1) // 2
total_letters = letters_per_cycle * cycles

grid = make_grid(rows, total_letters)

fill_pattern(grid, rows - 1, 0, "up", "a", total_letters)

print_grid(grid)

def next_letter(letter):
    if letter == "z":
        return "a"
    return chr(ord(letter) + 1)


def make_grid(rows, cols):
    if rows == 0:
        return []
    return [[" " for _ in range(cols)]] + make_grid(rows - 1, cols)


def fill_pattern(grid, row, col, direction, letter, count):
    if count == 0:
        return

    grid[row][col] = letter
    letter = next_letter(letter)

    if direction == "up":
        if row == 0:
            fill_pattern(grid, row, col + 1, "down", letter, count - 1)
        else:
            fill_pattern(grid, row - 1, col + 1, "up", letter, count - 1)

    else:
        if row == len(grid) - 1:
            fill_pattern(grid, row, col + 1, "up", letter, count - 1)
        else:
            fill_pattern(grid, row + 1, col + 1, "down", letter, count - 1)


def print_rows(grid, row):
    if row == len(grid):
        return

    line = ""

    for char in grid[row]:
        line += char + " "

    print(line.rstrip())
    print_rows(grid, row + 1)


def main():
    rows = int(input("rows: "))
    cycles = int(input("cycles: "))

    letters_per_cycle = rows * (rows + 1) // 2
    total_letters = letters_per_cycle * cycles

    grid = make_grid(rows, total_letters)

    fill_pattern(grid, rows - 1, 0, "up", "a", total_letters)

    print_rows(grid, 0)


main()

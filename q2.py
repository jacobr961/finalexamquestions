def get_next_letter(current_letter):
    # Start again from a, when it finishes with z
    if current_letter == "z":
        return "a"

    return chr(ord(current_letter) + 1)


def create_blank_pattern(rows, columns):
    # Having the blank pattern first
    pattern = []

    for row_number in range(rows):
        new_row = []

        for column_number in range(columns):
            new_row.append(" ")

        pattern.append(new_row)

    return pattern


def add_letters(pattern, row, column, going_up, letter, letters_left):
    # Base case 
    if letters_left == 0:
        return

    pattern[row][column] = letter
    letter = get_next_letter(letter)

    if going_up:
        if row == 0:
            add_letters(pattern, row, column + 1, False, letter, letters_left - 1)
        else:
            add_letters(pattern, row - 1, column + 1, True, letter, letters_left - 1)
    else:
        if row == len(pattern) - 1:
            add_letters(pattern, row, column + 1, True, letter, letters_left - 1)
        else:
            add_letters(pattern, row + 1, column + 1, False, letter, letters_left - 1)


def display_pattern(pattern):
    for row in pattern:
        for letter in row:
            print(letter, end=" ")
        print()


rows = int(input("rows: "))
cycles = int(input("cycles: "))

letters_in_one_cycle = rows * (rows + 1) // 2
total_letters = letters_in_one_cycle * cycles

pattern = create_blank_pattern(rows, total_letters)

# Start at the bottom row and move upwards
add_letters(pattern, rows - 1, 0, True, "a", total_letters)

display_pattern(pattern)

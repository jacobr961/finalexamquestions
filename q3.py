import cv2
import numpy as np


def shift_colour(value, shift):
    # Holds the colour value between 0 and 255
    return (value + shift) % 256


def undo_colour_shift(value, low_shift, high_shift):
    # Backwards rule for the low range first
    old_low_value = shift_colour(value, -low_shift)

    if old_low_value <= 127:
        return old_low_value

    # Backwards the high range rule, if it was not low
    old_high_value = shift_colour(value, -high_shift)
    return old_high_value


def encrypt_photo(photo, key1, key2):
    encrypted_photo = photo.copy()

    rows = photo.shape[0]
    columns = photo.shape[1]
    middle_row = (rows + 1) // 2

    for row in range(rows):
        for column in range(columns):
            blue = int(photo[row, column, 0])
            green = int(photo[row, column, 1])
            red = int(photo[row, column, 2])

            if row < middle_row:
                # Top half rules
                if blue <= 127:
                    blue = shift_colour(blue, key1 * key2)
                else:
                    blue = shift_colour(blue, -key1)

                if green <= 127:
                    green = shift_colour(green, -key2)
                else:
                    green = shift_colour(green, key1 + key2)

            else:
                # Bottom half rules
                if green <= 127:
                    green = shift_colour(green, key1 ** 2)
                else:
                    green = shift_colour(green, -(key1 * key2))

                if red <= 127:
                    red = shift_colour(red, -(key2 ** 2))
                else:
                    red = shift_colour(red, key2 ** 2)

            encrypted_photo[row, column] = [blue, green, red]

    return encrypted_photo


def decrypt_photo(photo, key1, key2):
    decrypted_photo = photo.copy()

    rows = photo.shape[0]
    columns = photo.shape[1]
    middle_row = (rows + 1) // 2

    for row in range(rows):
        for column in range(columns):
            blue = int(photo[row, column, 0])
            green = int(photo[row, column, 1])
            red = int(photo[row, column, 2])

            if row < middle_row:
                blue = undo_colour_shift(blue, key1 * key2, -key1)
                green = undo_colour_shift(green, -key2, key1 + key2)

            else:
                green = undo_colour_shift(green, key1 ** 2, -(key1 * key2))
                red = undo_colour_shift(red, -(key2 ** 2), key2 ** 2)

            decrypted_photo[row, column] = [blue, green, red]

    return decrypted_photo


def count_differences(original, decrypted):
    differences = 0

    rows = original.shape[0]
    columns = original.shape[1]
    channels = original.shape[2]

    for row in range(rows):
        for column in range(columns):
            for channel in range(channels):
                if original[row, column, channel] != decrypted[row, column, channel]:
                    differences += 1

    return differences


key1 = int(input("Enter key1: "))
key2 = int(input("Enter key2: "))

photo = cv2.imread("photo.jpg")

if photo is None:
    print("photo.jpg was not found")
else:
    encrypted = encrypt_photo(photo, key1, key2)
    decrypted = decrypt_photo(encrypted, key1, key2)

    cv2.imwrite("encrypted.png", encrypted)
    cv2.imwrite("decrypted.png", decrypted)

    difference = count_differences(photo, decrypted)

    if difference == 0:
        print("Decryption successful")
    else:
        print("Decryption failed:", difference, "pixels differ")

    # Having the three photos side by side
    combined = np.hstack((photo, encrypted, decrypted))
    cv2.imwrite("comparison.png", combined)

    print("Files saved")

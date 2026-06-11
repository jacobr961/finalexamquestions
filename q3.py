import cv2
import numpy as np


def change_value(value, amount):
    return (value + amount) % 256


def encrypt_image(image, key1, key2):
    encrypted = image.copy()

    rows = image.shape[0]
    cols = image.shape[1]

    middle = (rows + 1) // 2

    for i in range(rows):
        for j in range(cols):
            blue = int(image[i, j, 0])
            green = int(image[i, j, 1])
            red = int(image[i, j, 2])

            if i < middle:
                if blue <= 127:
                    blue = change_value(blue, key1 * key2)
                else:
                    blue = change_value(blue, -key1)

                if green <= 127:
                    green = change_value(green, -key2)
                else:
                    green = change_value(green, key1 + key2)

            else:
                if green <= 127:
                    green = change_value(green, key1 ** 2)
                else:
                    green = change_value(green, -(key1 * key2))

                if red <= 127:
                    red = change_value(red, -(key2 ** 2))
                else:
                    red = change_value(red, key2 ** 2)

            encrypted[i, j] = [blue, green, red]

    return encrypted


def decrypt_image(image, key1, key2):
    decrypted = image.copy()

    rows = image.shape[0]
    cols = image.shape[1]

    middle = (rows + 1) // 2

    for i in range(rows):
        for j in range(cols):
            blue = int(image[i, j, 0])
            green = int(image[i, j, 1])
            red = int(image[i, j, 2])

            if i < middle:
                if blue <= 127:
                    blue = change_value(blue, -(key1 * key2))
                else:
                    blue = change_value(blue, key1)

                if green <= 127:
                    green = change_value(green, key2)
                else:
                    green = change_value(green, -(key1 + key2))

            else:
                if green <= 127:
                    green = change_value(green, -(key1 ** 2))
                else:
                    green = change_value(green, key1 * key2)

                if red <= 127:
                    red = change_value(red, key2 ** 2)
                else:
                    red = change_value(red, -(key2 ** 2))

            decrypted[i, j] = [blue, green, red]

    return decrypted


def compare_images(original, decrypted):
    difference = 0

    rows = original.shape[0]
    cols = original.shape[1]
    channels = original.shape[2]

    for i in range(rows):
        for j in range(cols):
            for k in range(channels):
                if original[i, j, k] != decrypted[i, j, k]:
                    difference += 1

    return difference


key1 = int(input("Enter key1: "))
key2 = int(input("Enter key2: "))

photo = cv2.imread("photo.jpg")

if photo is None:
    print("Error: photo.jpg was not found.")
    print("Make sure photo.jpg is in the same folder as this Python file.")
else:
    encrypted = encrypt_image(photo, key1, key2)
    decrypted = decrypt_image(encrypted, key1, key2)

    cv2.imwrite("encrypted.png", encrypted)
    cv2.imwrite("decrypted.png", decrypted)

    different = compare_images(photo, decrypted)

    if different == 0:
        print("Decryption successful")
    else:
        print("Decryption failed:", different, "pixels differ")

    combined = np.hstack((photo, encrypted, decrypted))
    cv2.imwrite("comparison.png", combined)

    print("encrypted.png saved")
    print("decrypted.png saved")
    print("comparison.png saved")

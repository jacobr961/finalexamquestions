import cv2
import numpy as np


def move_value(value, amount):
    return (value + amount) % 256


def encrypt_pixel(pixel, row, middle, key1, key2):
    blue = int(pixel[0])
    green = int(pixel[1])
    red = int(pixel[2])

    if row < middle:
        # Top half
        if blue <= 127:
            blue = move_value(blue, key1 * key2)
        else:
            blue = move_value(blue, -key1)

        if green <= 127:
            green = move_value(green, -key2)
        else:
            green = move_value(green, key1 + key2)

        # Red is unchanged in top half

    else:
        # Bottom half
        # Blue is unchanged in bottom half

        if green <= 127:
            green = move_value(green, key1 ** 2)
        else:
            green = move_value(green, -(key1 * key2))

        if red <= 127:
            red = move_value(red, -(key2 ** 2))
        else:
            red = move_value(red, key2 ** 2)

    return [blue, green, red]


def decrypt_pixel(pixel, row, middle, key1, key2):
    blue = int(pixel[0])
    green = int(pixel[1])
    red = int(pixel[2])

    if row < middle:
        # Reverse top half changes
        if blue <= 127:
            blue = move_value(blue, -(key1 * key2))
        else:
            blue = move_value(blue, key1)

        if green <= 127:
            green = move_value(green, key2)
        else:
            green = move_value(green, -(key1 + key2))

    else:
        # Reverse bottom half changes
        if green <= 127:
            green = move_value(green, -(key1 ** 2))
        else:
            green = move_value(green, key1 * key2)

        if red <= 127:
            red = move_value(red, key2 ** 2)
        else:
            red = move_value(red, -(key2 ** 2))

    return [blue, green, red]


def encrypt_image(image, key1, key2):
    encrypted = image.copy()
    rows = image.shape[0]
    cols = image.shape[1]

    middle = (rows + 1) // 2

    for i in range(rows):
        for j in range(cols):
            encrypted[i, j] = encrypt_pixel(image[i, j], i, middle, key1, key2)

    return encrypted


def decrypt_image(image, key1, key2):
    decrypted = image.copy()
    rows = image.shape[0]
    cols = image.shape[1]

    middle = (rows + 1) // 2

    for i in range(rows):
        for j in range(cols):
            decrypted[i, j] = decrypt_pixel(image[i, j], i, middle, key1, key2)

    return decrypted


def compare_images(image1, image2):
    rows = image1.shape[0]
    cols = image1.shape[1]
    channels = image1.shape[2]

    different_pixels = 0

    for i in range(rows):
        for j in range(cols):
            for k in range(channels):
                if image1[i, j, k] != image2[i, j, k]:
                    different_pixels += 1

    return different_pixels


key1 = int(input("Enter key1: "))
key2 = int(input("Enter key2: "))

photo = cv2.imread("photo.jpg")

if photo is None:
    print("Could not find photo.jpg")
else:
    encrypted = encrypt_image(photo, key1, key2)
    cv2.imwrite("encrypted.jpg", encrypted)

    encrypted_photo = cv2.imread("encrypted.jpg")
    decrypted = decrypt_image(encrypted_photo, key1, key2)
    cv2.imwrite("decrypted.jpg", decrypted)

    decrypted_photo = cv2.imread("decrypted.jpg")

    different = compare_images(photo, decrypted_photo)

    if different == 0:
        print("Decryption successful")
    else:
        print("Decryption failed:", different, "pixels differ")

    # Add labels to each image
    photo_label = photo.copy()
    encrypted_label = encrypted.copy()
    decrypted_label = decrypted.copy()

    cv2.putText(photo_label, "Original", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.putText(encrypted_label, "Encrypted", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.putText(decrypted_label, "Decrypted", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    combined = np.hstack((photo_label, encrypted_label, decrypted_label))

    cv2.imshow("Original, Encrypted and Decrypted Images", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

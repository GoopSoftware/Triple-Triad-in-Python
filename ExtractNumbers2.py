import pytesseract
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Get image
image_path = 'downloaded_images/FFVIII_Caterchipillar_monster_card.png'
folder_path = 'downloaded_images'
counter = 0
total_accuracy = 0

for image_name in os.listdir(folder_path):
    files = os.path.join(folder_path, image_name)

    # Convert the image
    original_image = cv2.imread(files)
    cropped_image = original_image[4:52, 5:33]
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 220, 255, cv2.THRESH_BINARY)
    inverted_image = 255 - blackAndWhiteImage

    # Take the previous code and apply a variable for later code
    image_to_process = inverted_image

    # OCR the text
    text = pytesseract.image_to_string(image_to_process, config='--psm 10 --oem 3 -c tessedit_char_whitelist=A0123456789')
    counter += 1
    numbers = text
    print(f'{counter} Image: {image_name}'.strip('\n'))
    print("Extracted numbers:", numbers.strip('\n'))

    # Calculate accuracy
    extracted_numbers = [int(num) for num in numbers if num.isdigit()]
    accuracy = len(extracted_numbers)
    total_accuracy += accuracy

    # Save the image
    output_folder = 'bw_images'
    output_name = os.path.splitext(image_name)[0] + '_bw.png'
    output_path = os.path.join(output_folder, output_name)
    cv2.imwrite(output_path, image_to_process)

average_accuracy = total_accuracy / 440
average_accuracy = float(round(average_accuracy, 2))
print(f"Accuracy: {average_accuracy * 100}%")

# Show the image
plt.imshow(image_to_process, cmap='gray')
plt.axis('off')
plt.show()



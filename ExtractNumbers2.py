import pytesseract
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Get image
image_path = 'downloaded_images/FFVIII_Caterchipillar_monster_card.png'

# Convert the image



folder_path = 'downloaded_images'
for image_name in os.listdir(folder_path):
    files = os.path.join(folder_path, image_name)

    original_image = cv2.imread(files)
    cropped_image = original_image[4:52, 5:33]
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    inverted_image = 255 - blackAndWhiteImage

    image_to_process = inverted_image
    # OCR the text
    text = pytesseract.image_to_string(image_to_process,
                                       config='--psm 10 --oem 3 -c tessedit_char_whitelist=A0123456789')

    numbers = ''.join(filter(str.isdigit, text))
    print(f'Image: {image_name}')
    print("Extracted numbers:", numbers)

    # Save the image
    output_folder = 'bw_images'
    output_name = os.path.splitext(image_name)[0] + '_bw.png'
    output_path = os.path.join(output_folder, output_name)
    cv2.imwrite(output_path, image_to_process)

# Show the image
plt.imshow(image_to_process, cmap='gray')
plt.axis('off')
plt.show()



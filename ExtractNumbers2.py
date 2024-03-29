import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Todo Save the output into a notepad as soon as you decide the format


def split_image(image):
    # This function will split an image into thirds and return the 3 sections
    height, width = image.shape
    section_height = height // 3
    top_section = image[0:section_height, :]
    middle_section = image[section_height:2*section_height, :]
    bottom_section = image[2*section_height:3*section_height, :]
    return top_section, middle_section, bottom_section


# Get image from downloaded_images
#image_path = 'downloaded_images/FFVIII_Caterchipillar_monster_card.png'
folder_path = 'downloaded_images'
output_file_path = 'CardListValue.txt'

counter = 0
total_accuracy = 0


with open(output_file_path, 'w') as output_file:
    for image_name in os.listdir(folder_path):
        files = os.path.join(folder_path, image_name)

        # Convert the image
        original_image = cv2.imread(files)
        cropped_image = original_image[4:52, 5:33]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 220, 255, cv2.THRESH_BINARY)
        inverted_image = 255 - blackAndWhiteImage

        # Splits the cards into 3 sections
        top_section, middle_section, bottom_section = split_image(inverted_image)
        sections = [top_section, middle_section, bottom_section]
        extracted_numbers = []

        for i, section in enumerate(sections, start=1):
            # OCR the text
            text = pytesseract.image_to_string(section,
                                               config='--psm 10 --oem 3 -c '
                                                      'tessedit_char_whitelist=A0123456789')
            numbers = ''.join(filter(lambda char: char.isdigit() or char == 'A', text))
            extracted_numbers.extend(numbers)

            # Save the image
            output_folder = 'bw_images'
            output_name = os.path.splitext(image_name)[0] + f'_{i}_bw.png'
            output_path = os.path.join(output_folder, output_name)
            cv2.imwrite(output_path, section)

        counter += 1

        card_name = os.path.splitext(image_name)[0]
        output_line = f"{card_name}, {' '.join(extracted_numbers)}\n"
        output_file.write(output_line)


        # Calculate accuracy
        accuracy = len(extracted_numbers)
        total_accuracy += accuracy

# Print accuracy
average_accuracy = total_accuracy / 440
average_accuracy = round(average_accuracy, 2)
print(f"Accuracy: {average_accuracy * 100}%")

# Show the image
#plt.imshow(image_to_process, cmap='gray')
#plt.axis('off')
#plt.show()

if __name__ == '__main__':
    print('Numbers finished extracting')
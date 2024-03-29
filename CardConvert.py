from PIL import Image
import os


def change_blue_to_red(image_path, output_folder):
    img = Image.open(image_path)

    img = img.convert("RGBA")

    img_data = list(img.getdata())

    for i, pixel in enumerate(img_data):
        if pixel[2] > 30 and pixel[0] < 100 and pixel[1] < 100:
            img_data[i] = (255, pixel[1], pixel[2], pixel[3])

    img.putdata(img_data)

    filename = os.path.basename(image_path)
    output_path = os.path.join(output_folder, filename)
    img.save(output_path)


def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith((".png")):
            image_path = os.path.join(input_folder, filename)
            change_blue_to_red(image_path, output_folder)

input_folder = "downloaded_images"
output_folder = "red_images"

process_images(input_folder, output_folder)
import cv2
import os
from skimage.metrics import structural_similarity as ssim


def compare_images(image1, image2):
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    win_size = 5

    similarity = ssim(img1, img2, win_size=win_size, full=True)
    return similarity


def find_matching_image(input_image, folder_path):
    max_similarity = 0
    matching_image = None

    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            similarity, _ = compare_images(input_image, image_path)
            if similarity > max_similarity:
                max_similarity = similarity
                matching_image = image_path
    return matching_image


input_image_path = 'downloaded_images/FFVIII_Anacondaur_monster_card.png'

image_folder_path = 'downloaded_images'

matching_image_path = find_matching_image(input_image_path, image_folder_path)

if matching_image_path:
    print("Image Found:", matching_image_path)
else:
    print("No Image Found")
import cv2
import os
from skimage.metrics import structural_similarity as ssim


def compare_images(image1, image2):
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    win_size = 5
    # Detect similarity
    similarity = ssim(img1, img2, win_size=win_size, full=True)
    return similarity


# Takes the input image and the folder path and iterates between each image to find the matching image
def find_matching_image(input_image, folder_path):
    max_similarity = 0
    matching_image = None
    # Checks each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            similarity, _ = compare_images(input_image, image_path)
            if similarity > max_similarity:
                max_similarity = similarity
                matching_image = image_path
    return matching_image



### This code just iterates through the folder to ensure 100% accuracy
#counter = 0
image_folder_path = 'downloaded_images'

#for image_name in os.listdir(image_folder_path):
    #input_image_path = os.path.join(image_folder_path, image_name)
    #counter += 1

    #matching_image_path = find_matching_image(input_image_path, image_folder_path)

    #if matching_image_path:
        #print(f"{counter} Image Found:", matching_image_path)
    #else:
        #print("No Image Found")
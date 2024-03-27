import cv2
import os


def find_image(image_path, folder_path):

    input_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    orb = cv2.ORB_create()

    keypoints1, descriptors1 = orb.detectAndCompute(input_image, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        keypoints2, descriptors2 = orb.detectAndCompute(img, None)

        matches = matcher.match(descriptors1, descriptors2)

        matches.sort(key=lambda x: x.distance)

        print(f"Image: {filename}, Matches: {len(matches)}")


image_path = 'downloaded_images/FFVIII_Bomb_monster_card.png'
folder_path = 'downloaded_images'

find_image(image_path, folder_path)
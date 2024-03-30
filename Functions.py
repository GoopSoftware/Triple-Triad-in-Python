import random
import pygame
import os
import sys
import cv2
from skimage.metrics import structural_similarity as ssim

screen_width, screen_height = 540, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Triple Triad")

grid_size = (3, 3)
picture_size = (93, 120)

grid_cell_width = picture_size[0]
grid_cell_height = picture_size[1]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

image_folder = "downloaded_images"
images = [pygame.image.load(os.path.join(image_folder, img)).convert_alpha()
          for img in os.listdir(image_folder)]
num_images = len(images)

# The players hand
left_dropdown_images = images[:]
right_dropdown_images = images[:]
random.shuffle(left_dropdown_images)
random.shuffle(right_dropdown_images)
placed_left_cards = []
placed_right_cards = []
card_played = False
dropdown_width = 100
dropdown_item_height = 85
max_dropdown_items_left = 5
max_dropdown_items_right = 5

scroll_pos = 0

dragging_image = None
drag_offset = (0, 0)

card_at_position = [[None for _ in range(grid_size[1])] for _ in range(grid_size[0])]


def players_hand(x_pos, images, max_items, side):
    for i, img in enumerate(images[:max_items]):
        if img not in placed_left_cards and img not in placed_right_cards:
            img_rect = img.get_rect(topleft=(x_pos + 10, i * dropdown_item_height + 20 - scroll_pos))
            screen.blit(img, img_rect)
            if img_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return img
    return None

def draw_background():
    side_width = (screen_width - 300) // 2
    print("Side Width:", side_width)
    if len(left_dropdown_images) > 0:
        pygame.draw.rect(screen, WHITE, (0, 0, side_width, screen_height))
    if len(right_dropdown_images) > 0:
        pygame.draw.rect(screen, WHITE, (screen_width - side_width, 0, side_width, screen_height))

def draw_grid():

    start_x = (screen_width - (grid_size[1] * grid_cell_width)) // 2
    start_y = (screen_height - (grid_size[0] * grid_cell_height)) // 2

    for i in range(1, grid_size[0]):
        pygame.draw.line(screen, BLACK, (start_x, start_y + i * grid_cell_height),
                         (start_x + grid_size[1] * grid_cell_width, start_y + i * grid_cell_height))

    for j in range(1, grid_size[1]):
        pygame.draw.line(screen, BLACK, (start_x + j * grid_cell_width, start_y),
                         (start_x + j * grid_cell_width, start_y + grid_size[0] * grid_cell_height))

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            x = start_x + j * grid_cell_width + (grid_cell_width - picture_size[0]) // 2
            y = start_y + i * grid_cell_height + (grid_cell_height - picture_size[1]) // 2
            pygame.draw.rect(screen, BLUE, (x, y, picture_size[0], picture_size[1]), 2)


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

def compare_images(image1, image2):
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    win_size = 5
    # Detect similarity
    similarity = ssim(img1, img2, win_size=win_size, full=True)
    return similarity
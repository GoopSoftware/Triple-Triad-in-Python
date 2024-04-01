import pygame
import sys
import os
import random
from CardClass import Card
from Functions import (players_hand, draw_grid, draw_background, find_matching_image,
                       compare_images, read_card_data_from_txt)


# todo: store the card class on the grid for later information

pygame.init()
# standardizing the pygame window sizes as well as colors
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


# All file paths for program
image_folder = "downloaded_images"
image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if
                                       img.endswith('png')]
images = [pygame.image.load(os.path.join(image_folder, img)).convert_alpha()
          for img in os.listdir(image_folder)]\
# Number of images that are loaded from the images variable
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


def rearrange_numbers(card_object, direction):


def grid_to_index(row, col):
    return row * grid_size[1] + col


def index_to_grid(index):
    row = index // grid_size[1]
    col = index % grid_size[1]
    return row, col


screen.fill(WHITE)
pygame.display.flip()
running = True
while running:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handles the logic of when the mouse is pressed down for each players hand
            if event.button == 1 and not card_played:
                dragging_image_left = players_hand(0, left_dropdown_images,
                                                   max_dropdown_items_left, side='left')
                if dragging_image_left is not None:
                    if len(left_dropdown_images) > 0:
                        # This helps play the card onto the grid
                        dragging_image = dragging_image_left

                        # This code handles logic of dragging card which is broken
                        #drag_offset = (event.pos[0] - dragging_image.get_rect().left,
                                       #event.pos[1] - dragging_image.get_rect(). top)
                    else:
                        dragging_image_left = None

                dragging_image_right = players_hand(430, right_dropdown_images,
                                                    max_dropdown_items_right, side='right')
                if dragging_image_right is not None:
                    if len(right_dropdown_images) > 0:
                        # This helps play the card onto the grid
                        dragging_image = dragging_image_right

                        # This code handles logic of dragging card which is broken
                        #drag_offset = (event.pos[0] - dragging_image.get_rect().left,
                                       #event.pos[1] - dragging_image.get_rect(). top)
                    else:
                        dragging_image_right = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging_image is not None:
                if dragging_image is not None:
                    # Detecting the card numbers and outputting a Card class
                    selected_card_path = find_matching_image(dragging_image, image_folder)

                    filename = os.path.basename(selected_card_path)
                    filename = filename.replace("downloaded_images\\", "").replace('.png', "")

                    txt_file_path = "CardListValue.txt"
                    card_data = read_card_data_from_txt(filename, txt_file_path)

                    if card_data is not None:
                        # Extract card numbers
                        card_numbers = card_data

                        # Applying card numbers to card class
                        card_object = Card(*card_numbers)
                        #print("Card Object:", card_object)
                    else:
                        print("Error Card data not found for filename:", filename)

                if event.pos[0] < screen_width / 2:
                    side = 'left'
                    player_hand = left_dropdown_images
                    max_dropdown_items_left -= 1
                    left_dropdown_images.remove(dragging_image)
                else:
                    side = 'right'
                    player_hand = right_dropdown_images
                    max_dropdown_items_right -= 1
                    right_dropdown_images.remove(dragging_image)


                grid_start_x = (screen_width - (grid_size[1] * grid_cell_width)) // 2
                grid_start_y = (screen_height - (grid_size[0] * grid_cell_height)) // 2

                for i in range(grid_size[0]):
                    for j in range(grid_size[1]):
                        cell_rect = pygame.Rect(grid_start_x + j * grid_cell_width,
                                                grid_start_y + i * grid_cell_height,
                                                grid_cell_width, grid_cell_height)


                        if cell_rect.collidepoint(event.pos) and card_at_position[i][j] is None:
                            current_index = grid_to_index(i, j)
                            print("Card played at grid cell:", i+1, j+1)
                            adjacent_indices = [
                                grid_to_index(i-1, j),  # Above
                                grid_to_index(i, j - 1),  # Left
                                grid_to_index(i, j + 1),  # Right
                                grid_to_index(i+1, j),  # Below
                            ]
                            for adj_index in adjacent_indices:
                                adj_row, adj_col = index_to_grid(adj_index)
                                if 0 <= adj_row < grid_size[0] and 0 <= adj_col < grid_size[1]:
                                    adjacent_card = card_at_position[adj_row][adj_col]
                                    if adjacent_card is not None:
                                        if card_object.can_take(adjacent_card):
                                            if adj_index == grid_to_index(i-1, j):
                                                print("Taking card above")
                                            elif adj_index == grid_to_index(i+1, j):
                                                print("Taking card below")
                                            elif adj_index == grid_to_index(i, j-1):
                                                print("Taking left card")
                                            elif adj_index == grid_to_index(i,j+1):
                                                print("Taking right card")
                                            print("current card:", card_object)
                                            print("adjacent card:", adjacent_card)
                                    else:
                                        print("cannot take card")
                            cell_center = cell_rect.center
                            image_rect = dragging_image.get_rect(center=cell_center)
                            screen.blit(dragging_image, image_rect)

                            card_at_position[i][j] = card_object

                            card_played = True

                            if dragging_image in left_dropdown_images:
                                left_dropdown_images.remove(dragging_image)
                                placed_left_cards.append(dragging_image)
                            elif dragging_image in right_dropdown_images:
                                right_dropdown_images.remove(dragging_image)
                                placed_right_cards.append(dragging_image)

                            dragging_image = None
                            card_played = False
                            break
                draw_background()

        #elif event.type == pygame.MOUSEMOTION:
            #if dragging_image is not None:
                #dragging_image_rect = dragging_image.get_rect()
                #dragging_image_rect.topleft = (event.pos[0] - drag_offset[0], event.pos[1] - drag_offset[1])

    if not card_played:
        if len(left_dropdown_images) > 0:
            left_card_image = players_hand(0, left_dropdown_images, max_dropdown_items_left, side='left')
        if len(right_dropdown_images) > 0:
            right_card_image = players_hand(430, right_dropdown_images, max_dropdown_items_right, side='right')
    pygame.display.flip()

pygame.quit()
sys.exit()
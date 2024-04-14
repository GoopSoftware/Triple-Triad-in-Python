import pygame
import sys
import os
import random
from CardClass import Card
from Functions import (players_hand, draw_grid, draw_background, find_matching_image,
                       compare_images, read_card_data_from_txt)


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


left_player_score = 5
right_player_score = 5


def check_win_condition():
    #print("Checking win condition")
    if max_dropdown_items_left == 0:
        left_total_score = left_player_score
        right_total_score = right_player_score

        if left_total_score > right_total_score:
            print("Player 1 (left) wins!")
        elif left_total_score < right_total_score:
            print("Player 2 (right) wins!")
        else:
            print("It was a tie!")
        return True

    return False


def take_card(row, col):
    # This function handles the score system and whatever happens after a player takes a card
    global left_player_score, right_player_score

    if card_at_position[row][col] is not None:
        current_owner = card_at_position[row][col].owner
    else:
        print("Card owner doesn not exist")

    if current_owner == side:
        print("cannot take own card")
        return

    if left_player_turn:
        left_player_score -= 1
        right_player_score +=1
        card_at_position[row][col].owner = 'left'
    else:
        right_player_score -= 1
        left_player_score += 1
        card_at_position[row][col].owner = 'right'
    print("Left Player Score:", left_player_score)
    print("Right Player Score:", right_player_score)


def rearrange_numbers(n1, n2, n3, n4):
    n1, n2, n3, n4 = n1, n4, n2, n3
    return n1, n2, n3, n4

def grid_to_index(row, col):
    row = max(0, min(row, grid_size[0] - 1))
    col = max(0, min(col, grid_size[1] - 1))
    return row * grid_size[1] + col


def index_to_grid(index):
    row = index // grid_size[1]
    col = index % grid_size[1]
    row = max(0, min(row, grid_size[0] - 1))
    col = max(0, min(col, grid_size[1] - 1))
    return row, col

def print_grid_with_cards():
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if card_at_position[i][j] is None:
                pass
                #print("   ", end="")  # Print empty space if no card
            else:
                card = card_at_position[i][j]
                # Print card numbers or any other relevant information
                #print(f"{card}", end="")
            #print(" | ", end="")
        #print("\n" + "-" * (6 * grid_size[1] + 1))  # Horizontal line after each row


left_player_turn = True
cards_taken_left = 0
cards_taken_right = 0
font = pygame.font.Font(None, 36)


screen.fill(WHITE)
pygame.display.flip()
running = True
while running:
    draw_grid()
    left_player_score_surface = font.render("{}".format(left_player_score), True, BLACK)
    screen.blit(left_player_score_surface, (170, 25))
    right_player_score_surface = font.render("{}".format(right_player_score), True, BLACK)
    screen.blit(right_player_score_surface, (360, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not card_played:
                if left_player_turn:
                    dragging_image_left = players_hand(0, left_dropdown_images,
                                                   max_dropdown_items_left, side='left')
                    if dragging_image_left is not None:
                        if len(left_dropdown_images) > 0:
                            dragging_image = dragging_image_left

                            # This code handles logic of dragging card which is broken
                            #drag_offset = (event.pos[0] - dragging_image.get_rect().left,
                                           #event.pos[1] - dragging_image.get_rect(). top)
                        else:
                            dragging_image_left = None

                else:
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
                        #print("card numbers", card_numbers)

                        # Applying card numbers to card class
                        card_object = Card(*card_numbers)
                        #print("Card Object:", card_object)
                    else:
                        print("Error Card data not found for filename:", filename)

                if left_player_turn:
                    side = 'left'
                    player_hand = left_dropdown_images
                    max_dropdown_items_left -= 1
                    left_dropdown_images.remove(dragging_image)
                    left_player_turn = False
                else:
                    side = 'right'
                    player_hand = right_dropdown_images
                    max_dropdown_items_right -= 1
                    right_dropdown_images.remove(dragging_image)
                    left_player_turn = True


                grid_start_x = (screen_width - (grid_size[1] * grid_cell_width)) // 2
                grid_start_y = (screen_height - (grid_size[0] * grid_cell_height)) // 2

                for i in range(grid_size[0]):
                    for j in range(grid_size[1]):
                        cell_rect = pygame.Rect(grid_start_x + j * grid_cell_width,
                                                grid_start_y + i * grid_cell_height,
                                                grid_cell_width, grid_cell_height)


                        if cell_rect.collidepoint(event.pos) and card_at_position[i][j] is None:
                            card_object.owner = side
                            card_at_position[i][j] = card_object
                            current_index = grid_to_index(i, j)
                            adjacent_indices = [
                                (i - 1, j),  # Above
                                (i, j - 1),  # Left
                                (i, j + 1),  # Right
                                (i + 1, j),  # Below
                            ]

                            for adj_row, adj_col in adjacent_indices:
                                if 0 <= adj_row < grid_size[0] and 0 <= adj_col < grid_size[1]:
                                    adjacent_card = card_at_position[adj_row][adj_col]

                                    if adjacent_card is not None:
                                        if adj_row == i - 1 and adj_col == j:
                                            if card_object.can_take(adjacent_card, 'top'):
                                                #print("Can take card above:")
                                                take_card(adj_row, adj_col)
                                                card_object.owner = side

                                        if adj_row == i + 1 and adj_col == j:
                                            if card_object.can_take(adjacent_card, 'bottom'):
                                                #print("Can take the card below:")
                                                take_card(adj_row, adj_col)
                                                card_object.owner = side

                                        if adj_row == i and adj_col == j - 1:
                                            if card_object.can_take(adjacent_card, 'left'):
                                                #print("Can take the card to the left:")
                                                take_card(adj_row, adj_col)
                                                card_object.owner = side

                                        if adj_row == i and adj_col == j + 1:
                                            if card_object.can_take(adjacent_card, 'right'):
                                                #print("Can take the card to the right:")
                                                take_card(adj_row, adj_col)
                                                card_object.owner = side

                            if check_win_condition():
                                running = False

                            cell_center = cell_rect.center
                            image_rect = dragging_image.get_rect(center=cell_center)
                            screen.blit(dragging_image, image_rect)

                            card_at_position[i][j] = card_object


                            card_played = True

                            print_grid_with_cards()

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
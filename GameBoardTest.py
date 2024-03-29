import pygame
import sys
import os
import random
from CardClass import Card

pygame.init()

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


def draw_background():
    screen.fill(WHITE)

def players_hand(x_pos, images, max_items, side):
    for i, img in enumerate(images[:max_items]):
        img_rect = img.get_rect(topleft=(x_pos + 10, i * dropdown_item_height + 20 - scroll_pos))
        screen.blit(img, img_rect)
        if img_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return img
    return None


def draw_grid():
    #screen.fill(WHITE)

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


running = True
while running:
    #draw_background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not card_played:
                dragging_image_left = players_hand(0, left_dropdown_images,
                                                   max_dropdown_items_left, side='left')
                if dragging_image_left is not None:
                    dragging_image = dragging_image_left
                    drag_offset = (event.pos[0] - dragging_image.get_rect().left,
                                   event.pos[1] - dragging_image.get_rect(). top)


                dragging_image_right = players_hand(430, right_dropdown_images,
                                                    max_dropdown_items_right, side='right')
                if dragging_image_right is not None:
                    dragging_image = dragging_image_right
                    drag_offset = (event.pos[0] - dragging_image.get_rect().left,
                                   event.pos[1] - dragging_image.get_rect(). top)


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging_image is not None:
                if event.pos[0] < screen_width / 2:
                    side = 'left'
                    player_hand = left_dropdown_images
                else:
                    side = 'right'
                    player_hand = right_dropdown_images

                if side == 'left':
                    max_dropdown_items_left -= 1
                elif side == 'right':
                    max_dropdown_items_right -= 1

                grid_start_x = (screen_width - (grid_size[1] * grid_cell_width)) // 2
                grid_start_y = (screen_height - (grid_size[0] * grid_cell_height)) // 2

                for i in range(grid_size[0]):
                    for j in range(grid_size[1]):
                        cell_rect = pygame.Rect(grid_start_x + j * grid_cell_width,
                                                grid_start_y + i * grid_cell_height,
                                                grid_cell_width, grid_cell_height)

                        if cell_rect.collidepoint(event.pos):
                            cell_center = cell_rect.center
                            image_rect = dragging_image.get_rect(center=cell_center)
                            screen.blit(dragging_image, image_rect)

                            # removes card from hand when played
                            player_hand.remove(dragging_image)

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

        elif event.type == pygame.MOUSEMOTION:
            if dragging_image is not None:
                dragging_image_rect = dragging_image.get_rect()
                dragging_image_rect.topleft = (event.pos[0] - drag_offset[0], event.pos[1] - drag_offset[1])

    for i, card in enumerate(left_dropdown_images[:max_dropdown_items_left]):
        img_rect = card.get_rect(topleft=(0 + 10, i * dropdown_item_height + 20 - scroll_pos))
        screen.blit(card, img_rect)

    for i, card in enumerate(right_dropdown_images[:max_dropdown_items_right]):
        img_rect = card.get_rect(topleft=(430 + 10, i * dropdown_item_height + 20 - scroll_pos))
        screen.blit(card, img_rect)

    if not card_played:
        left_card_image = players_hand(0, left_dropdown_images, max_dropdown_items_left, side='left')
        right_card_image = players_hand(430, right_dropdown_images, max_dropdown_items_right, side='right')



    # This line of code hides the cards behind the grid
    #draw_grid()





    # This line of code is causing img clipping
    #if left_card_image is not None:
        #screen.blit(left_card_image, pygame.mouse.get_pos())

    pygame.display.flip()

pygame.quit()
sys.exit()
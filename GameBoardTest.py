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

left_dropdown_images = images[:]
right_dropdown_images = images[:]
random.shuffle(left_dropdown_images)
random.shuffle(right_dropdown_images)

dropdown_width = 100
dropdown_item_height = 85
max_dropdown_items = 5

scroll_pos = 0

dragging_image = None
drag_offset = (0, 0)


def players_hand(x_pos, images, side):
    for i, img in enumerate(images[:max_dropdown_items]):
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging_image_left = players_hand(0, left_dropdown_images, side='left')
                dragging_image_right = players_hand(430, right_dropdown_images, side='right')
                if dragging_image_left is not None:
                    dragging_image = dragging_image_left
                    drag_offset = (event.pos[0] - dragging_image.get_rect().left,
                                   event.pos[1] - dragging_image.get_rect(). top)
                if dragging_image_right is not None:
                    dragging_image = dragging_image_right
                    drag_offset = (event.pos[0] - dragging_image.get_rect().left,
                                   event.pos[1] - dragging_image.get_rect(). top)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging_image is not None:
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
                            dragging_image = None
                            break

        elif event.type == pygame.MOUSEMOTION:
            if dragging_image is not None:
                dragging_image_rect = dragging_image.get_rect()
                dragging_image_rect.topleft = (event.pos[0] - drag_offset[0], event.pos[1] - drag_offset[1])




    # This line of code hides the cards behind the grid
    draw_grid()

    left_card_image = players_hand(0, left_dropdown_images, side='left')
    right_card_image = players_hand(430, right_dropdown_images, side='right')


    # This line of code is causing img clipping
    #if left_card_image is not None:
        #screen.blit(left_card_image, pygame.mouse.get_pos())

    pygame.display.flip()

pygame.quit()
sys.exit()
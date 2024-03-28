import pygame
import sys
import os
import random

pygame.init()

screen_width, screen_height = 540, 380
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
dropdown_item_height = 50
max_dropdown_items = 5

scroll_pos = 0


def players_hand(x_pos, images, side):
    dropdown_rect = pygame.Rect(x_pos, 0, dropdown_width, screen_height)
    pygame.draw.rect(screen, WHITE, dropdown_rect)
    #pygame.draw.rect(screen, BLACK, dropdown_rect, 2)

    for i, img in enumerate(images[:max_dropdown_items]):
        img_rect = img.get_rect()
        img_rect.topleft = (x_pos + 10, i * dropdown_item_height + 10)
        if screen_height >= img_rect.bottom - scroll_pos >= 0:
            screen.blit(img, img_rect)


def draw_grid():
    screen.fill(WHITE)

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



    draw_grid()

    players_hand(0, left_dropdown_images, side='left')
    players_hand(430, right_dropdown_images, side='right')

    pygame.display.flip()

pygame.quit()
sys.exit()
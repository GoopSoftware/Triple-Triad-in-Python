for i, card in enumerate(left_dropdown_images[:max_dropdown_items_left]):
    img_rect = card.get_rect(topleft=(0 + 10, i * dropdown_item_height + 20 - scroll_pos))
    screen.blit(card, img_rect)

for i, card in enumerate(right_dropdown_images[:max_dropdown_items_right]):
    img_rect = card.get_rect(topleft=(430 + 10, i * dropdown_item_height + 20 - scroll_pos))
    screen.blit(card, img_rect)

if not card_played:
    left_card_image = players_hand(0, left_dropdown_images, max_dropdown_items_left, side='left')
    right_card_image = players_hand(430, right_dropdown_images, max_dropdown_items_right, side='right')

pygame.display.flip()
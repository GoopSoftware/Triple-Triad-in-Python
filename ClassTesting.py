from CardClass import Card

card_name = "FFVIII_Abyss_Worm_monster_card"
extracted_numbers = ['7', '5', '2', '3']
top, right, bottom, left = map(int, extracted_numbers)
card = Card(top, right, bottom, left)

print(f"Card name: {card_name}")
print(f"Card object: {card}")
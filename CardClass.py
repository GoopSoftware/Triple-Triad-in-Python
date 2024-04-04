class Card:
    def __init__(self, top, left, right, bottom):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

    def __repr__(self):
        return f"Card({self.top} {self.left} {self.right} {self.bottom})"


    def update_numbers(self, top, left, right, bottom):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

    def can_take(self, other_card, side):
        if side == 'top':
            if other_card.bottom == 10:
                return False
            return self.top > other_card.bottom

        if side == 'right':
            if other_card.left == 10:
                return False
            return self.right > other_card.left

        if side == 'bottom':
            if other_card.top == 10:
                return False
            return self.bottom > other_card.top

        if side == 'left':
            if other_card.right == 10:
                return False
            return self.left > other_card.right


    def take_card(self, other_card):
        if self.can_take(other_card):
            print("taking card")
            return True

        else:
            print("Cannot take card")
            return False
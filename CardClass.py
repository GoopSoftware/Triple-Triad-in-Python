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

    def can_take(self, other_card):
        if other_card.top == 10 or other_card.right == 10 or other_card.bottom == 10 or other_card.left == 10:
            return False

        if self.top == other_card.bottom or \
                self.right == other_card.left or \
                self.bottom == other_card.top or \
                self.left == other_card.right:
            return False

        if self.top > other_card.bottom:
            print(self.top, other_card.bottom)
            return True
        if self.right > other_card.left:
            print(self.right, other_card.left)
            return True
        if self.bottom > other_card.top:
            print(self.bottom, other_card.top)
            return True
        if self.left > other_card.right:
            print(self.left, other_card.right)
            return True
        return False

    def take_card(self, other_card):
        if self.can_take(other_card):
            print("taking card")
            return True

        else:
            print("Cannot take card")
            return False
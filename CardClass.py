class Card:
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def __repr__(self):
        return f"Card({self.top}, {self.right}, {self.bottom}, {self.left})"

    def can_take(self, other_card):
        if self.top == other_card.bottom or \
                self.right == other_card.left or \
                self.bottom == other_card.top or \
                self.left == other_card.right:
            return False

        if self.top > other_card.bottom:
            return True
        if self.right > other_card.left:
            return True
        if self.bottom > other_card.top:
            return True
        if self.left > other_card.right:
            return True
        return False
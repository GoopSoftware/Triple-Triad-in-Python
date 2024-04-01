class Card:
    def __init__(self, top, left, right, bottom):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

    def __repr__(self):
        return f"Card({self.top} {self.right} {self.bottom} {self.left})"


    def update_numbees(self, top, left, right, bottom):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

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
    def take_card(self, other_card):
        if self.cantake(other_card):
            #print("taking card")
            return True

        else:
            #print("Cannot take card")
            return False
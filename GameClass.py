class Game:
    def __init__(self):
        self.player1_score = 5
        self.player2_score = 5

    def update_scores(self, player_taking_card, num_cards_taken):
        if player_taking_card == 1:
            self.player1_score += num_cards_taken
            self.player2_score -= num_cards_taken
        elif player_taking_card == 2:
            self.player1_score += num_cards_taken
            self.player2_score -= num_cards_taken


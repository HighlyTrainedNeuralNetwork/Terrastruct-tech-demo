import numpy as np

class Game:
    def __init__(self, num_players):
        self.previous_winner = None
        self.players = {}
        self.stack = {}
        self.num_players = num_players
        self.deck = Deck()

    def add_players(self):
        for i in range(self.num_players):
            self.players[i + 1] = Player(i + 1)

    def deal_hands(self):
        deck_slice = self.deck.deck[:-(len(self.deck.deck) % self.num_players) or None]
        while len(deck_slice) > 0:
            for player in range(self.num_players):
                self.players[player + 1].hand.append(deck_slice.pop())

    def comparison(self):
        stack = []
        for player in self.players.values():
            stack.append(player.hand.pop())
            print("Player {} played card {}.".format(player.name, stack[-1]))
        if stack.count(max(stack)) == 1:
            winner = stack.index(max(stack)) + 1
        elif self.previous_winner:
            winner = self.previous_winner
        else:
            winner = np.random.randint(1, len(self.players) + 1)

        self.players[winner].win_pile.extend(stack)
        self.previous_winner = winner
        self.stack = {}
        stdout = "Player {} won the battle.".format(winner)
        for player in self.players.values():
            stdout += " Player {} now has {} cards left.".format(player.name, len(player.hand) + len(player.win_pile))
        print(stdout)

    def check_state(self):
        if any((len(player.hand) + len(player.win_pile)) == 0 for player in self.players.values()):
            print("Player {} has won the game!".format(max(self.players.values(), key=lambda x: len(x.win_pile) + len(x.hand)).name))
            return False
        else:
            for player in self.players.values():
                if len(player.hand) == 0:
                    player.shuffle()
                    print("Player {} shuffled their deck".format(player.name))
            return True

class Deck:
    def __init__(self):
        self.deck = []
        for i in range(1, 3):
            for z in range(1, 14):
                self.deck.append(z)
        np.random.shuffle(self.deck)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.win_pile = []

    def shuffle(self):
        self.hand = self.win_pile
        np.random.shuffle(self.hand)
        self.win_pile = []
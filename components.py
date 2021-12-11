import numpy as np

class Game:
    def __init__(self, num_players):
        self.previous_winner = None
        self.players = []
        self.stack = {}
        self.num_players = num_players
        self.deck = Deck()

    def add_players(self):
        for i in range(self.num_players):
            bot_type = input("Select bot type from highest and random:")
            self.players.append(Player(i + 1, bot_type))

    def deal_hands(self):
        deck_slice = self.deck.deck[:-(len(self.deck.deck) % self.num_players) or None]
        while len(deck_slice) > 0:
            for player in range(self.num_players):
                self.players[player].draw_pile.append(deck_slice.pop())
        for player in self.players:
            for i in range(5):
                player.hold_pile.append(player.draw_pile.pop())

    def execute_turn(self):
        stack = []
        for player in self.players:
            if player.strategy == "random":
                stack.append(player.play_random())
            elif player.strategy == "highest":
                stack.append(player.play_highest())
            print("Player {} played card {} from {}.".format(player.name, stack[-1], player.hold_pile))
        if stack.count(max(stack)) == 1:
            winner = stack.index(max(stack))
        elif self.previous_winner:
            winner = self.previous_winner
        else:
            winner = np.random.randint(0, len(self.players))
        self.players[winner].win_pile.extend(stack)
        self.previous_winner = winner
        self.stack = []
        stdout = "Player {} won the battle.".format(winner + 1)
        for player in self.players:
            player.attempt_draw()
            stdout += " Player {} now has {} cards left.".format(player.name, len(player.draw_pile) + len(player.hold_pile) + len(player.win_pile))
        print(stdout)

    def check_state(self):
        if any(len(player.draw_pile) == 0 and len(player.hold_pile) == 0 and len(player.win_pile) == 0 for player in self.players):
            winner = max(self.players, key=lambda x: len(x.hold_pile) + len(x.draw_pile) + len(x.win_pile)).name
            print("Player {} won the game!".format(winner))
            return False
        return True

class Deck:
    def __init__(self):
        self.deck = []
        for i in range(1, 2):
            for z in range(1, 15):
                self.deck.append(z)
        np.random.shuffle(self.deck)

class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.draw_pile = []
        self.hold_pile = []
        self.win_pile = []
        self.strategy = strategy

    def shuffle(self):
        self.draw_pile = self.win_pile
        np.random.shuffle(self.draw_pile)
        self.win_pile = []

    def attempt_draw(self):
        if len(self.draw_pile) > 0:
            self.hold_pile.append(self.draw_pile.pop())
        elif len(self.win_pile) > 0:
            self.shuffle()
            print("Player {} shuffled their deck".format(self.name))
            self.hold_pile.append(self.draw_pile.pop())

    def play_random(self):
        np.random.shuffle(self.hold_pile)
        return self.hold_pile.pop()

    def play_highest(self):
        self.hold_pile.sort()
        return self.hold_pile.pop()
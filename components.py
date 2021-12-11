import numpy as np

class Game:
    def __init__(self, num_players):
        self.players = []
        self.stack = {}
        self.num_players = num_players
        self.deck = Deck()
        self.active_fight = True

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

    def execute_turn(self, considered_players):
        for player in considered_players:
            if player.name in self.stack.keys():
                self.stack[player.name].append(player.identify_strategy())
            else:
                self.stack[player.name] = [player.identify_strategy()]
            print("Player {} played card {} from {}.".format(player.name, self.stack[player.name][-1], player.hold_pile + [self.stack[player.name][-1]]))
        latest_cards = [values[-1] for player, values in self.stack.items() if player in [player.name for player in considered_players]]
        if latest_cards.count(max(latest_cards)) == 1:
            winner = considered_players[latest_cards.index(max(latest_cards))].name
            print("Player {} won the battle.".format(winner))
            self.players[winner - 1].win_pile.extend(sum(self.stack.values(), []))
            self.stack = {}
        stdout = ""
        for player in considered_players:
            stdout += "Player {} now has {} cards left.".format(player.name, len(player.draw_pile) + len(player.hold_pile) + len(player.win_pile))
            player.attempt_draw()
        print(stdout)
        if self.stack:
            self.check_state()
            considered_players = [player for iteration, player in enumerate(considered_players) if latest_cards[iteration] == max(latest_cards) and not player.eliminated]
            self.execute_turn(considered_players)

    def check_state(self):
        for player in [player for player in self.players if not player.eliminated]:
            if len(player.draw_pile) == 0 and len(player.hold_pile) == 0 and len(player.win_pile) == 0:
                print("Player {} was eliminated.".format(player.name))
                player.eliminated = True
        if [player.eliminated for player in self.players].count(False) == 1:
            winner = next(player for player in self.players if not player.eliminated).name
            print("Player {} wins!".format(winner))
            return False
        return True

class Deck:
    def __init__(self):
        self.deck = []
        for i in range(1, 5):
            for y in range(1, 15):
                self.deck.append(y)
        np.random.shuffle(self.deck)

class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.draw_pile = []
        self.hold_pile = []
        self.win_pile = []
        self.strategy = strategy
        self.eliminated = False

    def shuffle(self):
        self.draw_pile = self.win_pile
        np.random.shuffle(self.draw_pile)
        self.win_pile = []

    def attempt_draw(self):
        if len(self.draw_pile) > 0:
            self.hold_pile.append(self.draw_pile.pop())
        elif len(self.win_pile) > 0:
            self.shuffle()
            self.hold_pile.append(self.draw_pile.pop())

    def identify_strategy(self):
        if self.strategy == "random":
            return self.play_random()
        elif self.strategy == "highest":
            return self.play_highest()

    def play_random(self):
        np.random.shuffle(self.hold_pile)
        return self.hold_pile.pop()

    def play_highest(self):
        self.hold_pile.sort()
        return self.hold_pile.pop()
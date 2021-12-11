from components import Game

game_instance = Game(2)
game_instance.add_players()
game_instance.deal_hands()

game_active = True
while game_active:
    game_instance.execute_turn()
    game_active = game_instance.check_state()
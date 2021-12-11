from components import Game

game_instance = Game(5)
game_instance.add_players()
game_instance.deal_hands()

game_active = True
while game_active:
    game_instance.execute_turn([player for player in game_instance.players if not player.eliminated])
    game_active = game_instance.check_state()
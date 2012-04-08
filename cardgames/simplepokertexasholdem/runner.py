'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

###############################################################################
# [have fun] 11) Play!
  
from cardgames import simplepokertexasholdem

strategyPlayer1 = u'''
addCommand(BetCommand(player, 10))'''
strategyPlayer2 = simplepokertexasholdem.Strategy()

from gameengine import players
strategyPlayer3 = players.InteractiveStrategy()

# required
mapPlayersToStrategy = {'Player1': strategyPlayer1, 'Player2': strategyPlayer3} 

# [optional]
mapPlayersTeams = {'Player1': 'Team1', 'Player2': 'Team2'}

# optional
mapOfConfigurations = {'timeForCommand': -1, 'timeForPlay': -1, 'timeForGame': -1,
                       'amountOfChipsPerPlayer': 300, 'roundsPrice': 50, 'maxBet': 100}

if __name__ == "__main__":
  game = simplepokertexasholdem.GameFactory().createGame(mapPlayersToStrategy, mapPlayersTeams, mapOfConfigurations)
  try:
    game.start()
  finally:
    print(game.report().summary())

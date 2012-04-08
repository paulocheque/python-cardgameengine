'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

from cardgameengine import players
from cardgames import truco

configurations = truco.TrucoConfigurations()

strategyPlayer1 = truco.TrucoStrategy
strategyPlayer2 = truco.TrucoStrategy

listofplayers = [players.Player('Player1', strategyPlayer1), 
                players.Player('Player2', strategyPlayer2)]

# or

team1 = players.Team('Team1')
team2 = players.Team('Team2')
listofplayers = [players.Player('Player1', strategyPlayer1, team1), 
                players.Player('Player2', strategyPlayer2, team2)]

game = truco.TrucoCardGame(listofplayers, configurations)
game.play()
game.report()
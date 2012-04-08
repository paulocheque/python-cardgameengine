'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

from cardgameengine import players
from cardgames import pokertexasholdem

configurations = pokertexasholdem.PokerTexasHoldEmConfigurations()

strategyPlayer1 = pokertexasholdem.PokerTexasHoldEmStrategy
strategyPlayer2 = pokertexasholdem.PokerTexasHoldEmStrategy

team1 = players.Team('Team1')
team2 = players.Team('Team2')
listofplayers = [players.Player('Player1', strategyPlayer1, team1), 
                 players.Player('Player2', strategyPlayer2, team2)]

game = pokertexasholdem.PokerTexasHoldEmCardGame(listofplayers, configurations)
game.play()
game.report()
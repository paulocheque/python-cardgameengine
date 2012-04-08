'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''
 
from cardgameengine import players
from cardgames import blackjack

# one to seven players
# accept 1, 2, 4, 6 and 8 decks
configurations = blackjack.BlackJackConfigurations()

strategyPlayer1 = blackjack.BlackJackStrategy
strategyPlayer2 = blackjack.BlackJackStrategy

team1 = players.Team('Team1')
team2 = players.Team('Team2')
listofplayers = [players.Player('Player1', strategyPlayer1, team1), 
                players.Player('Player2', strategyPlayer2, team2)]

game = blackjack.BlackJackCardGame(listofplayers, configurations)
game.play()
game.report()
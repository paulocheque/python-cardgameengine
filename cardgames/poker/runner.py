'''

@author: Paulo Cheque (paulocheque@gmail.com)

Example of usage:

from cardgameengine import cardgame
from cardgames.mygame import * 

players = [MyPlayer('Player1'), MyPlayer('Player2')]

# or

team1 = cardgame.Team('Team1')
team2 = cardgame.Team('Team2')
players = [MyPlayer('Player1', team1), MyPlayer('Player2', team2)]

game = MyGame(players)
game.start()
game.report()
'''


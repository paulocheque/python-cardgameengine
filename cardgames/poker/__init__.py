'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

from cardgameengine import cardgame

class PokerRound(cardgame.Round):
  
  def organize(self):
#    distribuir cartas
    pass
  
  def isTheEnd(self):
    pass
    
  def end(self):
#    divide fichas entre vencedores
    pass
  
  def winner(self):
#    jogador com melor jogo, pode ter empate
    pass
  
class PokerCardGame(cardgame.CardGame):
  
  def __init__(self, roundPrototype, players):
    super(PokerCardGame, self).__init__(HoleRound(), players)

  def organize(self):
#    distribuir fichas
    pass
  
  def isTheEnd(self):
#    so sobrou um player com fichas
    pass
    
  def end(self):
    pass
  
  def winner(self):
#    unico player
    pass

'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

from cardgameengine import cardgame
from cardgameengine import commands
from cardgameengine import players
from cardgameengine import cards
from cardgameengine import utils
from cardgameengine.constants import *

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class BlackJackCard(cards.ValueCard):
  
  values = cards.VALUES_ANGLO_AMERICAN
  suits = cards.SUITS_ANGLO_AMERICAN

###############################################################################
# [required] 2) Create the logic of the game: Probably this is easy to create than MyRound class.

class BlackJackCardGame(cardgame.CardGame):

  def __init__(self, players, configurations):
    super(BlackJackCardGame, self).__init__(BlackJackRound, players, configurations, BlackJackCardGameReport)
    self.playersPoints = {}
    for player in players:
      if not player.name in self.playersPoints:
        self.playersPoints[player.name] = 0
    
  def organize(self): pass
  
  def end(self): pass
    
  def conditionToWin(self, player):
    return self.numberOfRounds() == self.maximumOfRounds and \
          self.playersPoints[player.name] >= max(self.playersPoints.values())
      

###############################################################################
# [required] 2): Define the context where the commands will be executed:

class BlackJackRoundContext(cardgame.RoundContext):
  def __init__(self):
    super(BlackJackRoundContext, self).__init__()
    self.playersPoints = {}
    self.playersNumberOfCards = {}
    self.whichPlayersHaveStood = {}
    self.whichPlayersHaveBusted = {}
    self.whichPlayersHaveSurrended = {}

  def summary(self):
    return str(self.playersPoints)

###############################################################################
# [required] 3): Define player's commands

class HitCommand(commands.CardGameCommand):

  def validate(self, context):
    pass
  
  def execute(self, game, round):
    round.seeCurrentPlayerCards().push(round.deck.pop())
    bust = round.seeCurrentPlayerCards().score() > 21
    if bust: 
      round.standPlayer(self.player)
      round.removePlayer(self.player)
  
MyCardGame.registerCommand(HitCommand)
  
class StandCommand(commands.CardGameCommand):

  def validate(self, context):
    self.context.playercards
  
  def execute(self, game, round):
    round.standPlayer(self.player)
    
MyCardGame.registerCommand(StandCommand)
    
class DoubleDownCommand(commands.CardGameCommand):

  def validate(self, context):
    pass
  
  def execute(self, game, round):
#    dobrar aposta, pegar uma carta e stand
    round.seeCurrentPlayerCards().push(round.deck.pop())
    round.standPlayer(self.player)
    bust = round.seeCurrentPlayerCards().score() > 21
    if bust: 
      round.removePlayer(self.player)
#    round.bettingBox += self.params

MyCardGame.registerCommand(DoubleDownCommand)
  
class SplitAPairCommand(commands.CardGameCommand):

  def validate(self, context):
#    aposta maior que min e menor que max
    self.context.playercards.height() == 2 and self.context.playercards.allCardsWithSameValue()
  
  def execute(self, game, round):
#    round.bettingBox += self.params
#    aumentar a aposta, separar duas cartas, 
#    cada carta recebe + 2
    pass
  
MyCardGame.registerCommand(SplitAPairCommand)
  
class SurrenderCommand(commands.CardGameCommand):
  '''
  Leave current round giving up helf this bet
  '''
  
  def validate(self, context):
    pass
  
  def execute(self, game, round):
    round.removePlayer(self.player)
#    sai da rodada e perde metade do dinheiro apostado
    pass

MyCardGame.registerCommand(SurrenderCommand)

###############################################################################
# [required] 4): Define strategies to a player

class BlackJackStrategy(players.Strategy):
  
  def play(self, commandsManager, context):
    self.hit(commandsManager, context)
    self.stop(commandsManager, context)
    pass

  def hit(self, commandsManager, context): pass
  def stop(self, commandsManager, contextself): pass
  
###############################################################################
# [optional] 5): Define a model of reports to store informations.
 
# All reports already have: players, initialNumberOfPlayers, durationTime, winners
# RoundReport has report of all commands (good to debug and undertandings algorithms)
# CardGameReport has report of all rounds (good to debug and undertandings algorithms)

class BlackJackRoundReport(cardgame.RoundReport):
  # need implementation
  pass
  
class BlackJackCardGameReport(cardgame.CardGameReport):
  # need implementation
  pass
  
###############################################################################
# [required] 6) Create the logic of a round of the game:
 
class BlackJackRound(cardgame.Round):

  def __init__(self, game, players, commandsManager):
    super(BlackJackRound, self).__init__(game, players, commandsManager, BlackJackRoundContext, BlackJackRoundReport)
    self.bettingBox = 0
#    self.dealerCards = cards.StackOfCards()

  def populateContext(self, context):
    context.playersPoints = self.game.playersPoints

  def organize(self):
    self.deck.shuffle()
    self.distributeCardsToAllPlayers(1)
  
  def end(self): pass
    
  def conditionToWin(self, player):
    return self.seeCards(player).score() <= 21 and \
          self.playersCards[player.name] >= max(self.playersCards.values())
    
###############################################################################
# [optional] 7) Define configurations of the game
    
class BlackJackConfigurations(cardgame.Configurations):
  
  def __init__(self, maximumOfRounds=3, timeForPlay=-1):
    def scoreFunction(value, suit):
      if value == 1: return 1 # or 11
      if value >= 11 and value <= 13: return 10
      return value
    
    deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(BlackJackCard, 4, 13, 1, 0, scoreFunction)
    super(BlackJackConfigurations, self).__init__(deckPrototype, timeForPlay)
    
    self.maximumOfRounds = maximumOfRounds
    # aposta minima e maxima
    

###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 


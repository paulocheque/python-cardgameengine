'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

  # need implementation so suas cartas e o que virou. Quantas cartas tem cada um? sua posicao na rodada. se é primeiro, segundo etc.
  # need implementation
  # trucar, desistir, baixar jogo, pedir 6, 9, 12

from cardgameengine import cardgame
from cardgameengine import commands
from cardgameengine import players
from cardgameengine import cards
from cardgameengine import utils
from cardgameengine.constants import *

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class TrucoCard(cards.SuitCard):
  values = cards.VALUES_ANGLO_AMERICAN
  suits = cards.SUITS_ANGLO_AMERICAN
  
###############################################################################
# [required] 2) Create the logic of the game: Probably this is easy to create than MyRound class.

class MyCardGame(cardgame.CardGame):

  def __init__(self, players, configuration):
    # super(MyCardGame, self).__init__(MyRound, players[, configurations=None][, reportCollectorClass=CardGameReport])
    super(MyCardGame, self).__init__(MyRound, players, configurations, MyCardGameReport)
    
  def organize(self):
    # need implementation
    # Some work before the round is started, like give chips, etc
    pass
  
  def end(self):
    # need implementation
    # Some work after the game is finished, like log something in report, etc
    pass
    
  def conditionToWin(self, player):
    # need implementation
    # Define a logic that return True if a player win this game, else returns False
    # Pay attention that this method is used by 'isTheEnd' and 'winners' methods
    pass
  
###############################################################################
# [required] 2): Define the context where the commands will be executed:

class MyRoundContext(cardgame.RoundContext):
  def __init__(self):
    super(MyRoundContext, self).__init__()
    # some variables
    # see method context on the round class (step to create the Round)

  def summary(self):
    return 'Commands' + str(self.somecommand)

###############################################################################
# [required] 3): Define player's commands

class MyCommand(commands.CardGameCommand):

  def validate(self, context):
    # Must return InvalidCommandError if this command cant be executed in that context
    if context.flag == True: 
      raise InvalidCommandError('flag must be False!')
  
  def execute(self, game, round):
    # some implementation here, example:
    game.removePlayer(self.player)
    round.seeCards(self.player).sort()
    
MyCardGame.registerCommand(MyCommand)

###############################################################################
# [required] 4): Define strategies to a player

class MyStrategy(players.Strategy):

  def play(self, commandsManager, context):
    self.stepone(commandsManager, context)
    self.steptwo(commandsManager, context)
      
  def stepone(self, commandsManager, context):
    # implementation here, example:
    if context.something == anotherthing:
      mycommand = MyCommand(self.player, context)
      if mycommand.isValid(context):
        commandsManager.addCommand(mycommand)
    pass
    
  def steptwo(self, commandsManager, context):
    # implementation here, example:
    pass
    
###############################################################################
# [optional] 5): Define a model of reports to store informations.
 
class MyRoundReport(cardgame.RoundReport):
  # need implementation
  pass
  
class MyCardGameReport(cardgame.CardGameReport):
  # need implementation
  pass
  
###############################################################################
# [required] 6) Create the logic of a round of the game:
 
class MyRound(cardgame.Round):

  def __init__(self, game, players, commandsManager):
    super(MyRound, self).__init__(game, players, commandsManager, MyContext, MyRoundReport)

  def populateContext(self, context):
    # need implementation:
    # Set attributes to the context that a user need to know to play, like community cards, etc
    # Example: context.communitycards = self.communitycards
    # Dont do this: context.round = self or context.game = self.game. This can facilitate cheats.
    pass

  def organize(self):
    # need implementation
    # Some work before the round is started, like give cards to players, community cards, chips, etc
    pass
  
  def end(self):
    # need implementation
    # Some work after the round is finished, like log something in report or count points...
    pass
    
  def conditionToWin(self, player):
    # need implementation
    # Define a logic that return True if a player win this round, else returns False
    # Pay attention that this method is used by 'isTheEnd' and 'winners' methods
    pass

###############################################################################
# [required] 7) Define configurations of the game
# Define a model of deck that will be used in the beginning of all rounds

class MyConfigurations(cardgame.Configurations):
  
  def __init__(self, deckPrototype, timeForPlay=-1):
  
    deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(TrucoCard, 4, 13, 1, 0)

    super(MyConfigurations, self).__init__(deckPrototype, timeForPlay)
    
###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 


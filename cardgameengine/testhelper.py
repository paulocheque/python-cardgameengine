'''

@author: Paulo Cheque (paulocheque@gmail.com)

Example of usage:

from cardgameengine import mygamehelper

class MyTestCaseClass(mygamehelper.CardGameEngineTests):
  pass

'''

import time

import unittest

from gameengine import commands, players, utils
from cardgameengine import cardgame, cards
from cardgameengine.constants import *

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class MyCard(cards.Card):
  pass

class MyMappedCard(cards.Card):
  values = cards.VALUES_ANGLO_AMERICAN
  suits = cards.SUITS_ANGLO_AMERICAN
  
class MyCustomMappedCard(cards.Card):
  values = {1: 'AS'}
  suits = {1: 'CLUBS'}
  
class MyValueCard(cards.ValueCard):
  pass

class MySuitCard(cards.SuitCard):
  pass

###############################################################################
# [required] 2) Create the logic of the game

class MyCardGame(cardgame.Game):
  
  def __init__(self, players, configurations=None):
    commandsManager = commands.SynchronousCommandsManager()
    commandsManager.registerCommand(NeutralCommand)
    commandsManager.registerCommand(InvalidCommand)
    commandsManager.registerCommand(BuggedCommand)
    commandsManager.registerCommand(SlowCommand)
    commandsManager.registerCommand(ParamsCommand)
    super(MyCardGame, self).__init__(players, configurations, commandsManager, MyCardGameReport(), MyRound)
    
  def organize(self): pass
  
  def end(self): pass
    
  def conditionToWin(self, player): pass

###############################################################################
# [required] 2): Define player's commands

class NeutralCommand(commands.PlayerCommand):
  def executeWithValidation(self, game, round): print('Hi!')
  
class UnknownCommand(commands.PlayerCommand):
  def executeWithValidation(self, game, round): return True
  
class InvalidCommand(commands.PlayerCommand):
  def validate(self, context):
    raise commands.InvalidCommandError(self, 'an error message') 
    return False
  def executeWithValidation(self, game, round): return True
  
class BuggedCommand(commands.PlayerCommand):
  def executeWithValidation(self, game, round): raise Exception('ops')
  
class SlowCommand(commands.PlayerCommand):
  def executeWithValidation(self, game, round): time.sleep(0.5)
  
class ParamsCommand(commands.PlayerCommand):
  def executeWithValidation(self, game, round): print(self.params)

###############################################################################
# [required] 3): Define the context where the commands will be executed:

class MyPlayerContext(cardgame.Context):

  def __init__(self):
    super(MyPlayerContext, self).__init__()

###############################################################################
# [required] 4): Define strategies to a player

class MyStrategy(players.Strategy):
  
  def play(self, commandsManager, context):
    self.actionOne(commandsManager, context)
    self.actionTwo(commandsManager, context)
    
  def actionOne(self, commandsManager, context): pass
  def actionTwo(self, commandsManager, context): pass
  
class CycleStrategy(players.Strategy):
  
  def __init__(self):
    self.flag = 0
    
  def play(self, commandsManager, context):
    if self.flag == 0: 
      self.flag = 1
      commandsManager.addCommand(NeutralCommand(self.player, self.flag))
    if self.flag == 1: 
      self.flag = 0
      commandsManager.addCommand(NeutralCommand(self.player, self.flag))
  
###############################################################################
# [optional] 5): Define a model of reports to store informations.
 
class MyRoundReport(cardgame.RoundReport):
  
  def __init__(self):
    super(MyRoundReport, self).__init__()
    self.mydata = 0
  
class MyCardGameReport(cardgame.GameReport):
  
  def __init__(self):
    super(MyCardGameReport, self).__init__()
    self.mydata = 0
  
###############################################################################
# [required] 6) Create the logic of a round of the game:
 
class MyRound(cardgame.Round):

  def __init__(self, game, players, configurations):
    super(MyRound, self).__init__(game, players, configurations, reportCollector=MyRoundReport())

  def populateContext(self, context): pass

  def organize(self): pass
  
  def end(self): pass
    
  def conditionToWin(self, player): pass

###############################################################################
# [optional] 7) Define configurations of the game

deckMappedCard = cards.DeckPrototypeBuilder.createCommonDeck(MyMappedCard, 4, 13, 1, 1)
deckCustomMappedCard = cards.DeckPrototypeBuilder.createCommonDeck(MyCustomMappedCard, 4, 13, 1, 1)
deckValusCard = cards.DeckPrototypeBuilder.createCommonDeck(MyValueCard, 4, 13, 1, 1)
deckSuitCard = cards.DeckPrototypeBuilder.createCommonDeck(MySuitCard, 4, 13, 1, 1)

def scoreFunction(value, score):
  if value == 0: return 20
  if value == 1: return 15
  if value == 2: return 10
  if value >= 3 and value <= 7: return 5
  if value >= 8 and value <= 13: return 10
  
scoredDeck = cards.DeckPrototypeBuilder.createCommonDeck(MyCard, 4, 13, 1, 0, scoreFunction)

uncommonDeck = cards.StackOfCards()
uncommonDeck.push(cards.Card(-1, 500, 34))
uncommonDeck.push(cards.Card(-50, -123, 1234))
uncommonDeck.push(cards.Card(-50, -123, 456))
uncommonDeck.push(cards.Card(-50, -123))

deck = cards.DeckPrototypeBuilder.createCommonDeck(MyCard, 4, 13, 1, 1)

class MyConfigurations(cardgame.Configurations):
  def __init__(self):
    super(MyConfigurations, self).__init__(deck, 5, 5, 5)
    
    
###############################################################################
# Base Test Class:

class CardGameEngineTests(unittest.TestCase):

  def setUp(self):
    self.oneplayer = [players.Player('Player1', MyStrategy), players.Player('Player2', MyStrategy)]
    self.twoplayers = [players.Player('Player1', MyStrategy), players.Player('Player2', MyStrategy)]
    self.twoplayersWithSameTeam = [
                             players.Player('Player1', MyStrategy, team=players.Team('MyTeam')), 
                             players.Player('Player2', MyStrategy, team=players.Team('MyTeam'))]
    
    self.player = self.twoplayers[0]
    
    self.context = MyPlayerContext()
    
    self.params = None
    
    self.neutralcommand = NeutralCommand(self.player, self.params)
    self.unknowncommand = UnknownCommand(self.player, self.params)
    self.invalidcommand = InvalidCommand(self.player, self.params)
    self.buggedcommand = BuggedCommand(self.player, self.params)
    self.slowcommand = SlowCommand(self.player, self.params)
    self.paramscommand = ParamsCommand(self.player, 'myparam')
    
    self.strategy = MyStrategy
    
    self.roundreport = MyRoundReport()
    self.cardgamereport = MyCardGameReport()
    
    self.deck = deck.clone()
    self.deckMappedCard = deckMappedCard.clone()
    self.deckCustomMappedCard = deckCustomMappedCard.clone()
    self.deckValusCard = deckValusCard.clone()
    self.deckSuitCard = deckSuitCard.clone()
    self.uncommonDeck = uncommonDeck.clone()
    
    self.configurations = MyConfigurations()
    
    self.game = MyCardGame(self.twoplayers, self.configurations)
    
    self.round = MyRound(self.game, self.twoplayers[:], self.configurations)
    self.round.currentPlayer = self.player
    self.game.currentRound = self.round
    
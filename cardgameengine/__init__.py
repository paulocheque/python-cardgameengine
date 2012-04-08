'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

'''
=Description=

Written in python (compatible with 2.6 and 3.0), this library has useful objects and methods to facilitate of the creation of card games.
Using this engine/framework it is possible to create a greate and famous card game with few lines of code, 
but only for the core of the game, because this engine don't provide methods to create users interfaces (GUI, WUI, Console).
This library provides a model (in the end of this document) of unit tests to your games, to facilitate writing
a card game with TDD.

=Games under construction=

  * Hole (about 450 lines of code)
  * Poker Texas Hold'Em (about 400 lines of code)
  * BlackJack

=Next games =

  * Poker
  * Canastra
  * Solitaire
  * Truco
  * Hearts
  * Blackjack
  * Spades
  * Uno

=Example of Usage=
 
{{{

# Let's create a game called "My"

from gameengine import game, utils, commands, players, errors
from cardgameengine import cardgame, cards
from cardgameengine.constants import *

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

#'Card': Ordered by value / Equality by value and suit
#'ValueCard': Ordered by value / Equality by value
#'SuitCard': Ordered by value and suit / Equality by value and suit

class Card(cards.SuitCard):
  # If you specified 'values' and 'suits' variables, so the __str__ will return a the name of a value/suit.
  # Example with variables: 1-1, 11-2 ...
  # Example without variables: AS-SPADES, J-HEARTS ...
  
  # You can use common values and suits (cards.VALUES_***, cards.SUITS_***) or create your own:
  # Example: values = {1: 'AS' ... }, suits = {1: 'CLUBS' ... }
  
  values = cards.VALUES_ANGLO_AMERICAN
  suits = cards.SUITS_ANGLO_AMERICAN
  
###############################################################################
# [required] 2) Define configurations of the game

class Configurations(cardgame.Configurations):
  
  def __init__(self, timeForCommand=-1, timeForPlay=-1, timeForGame=-1):
  
    # Parameters (there parameters can be passed by constructor to facilitate the customization:
    # cardClass: Class object of the card, to use to create instances, like prototype pattern.
    # numberOfSuits: Number os different suits, tipically is 2 or 4
    # numberOfCardsPerSuit: Number of cards per suit, tipically is 10, 11, 12 or 13
    # numberOfDecks (default 1): Number of decks, i.e., equal cards (value and suit) in the deck
    # numberOfJokersPerDeck (default 0): Number of jokers (Card(0, 0)) per deck
    # scoreFunction (default: lambda value,suit: 0): give a function with rules of score
    # Example:

    def scoreFunction(value, suit):
      if value == 0: return 20
      if value == 1: return 15
      if value == 2: return 10
      if value >= 3 and value <= 7: return 5
      if value >= 8 and value <= 13: return 10
      return 0
    
    # Define a model of deck that will be used in the beginning of all rounds
    deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(Card, 4, 13, 1, 1, scoreFunction)
    
    # If you need a not common deck, for example two cards with same value and suit but with different score,
    # you can simply do this (example):
    # deckPrototype = cards.StackOfCards()
    # deckPrototype.push(cards.Card(-1, 500, 34))
    # deckPrototype.push(cards.Card(-50, -123, 1234))
    # deckPrototype.push(cards.Card(-50, -123, 456))
    # deckPrototype.push(cards.Card(-50, -123))
    
    # timeForCommand: default -1 = infinite
    # timeForPlay: default -1 = infinite  
    # timeForGame: default -1 = infinite
    # super(Configurations, self).__init__(deckPrototype[, timeForCommand=-1][, timeForPlay=-1][, timeForGame=-1])
    super(Configurations, self).__init__(deckPrototype, timeForCommand, timeForPlay, timeForGame)
    # other attributes here
    
###############################################################################
# [required] 3): Define the context of a player

# A context contains the content that a player can see to decide what to do.
# All contexts has: player, playercards, currentGamePlayers, currentRoundPlayers and historicOfCommands

# Summary of context return a string that contains a short description of the state of that context.
  
class Context(cardgame.Context):

  def __init__(self):
    super(Context, self).__init__()
    # some variables
    self.flag = True
    # see method context on the round class (step to create the Round)
    
  def notify(self, event):
    super(Context, self).notify(event)
    # ...
  
  #import copy
  #Important: Clone objects to avoid that bad strategies change the model without commands

###############################################################################
# [required] 4) Card game logic

#################################
# [optional] 4.1): Define a model of reports to store informations.
 
# All reports already have: players, initialNumberOfPlayers, durationTime, winners
# GameReport has report of all rounds (good to debug and undertandings algorithms)

class GameReport(cardgame.GameReport):
  def __init__(self):
    super(GameReport, self).__init__()
  
#################################s
# [required] 4.2) Create the logic of the game

class Game(cardgame.Game):

  def __init__(self, players, configurations):
    commandsManager = commands.AsynchronousCommandsManager()
    commandsManager.registerCommand(FooCommand)
    super(Game, self).__init__(players, configurations, commandsManager, GameReport(), 
                               startCommand=StartGameCommand(), 
                               endCommand=EndGameCommand(), 
                               playerplaysCommand=PlayerPlaysGameCommand(),
                               roundClass=Round)
    
  def conditionToWin(self, player):
    # need implementation
    # Define a logic that return True if a player win this game, else returns False
    # Pay attention that this method is used by 'isTheEnd' and 'winners' methods
    pass

###############################################################################
# [required] 5) Round logic

#################################
# [optional] 5.1): Define a model of reports to store informations 
 
# All reports already have: players, initialNumberOfPlayers, durationTime, winners
# RoundReport has report of all commands (good to debug and undertandings algorithms)

class RoundReport(cardgame.RoundReport):
    def __init__(self):
      super(RoundReport, self).__init__()
  
#################################
# [required] 5.2) Create the logic of a round of the game:

class Round(cardgame.Round):

  def __init__(self, game, players, configurations, commandsManager):
    super(Round, self).__init__(game, players, configurations, commandsManager, RoundReport(),
                               startCommand=StartGameRoundCommand(), 
                               endCommand=EndGameRoundCommand(), 
                               playerplaysCommand=PlayerPlaysGameCommand()))
    self.flag = True

  def conditionToWin(self, player):
    # need implementation
    # Define a logic that return True if a player win this round, else returns False
    # Pay attention that this method is used by 'isTheEnd' and 'winners' methods
    pass

###############################################################################
# [required] 6): Define game's commands

class StartGameCommand(game.StartGameCommand):
  # Some work before the game/round is started, like give cards to players, community cards, chips, etc
  def execute(self, game):
    # some implementation here, example:
    pass
    
class EndGameCommand(game.EndGameCommand):
  # Some work after the game/round is finished, like log something in report or count points...
  def execute(self, game):
    # some implementation here, example:
    pass
    
class StartGameRoundCommand(game.StartGameCommand):
  # Some work before the game/round is started, like give cards to players, community cards, chips, etc
  def execute(self, game):
    # some implementation here, example:
    pass
    
class EndGameRoundCommand(game.EndGameCommand):
  # Some work after the game/round is finished, like log something in report or count points...
  def execute(self, game):
    # some implementation here, example:
    pass
    
class PlayerPlaysGameCommand(game.PlayerPlaysGameCommand):
  # Some work before a player plays, like clean variables
  def execute(self, game):
    # some implementation here, example:
    pass
    

###############################################################################
# [required] 7): Define player's commands

# Define errors:

# class CantHitError(errors.InvalidCommandError):
#  """Player cant hit"""
    
# class CheatError(errors.CheatCommandError):
#  """Invalid cards"""

class FooCommand(cardgame.PlayerCommand):

  def validate(self, context):
    # Must return InvalidCommandError if this command cant be executed in that context
    if context.flag == True: 
      raise CheatError(self)
    else:
      raise CantHitError(self)
  
  def call(self, game, round, playercards):
    # some implementation here, example:
    game.removePlayer(self.player)
    round.seeCards(self.player).sort()
    
###############################################################################
# [required] 8): Define strategies to a player

class Strategy(players.Strategy):

  def play(self, commandsManager):
    self.stepone(commandsManager)
    self.steptwo(commandsManager)
      
  def stepone(self, commandsManager):
    # implementation here, example:
    if self.context.flag == True:
      mycommand = FooCommand(self.player, 'some param, int, bool, str...')
      if mycommand.isValid(self.context):
        commandsManager.addCommand(mycommand)
    
  def steptwo(self, commandsManager):
    # implementation here, example:
    pass
    
# now you can instantiate your player with it: players.Player('Player', Strategy())
  
###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

# If necessary, use module utils that have useful algorithms

from gameengine import utils

###############################################################################
# [required] 10) Define a factory

class GameFactory(cardgame.GameFactory):
  
  def __init__(self):
    super(GameFactory, self).__init__(Game, Context, Configurations)

###############################################################################
# [have fun] 11) Play!
  
# example, file runner.py:
 
from cardgames import mygame

# Util for implement strategies
# from gameengine import players
# from cardgameengine import cards
# from gameengine import utils


strategyPlayer1 = u'source code'
strategyPlayer2 = mygame.Strategy()

# required
mapPlayersToStrategy = {'Player1': strategyPlayer1, 'Player2': strategyPlayer2} 

# [optional]
mapPlayersTeams = {'Player1': 'Team1', 'Player2': 'Team2'}

# optional
mapOfConfigurations = {'timeForCommand': -1, 'timeForPlay': -1, 'timeForGame': -1}


if __name__ == "__main__":
  game = mygame.Factory().createGame(mapPlayersToStrategy, mapPlayersTeams, mapOfConfigurations)
  try:
    game.start()
  finally:
    print(game.report().summary())
}}}

=Example of unit tests for your game=

{{{
}}}

=Source code=

Part of the code was written with TDD, another part use TAD ou TFD.

The source code has a lot of unit tests using one of the internal frameworks of Python: unittest.

In the source code, there are commentaries telling which design pattern a class or method represent, to facilitate the comprehension.
Here a list of some patterns used:
  
  * Builder
  * Collecting Parameter
  * Command
  * Prototype
  * State
  * Strategy
  * Template Method
  * Observer
  * Abstract Factory
  
Sometimes it used reflection/meta programming to instantiate objects.

Commands are synchonized with a queue, only one command can update the model at a time.

=Dependencies=

  * Python-DataObjects: http://code.google.com/p/python-dataobjects
  
'''
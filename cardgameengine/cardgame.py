'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

from string import Template
from gameengine import game, gameofrounds, players, commands, factory, utils
from cardgameengine import cards

###############################################################################

class Context(gameofrounds.Context):
  '''
  Example of usage:
  
  class Context(cardgame.Context):
    def __init__(self):
      super(Context, self).__init__()
      # other attributes here
      
    def notifyGameOfRoundsCommand(self, event):
      #need implementation
      pass
      
    def notifyRoundCommand(self, event):
      #need implementation
      pass
      
    def notifyPlayerCommand(self, event):
      #need implementation
      pass
  '''
  
  def __init__(self):
    super(Context, self).__init__()
    self.playercards = None
    
  # FIXME name only, aqui vem a estrategia junto so o nome, see cards of Player(name)?
  
  def notify(self, event):
    if isinstance(event.game, Round):
      self.playercards = event.game.seeCards(self.player)
    else:
      if event.game.currentRound is not None:
        self.playercards = event.game.currentRound.seeCards(self.player)
    super(Context, self).notify(event)
        
  def notifyGameOfRoundsCommand(self, event): pass
  def notifyRoundCommand(self, event): pass
  def notifyPlayerCommand(self, event): pass 
  
###############################################################################
    
class PlayerCommand(commands.PlayerCommand):
  '''
  Example of usage:
  
  class SomeCommand(cardgame.GameCommand):
    def validate(self, context):
      # need implementation
    
    def call(self, game, round, playercards):
      # need implementation
  '''

  def validate(self, context): pass
  
  def executeWithValidation(self, round):
    playercards = round.seeCards(self.player)
    self.call(round.game, round, playercards)

  def call(self, game, round, playercards): pass
  
###############################################################################

class RoundReport(gameofrounds.RoundReport):
  '''
  RoundReport has log of all commands (good to debug and undertandings algorithms)
  
  Example of usage:
  
  class RoundReport(cardgame.RoundReport):
    def __init__(self):
      super(RoundReport, self).__init__()
      # more attributes here
  '''
  
  def __init__(self):
    super(RoundReport, self).__init__()

    
###############################################################################

class GameReport(gameofrounds.GameOfRoundsReport):
  '''
  GameReport has report of all rounds (good to debug and undertandings algorithms)
  
  Example of usage:
  
  class GameReport(cardgame.GameReport):
    def __init__(self):
      super(GameReport, self).__init__()
      # more attributes here
  '''
  
  def __init__(self):
    super(GameReport, self).__init__()
    
###############################################################################
    
# Collecting Parameter: reportCollector
class Round(gameofrounds.GameRound):
  '''
  Example of Usage:
  
  class Round(cardgame.Round):

    def __init__(self, game, players, commandsManager, configurations=game.Configurations()): 
      super(Round, self).__init__(game, players, configurations, commandsManager,  
                                  RoundReport(),
                                  StartGameRoundCommand(), 
                                  EndGameRoundCommand(), 
                                  PlayerPlaysGameCommand())

    def conditionToWin(self, player):
      # need implementation
      # Define a logic that return True if a player win this round, else returns False
      pass
  '''
  
  def __init__(self, game, players, 
               configurations=game.Configurations(), 
               commandsManager=commands.SynchronousCommandsManager(),
               reportCollector=RoundReport(),
               startCommand=gameofrounds.StartGameRoundCommand(), 
               endCommand=gameofrounds.EndGameRoundCommand(), 
               playerplaysCommand=game.PlayerPlaysGameCommand()): 
    super(Round, self).__init__(game, players, configurations, commandsManager,
                               reportCollector, startCommand, endCommand, playerplaysCommand)
    self.deck = self.configurations.deckPrototype.clone()
    
    self.playersCards = {}
    for player in self.players:
      self.playersCards[player.name] = cards.StackOfCards()
      
    self.currentPlayer = None
    
  @classmethod
  def name(clazz):
    return clazz.__name__.replace('Round', '')
  
  def seeCards(self, player):
    if player == None: raise Exception('Player not found: ' + str(player))
    return self.playersCards[player.name]
  
  def distributeCardsToAllPlayers(self, amount):
    cards.distributeCards(self.deck, self.playersCards.values(), amount)
    
  def play(self):
    while len(self.players) > 0 and not self.isTheEnd():
      # FIXME One player at a time. This is a strategy of round, maybe it need to abstract this strategy
      for player in self.players:
        self.currentPlayer = player
        self.currentPlayerPlays()
        if self.isTheEnd(): # if a player finish the round
          break

  def currentPlayerPlays(self):
    self.playerPlays(self.game.commandsManager, self.currentPlayer)
        
  def whoIsPlaying(self):
    return self.currentPlayer
  
  def conditionToWin(self, player): raise NotImplementedError()

###############################################################################

class Configurations(gameofrounds.GameOfRoundsConfigurations):
  def __init__(self, deckPrototype, timeForCommand=-1, timeForPlay=-1, timeForGame=-1, numberOfRounds=-1):
    '''
    Example of usage:
    
    class Configurations(cardgame.Configurations):
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
      
      deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(Card, 4, 13, 1, 0, scoreFunction)
      
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
      # super(Configurations, self).__init__(deckPrototype[, timeForCommand=-1]
      #                                      [, timeForPlay=-1][, timeForGame=-1],
      #                                      [, numberOfRounds=-1])
      super(Configurations, self).__init__(deckPrototype, timeForCommand, timeForPlay, timeForGame, numberOfRounds)
      # other attributes here
    '''
    super(Configurations, self).__init__(timeForCommand, timeForPlay, timeForGame, numberOfRounds)
    self.deckPrototype = deckPrototype
    
###############################################################################
    
# Observer pattern: Observable
# Collecting Parameter: reportCollector
class Game(gameofrounds.GameOfRounds):
  '''
  Example of Usage:
  
  class Game(cardgame.Game):
  
    def __init__(self, players, 
                 configurations=GameOfRoundsConfigurations()): 
      super(Game, self).__init__(players, configurations, commands.SynchronousCommandsManager(),  
                                 GameReport(),StartGameCommand(), EndGameCommand(), PlayerPlaysGameCommand(), Round)
                                 
    def conditionToWin(self, player):
      # need implementation
      # Define a logic that return True if a player win this game, else returns False
      pass
  '''

  def __init__(self, players, 
               configurations=gameofrounds.GameOfRoundsConfigurations(), 
               commandsManager=commands.SynchronousCommandsManager(),
               reportCollector=GameReport(),
               startCommand=game.StartGameCommand(), 
               endCommand=game.EndGameCommand(), 
               playerplaysCommand=game.PlayerPlaysGameCommand(),
               roundClass=Round): 
    super(Game, self).__init__(players, configurations, commandsManager,
                               reportCollector, startCommand, endCommand, playerplaysCommand, roundClass)
  
  @classmethod
  def name(clazz):
    return clazz.__name__.replace('CardGame', '')
  
  # State
  def whoIsPlaying(self):
    if self.currentRound == None: raise Exception('Game not started')
    return self.currentRound.whoIsPlaying()
  
  def conditionToWin(self, player): raise NotImplementedError()
  
###############################################################################

class CardUtils(game.Utils):
  pass

###############################################################################
# [required] 10) Define a factory

accessibleClasses = [utils.CombinationGenerator, cards.StackOfCards]

class GameFactory(factory.GameFactory):
  
  def __init__(self, gameClass=Game, contextClass=Context, configurationsClass=Configurations, accessibleClasses=accessibleClasses):
    super(GameFactory, self).__init__(gameClass, contextClass, configurationsClass, accessibleClasses)
    
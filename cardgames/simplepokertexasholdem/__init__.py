'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

import string
from gameengine import game, utils, commands, players, errors, utils
from cardgameengine import cardgame, cards
from cardgameengine.constants import *

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class Card(cards.SuitCard):
  values = cards.VALUES_ANGLO_AMERICAN
  suits = cards.SUITS_ANGLO_AMERICAN
  
###############################################################################
# [required] 2) Define configurations of the game

class Configurations(cardgame.Configurations):
  
  def __init__(self, amountOfChipsPerPlayer=1000, roundsPrice=10, maxBet=100,
               timeForCommand=-1, timeForPlay=-1, timeForGame=-1):
    deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(Card, 4, 13, 1, 0)
    super(Configurations, self).__init__(deckPrototype, timeForCommand, timeForPlay, timeForGame)
    self.amountOfChipsPerPlayer = amountOfChipsPerPlayer
    self.roundsPrice = roundsPrice
    self.maxBet = maxBet
    
###############################################################################
# [required] 3): Define the context of a player

class Context(cardgame.Context):
  
  def __init__(self):
    super(Context, self).__init__()
    self.step = 0
    self.playersChips = {}
    self.communityCards = None
    self.pot = 0
    self.bigBet = 0
    self.currentPlayerDecided = False

  def notifyGameOfRoundsCommand(self, event): pass
  def notifyRoundCommand(self, event): pass
  def notifyPlayerCommand(self, event):
    round = event.game
    self.playersChips = round.game.playersChips
    self.step = round.step
    self.communityCards = round.communityCards
    self.pot = round.pot
    self.bigBet = round.bigBet
    self.currentPlayerDecided = round.currentPlayerDecided
    
  def summary(self):
    t = string.Template(
'''
Round ${numberOfRounds} Step ${step} - ${player} - ${playercards}:
- Players Chips: ${playersChips}
- Community Cards: ${communityCards}
- Pot: ${pot}
- Big bet: ${bigBet}
''')
    return t.substitute(numberOfRounds=self.numberOfRounds,
                        player=self.player.name,
                        playercards=str(self.playercards),
                        step=self.step,
                        playersChips=', '.join((player + ' ' + str(chips)) for player, chips in self.playersChips.items()),
                        communityCards=str(self.communityCards),
                        pot=self.pot,
                        bigBet=self.bigBet)
    
###############################################################################
# [required] 4) Card game logic

#################################
# [optional] 4.1): Define a model of reports to store informations.
 
class GameReport(cardgame.GameReport):
  def __init__(self):
    super(GameReport, self).__init__()
  
#################################s
# [required] 4.2) Create the logic of the game

class SimpleCommunityPoker(cardgame.Game):

  def __init__(self, players, configurations):
    commandsManager = commands.SynchronousCommandsManager()
    commandsManager.registerCommand(FoldCommand)
    commandsManager.registerCommand(FoldShowingTheCardsCommand)
    commandsManager.registerCommand(BetCommand)
    commandsManager.registerCommand(PayCommand)
    commandsManager.registerCommand(AllInCommand)
    commandsManager.registerCommand(StepCommand)
    super(SimpleCommunityPoker, self).__init__(players, configurations, commandsManager, GameReport(), 
                               startCommand=StartGameCommand(), 
                               endCommand=EndGameCommand(), 
                               playerplaysCommand=PlayerPlaysGameCommand(),
                               roundClass=Round)
    self.playersChips = {}
    for player in players:
      self.playersChips[player.name] = 0

  def amountOfChips(self, player):
    return self.playersChips[player.name]

  def conditionToWin(self, player):
    return self.numberOfPlayers() == 1 and player in self.players

###############################################################################
# [required] 5) Round logic

#################################
# [optional] 5.1): Define a model of reports to store informations 
 
class RoundReport(cardgame.RoundReport):
    def __init__(self):
      super(RoundReport, self).__init__()
      self.typeWinnerCombination = None
  
#################################
# [required] 5.2) Create the logic of a round of the game:

class Round(cardgame.Round):

  def __init__(self, game, players, configurations, commandsManager):
    super(Round, self).__init__(game, players, configurations, commandsManager, RoundReport(),
                               startCommand=StartGameRoundCommand(), 
                               endCommand=EndGameRoundCommand(), 
                               playerplaysCommand=PlayerPlaysGameCommand())
    self.stepCommand = StepCommand()
    self.step = 0
    self.communityCards = StackOfCards()
    self.pot = 0
    self.currentPlayerDecided = False
    self.bigBet = 0
    self.winnerCombination = None
    
  def conditionToWin(self, player):
    return (self.numberOfPlayers() == 1 and player in self.players) or \
          (self.winnerCombination is not None and \
           self.bestCombination(player) >= self.winnerCombination)

  def showdown(self):
    self.winnerCombination = self.bestCombination(self.players[0])
    for player in self.players:
      combination = self.bestCombination(player)
      if combination > self.winnerCombination:
        self.winnerCombination = combination

  def bestCombination(self, player):
    combinations = self.possibleCombinations(player)
    bestCombination = CombinationFactory.create(combinations[0])
    for combination in combinations:
      c = CombinationFactory.create(combination)
      if c > bestCombination:
        bestCombination = c
    return bestCombination
        
  def possibleCombinations(self, player):
    combinations = []
    generator = utils.CombinationGenerator(5, 3)
    while generator.hasNext():
      combination = StackOfCards()
      combination.pushAll(self.seeCards(player))
      for i in generator.next():
        combination.push(self.communityCards.see(i))
        combinations.append(combination)
    return combinations

  def play(self):
    while len(self.players) > 0 and not self.isTheEnd():
      # FIXME One player at a time. This is a strategy of round, maybe it need to abstract this strategy
      for player in self.players:
        self.currentPlayer = player
        self.currentPlayerPlays()
        if self.isTheEnd(): # if a player finish the round
          break
      self.commandsManager.addCommand(self.stepCommand)


###############################################################################
# [required] 6): Define game's commands

class StartGameCommand(game.StartGameCommand):

  def execute(self, game):
    for player in game.players:
      game.playersChips[player.name] = game.configurations.amountOfChipsPerPlayer
    
class EndGameCommand(game.EndGameCommand):

  def execute(self, game): pass
    
class StartGameRoundCommand(game.StartGameCommand):

  # FIXME tests
  def execute(self, round):
    for player in round.players:
      if round.game.playersChips[player.name] < round.game.configurations.roundsPrice:
        round.game.removePlayer(player)
      else:
        round.game.playersChips[player.name] -= round.game.configurations.roundsPrice
        round.pot += round.game.configurations.roundsPrice
    
class EndGameRoundCommand(game.EndGameCommand):

  def execute(self, round):
    winners = round.winners()
    division = len(winners)
    for winner in winners:
      round.game.playersChips[winner.name] += (float(round.pot) / division)
    round.pot = 0
    
class PlayerPlaysGameCommand(game.PlayerPlaysGameCommand):

  def execute(self, round):
    round.currentPlayerDecided = False

class StepCommand(game.PlayerPlaysGameCommand):

  def execute(self, round):
    if round.step == 0:
      round.deck.shuffle()
      round.distributeCardsToAllPlayers(2)
      round.communityCards.push(round.deck.pop())
      round.communityCards.push(round.deck.pop())
      round.communityCards.push(round.deck.pop())
      # self.roundsPrice = roundsPrice FIXME
      # tests, if a player dont have money? all in?
    elif round.step == 1:
      round.communityCards.push(round.deck.pop())
    elif round.step == 2:
      round.communityCards.push(round.deck.pop())
    else:
      round.showdown()
    round.step += 1

###############################################################################
# [required] 7): Define player's commands

# Define errors:

class AlreadyDecidedInvalidCommandError(errors.InvalidCommandError):
  """Player have already been decided"""
  
class BadBetValueInvalidCommandError(errors.InvalidCommandError):
  """Player is trying to bet a value bigger than the permitted"""
  
class InsuficientBetValueInvalidCommandError(errors.InvalidCommandError):
  """Player is trying to bet few chips without all-in"""
  
class IllegalBetValueInvalidCommandError(errors.CheatCommandError):
  """Player is trying to bet more chips than he/she has"""
  
class PokerCommand(cardgame.PlayerCommand):
  
  def validate(self, context):
    if context.currentPlayerDecided:
      raise AlreadyDecidedInvalidCommandError(self)
  
  def call(self, game, round, playercards): pass

class FoldCommand(PokerCommand):

  def call(self, game, round, playercards):
    round.removePlayer(self.player)
  
class FoldShowingTheCardsCommand(PokerCommand):

  def call(self, game, round, playercards):
    round.removePlayer(self.player)
  
class BetCommand(PokerCommand):

  def validate(self, context):
    super(BetCommand, self).validate(context) # FIXME tests
    if self.params > context.configurations.maxBet:
      raise BadBetValueInvalidCommandError(self)
#    if self.params < 1000 and self.params != context.playersChips[self.player.name]: # FIXME all in
#      raise InsuficientBetValueInvalidCommandError(self)
#    if self.params > context.playersChips[self.player.name]:
#      raise IllegalBetValueInvalidCommandError(self)

  def call(self, game, round, playercards):
    round.pot += self.params
    game.playersChips[self.player.name] -= self.params
  
#Call
class PayCommand(BetCommand):

  def call(self, game, round, playercards):
    pass # FIXME
  
class AllInCommand(BetCommand):

  def call(self, game, round, playercards):
    round.pot += game.playersChips[self.player.name]
    game.playersChips[self.player.name] = 0
    
###############################################################################
# [required] 8): Define strategies to a player

class Strategy(players.Strategy):

  def play(self, commandsManager):
    self.compulsoryBets(commandsManager)
    self.preFlop(commandsManager)
    self.flop(commandsManager)
    self.turn(commandsManager)
    self.river(commandsManager)

  # Let the developer implement this methods with his stratagies
  def compulsoryBets(self, commandsManager): pass
  def preFlop(self, commandsManager): pass
  def flop(self, commandsManager): pass
  def turn(self, commandsManager): pass
  def river(self, commandsManager): pass
    
###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

class StackOfCards(cards.StackOfCards):

  def isSequence(self):
    if self.allCardsInSequence(): return True
    c = StackOfCards()
    c.pushAll(self.cards)
    # 10 J Q K AS
    if c.containsCardWithValue(1): # AS
      cardAS = c.popIndex(0)
      c.push(cards.Card(14, cardAS.suit))
      if c.allCardsInSequence(): return True
    return False

  def isValidCombination(self):
    return self.height() == 5
  
  def isRoyalStraigthFlush(self):
    return  self.isValidCombination() and \
            self.allCardsInSequenceWithSameSuit() and \
            self.containsCardWithValue(1) and \
            self.containsCardWithValue(13)
  
  def isStraigthFlush(self):
    return self.isValidCombination() and self.isSequence() and self.allCardsWithSameSuit()
  
  def isFourOfAKind(self):
    self.sortByValue()
    return self.isValidCombination() and \
            (self.numberOfCards(self.seeFirstCard()) == 4 or 
            self.numberOfCards(self.seeLastCard()) == 4)
    
  def isFullHouse(self):
    self.sortByValue()
    return self.isValidCombination() and \
      (self.numberOfCards(self.seeFirstCard()) == 2 and self.numberOfCards(self.seeLastCard()) == 3) or \
      (self.numberOfCards(self.seeFirstCard()) == 3 and self.numberOfCards(self.seeLastCard()) == 2)
    
  def isFlush(self):
    return self.isValidCombination() and self.allCardsWithSameSuit()
  
  def isStraigth(self):
    return self.isValidCombination() and self.isSequence()
  
  def isThreeOfAKind(self):
    self.sortByValue()
    return self.isValidCombination() and \
      not self.isFullHouse() and \
      (self.numberOfCardsWithValue(self.see(0).value) == 3 or \
       self.numberOfCardsWithValue(self.see(1).value) == 3 or \
       self.numberOfCardsWithValue(self.see(2).value) == 3)
  
  def isTwoPair(self):
    self.sortByValue()
    return self.isValidCombination() and \
      not self.isFourOfAKind() and \
      ((self.numberOfCardsWithValue(self.see(0).value) == 2 and self.numberOfCardsWithValue(self.see(2).value) == 2) or \
       (self.numberOfCardsWithValue(self.see(1).value) == 2 and self.numberOfCardsWithValue(self.see(3).value) == 2))
  
  def isPair(self):
    self.sortByValue()
    return self.isValidCombination() and \
      not self.isFourOfAKind() and not self.isTwoPair() and \
      (self.numberOfCardsWithValue(self.see(0).value) == 2 or \
       self.numberOfCardsWithValue(self.see(1).value) == 2 or \
       self.numberOfCardsWithValue(self.see(2).value) == 2 or \
       self.numberOfCardsWithValue(self.see(3).value) == 2)
  
  def isHighCard(self):
    return self.isValidCombination() and \
            not self.isRoyalStraigthFlush() and not self.isStraigthFlush() and \
            not self.isFourOfAKind() and not self.isFullHouse() and \
            not self.isFlush() and not self.isStraigth() and \
            not self.isThreeOfAKind() and not self.isTwoPair() and not self.isPair()
            
class Combination(object):
  
  def __init__(self, stack):
    self.stack = stack
    self.stack.sortByValue()
    
  def __lt__(self, that): return self.compare(that) < 0
  def __le__(self, that): return self.compare(that) <= 0
  def __gt__(self, that): return not self.__le__(that)
  def __ge__(self, that): return not self.__lt__(that)
    
  def compare(self, that):
    order = CombinationFactory.order
    if order.index(self.__class__) == order.index(that.__class__): return self.untie(that)
    return order.index(self.__class__) - order.index(that.__class__)
    
  def untie(self, that): pass
  
class RoyalStraigthFlush(Combination):
  def untie(self, that):
    return 0
  
class StraigthFlush(Combination):
  def untie(self, that):
    return self.stack.compareByHighValue(that.stack)
  
class FourOfAKind(Combination):
  def untie(self, that):
    if self.stack.see(2).value - that.stack.see(2).value == 0: return 0
    aux = self.stack.clone()
    aux.popCardsWithValue(self.stack.see(2).value)
    thataux = that.stack.clone()
    thataux.popCardsWithValue(that.stack.see(2).value)
    return aux.compareByHighValue(thataux)
  
class FullHouse(Combination):
  def untie(self, that):
    if self.stack.see(2).value - that.stack.see(2).value == 0: return 0
    aux = self.stack.clone()
    aux.popCardsWithValue(self.stack.see(2).value)
    thataux = that.stack.clone()
    thataux.popCardsWithValue(that.stack.see(2).value)
    return aux.compareByHighValue(thataux)
  
class Flush(Combination):
  def untie(self, that):
    return self.stack.compareByHighValue(that.stack)
  
class Straigth(Combination):
  def untie(self, that):
    return self.stack.compareByHighValue(that.stack)
  
class ThreeOfAKind(Combination):
  def untie(self, that):
    if self.stack.see(2).value - that.stack.see(2).value == 0: return 0
    aux = self.stack.clone()
    aux.popCardsWithValue(self.stack.see(2).value)
    thataux = that.stack.clone()
    thataux.popCardsWithValue(that.stack.see(2).value)
    return aux.compareByHighValue(thataux)
  
class TwoPair(Combination): 
  def getValueOfPairs(self, stack):
    if stack.see(4) == stack.see(3): # AABCC or ABBCC
      highestPairValue = stack.see(4).value
      if stack.see(2) == stack.see(1): # ABBCC
        lowestPairValue = stack.see(2).value
      else:
        lowestPairValue = stack.see(0).value # AABCC
    else: # AABBC
      highestPairValue = stack.see(3).value
      lowestPairValue = stack.see(0).value
    return (lowestPairValue, highestPairValue)
  
  def untie(self, that):
    selfPairValues = self.getValueOfPairs(self.stack)
    thatPairValues = self.getValueOfPairs(that.stack)
    highPairDifference = selfPairValues[1] - thatPairValues[1]
    if highPairDifference != 0: return highPairDifference
    lowerPairDifference = selfPairValues[0] - thatPairValues[0]
    if lowerPairDifference != 0: return lowerPairDifference
    return self.stack.compareByHighValue(that.stack)
  
class Pair(Combination): # AABCD ABBCD ABCCD ABCDD
  def getValueOfPair(self, stack):
    for card1, card2 in zip(stack.cards, stack.cards[1:]):
      if card1.value == card2.value: 
        return card1.value
      
  def untie(self, that):
    pairDifference = self.getValueOfPair(self.stack) - self.getValueOfPair(that.stack)
    if pairDifference != 0: return pairDifference
    return self.stack.compareByHighValue(that.stack)
  
class HighCard(Combination):
  def untie(self, that):
    return self.stack.compareByHighValue(that.stack)

class CombinationFactory(object):

  order = [RoyalStraigthFlush, StraigthFlush, FourOfAKind, FullHouse, 
                Flush, Straigth, ThreeOfAKind, TwoPair, Pair, HighCard]
  
  @staticmethod
  def create(stack):
    if stack.isRoyalStraigthFlush(): return RoyalStraigthFlush(stack)
    if stack.isStraigthFlush(): return StraigthFlush(stack)
    if stack.isFourOfAKind(): return FourOfAKind(stack)
    if stack.isFullHouse(): return FullHouse(stack)
    if stack.isFlush(): return Flush(stack)
    if stack.isStraigth(): return Straigth(stack)
    if stack.isThreeOfAKind(): return ThreeOfAKind(stack)
    if stack.isTwoPair(): return TwoPair(stack)
    if stack.isPair(): return Pair(stack)
    if stack.isHighCard(): return HighCard(stack)
    raise Exception('Invalid combination')

###############################################################################
# [required] 10) Define a factory

class GameFactory(cardgame.GameFactory):
  
  def __init__(self):
    super(GameFactory, self).__init__(SimpleCommunityPoker, Context, Configurations)

'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import copy
from string import Template
from gameengine import game, gameofrounds, commands, players, utils, errors
from cardgameengine import cardgame, cards

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class Card(cards.SuitCard):
  values = cards.VALUES_ANGLO_AMERICAN
  suits = cards.SUITS_ANGLO_AMERICAN
  
###############################################################################
# [optional] 2) Define configurations of the game

class Configurations(cardgame.Configurations):

  def __init__(self, maximumScore=1000, numberOfDeads=2, timeForCommand=-1, timeForPlay=-1, timeForGame=-1):
    def scoreFunction(value, suit):
      if value == 0: return 20
      if value == 1: return 15
      if value == 2: return 10
      if value >= 3 and value <= 7: return 5
      if value >= 8 and value <= 13: return 10
      return 0
      
    deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(Card, 4, 13, 2, 2, scoreFunction)
    super(Configurations, self).__init__(deckPrototype, timeForCommand, timeForPlay, timeForGame)
    
    self.maximumScore = maximumScore
    self.numberOfDeads = numberOfDeads
    
###############################################################################
# [required] 3): Define the context of a player

class Context(cardgame.Context):
  
  def __init__(self):
    super(Context, self).__init__()
    self.teamsScores = {} # map team name -> score
    self.deckHeight = 0 # int
    self.numberOfCardsOfAnothersPlayers = {} # map player name -> number of cards
    self.numberOfCardsOfAnothersTeams = {} # map team name -> number of cards
    self.discardedCards = None # cards.StackOfCards
    self.teamsCombinations = {} # map team name -> list of StackOfCards
    self.numberOfDeads = 0 # int
    self.teamsHaveAlreadyHit = [] # list of team names
    self.playersHaveAlreadyHit = [] # list of player names
    self.currentPlayerHasAlreadyGetCards = False # Boolean
    self.currentPlayerHasAlreadyDiscarded = False # Boolean
  
  # Methods:
  # teamHasCanastra(team)
  # teamCanHit(team)
  
  def teamHasCanastra(self, team):
    for combination in self.teamsCombinations[team.name]:
      if combination.height() >= 7:
        return True
    return False
  
  def teamCanHit(self, team):
    return self.teamHasCanastra(team) or \
          (team.name not in self.teamsHaveAlreadyHit and self.numberOfDeads > 0)

  def notifyGameOfRoundsCommand(self, event): pass
    
  def notifyRoundCommand(self, event):
    round = event.game
    if round != None:
      self.teamsScores = copy.deepcopy(round.game.teamsScores)
      self.deckHeight = round.deck.height()
      for player in round.players:
        self.numberOfCardsOfAnothersPlayers[player.name] = round.seeCards(player).height()
        if player.team.name not in self.numberOfCardsOfAnothersTeams:
          self.numberOfCardsOfAnothersTeams[player.team.name] = 0
        self.numberOfCardsOfAnothersTeams[player.team.name] += round.seeCards(player).height()
      self.discardedCards = StackOfCards(copy.deepcopy(round.discardedCards))
      self.teamsCombinations = copy.deepcopy(round.teamsCombinations)
      self.numberOfDeads = len(round.deads)
      self.teamsHaveAlreadyHit = copy.deepcopy(round.teamsHaveAlreadyHit)
      self.playersHaveAlreadyHit = copy.deepcopy(round.playersHaveAlreadyHit)
      self.currentPlayerHasAlreadyGetCards = round.currentPlayerHasAlreadyGetCards
      self.currentPlayerHasAlreadyDiscarded = round.currentPlayerHasAlreadyDiscarded
      self.playercards = StackOfCards(self.playercards)
    
  def notifyPlayerCommand(self, event):
    self.notifyRoundCommand(event)
  
#    print('NAOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
      
#  start round: deckHeight, numberOfCardsOfAnothersPlayers, discardedCards, 
#  teamsCombinations, numberOfDeads, teamsHaveAlreadyHit, playersHaveAlreadyHit, currentPlayerHasAlreadyGetCards
#  currentPlayerHasAlreadyDiscarded, playercards
#  
#  player play: currentPlayerHasAlreadyGetCards, currentPlayerHasAlreadyDiscarded
#  end round: teamsScores
#  compra: deckHeight, numberOfCardsOfAnothersPlayers, currentPlayerHasAlreadyGetCards, playercards
#  baixa: numberOfCardsOfAnothersPlayers, teamsCombinations, numberOfDeads, teamsHaveAlreadyHit, playersHaveAlreadyHit, playercards
#  descarta: numberOfCardsOfAnothersPlayers, discardedCards, numberOfDeads, teamsHaveAlreadyHit, playersHaveAlreadyHit, currentPlayerHasAlreadyDiscarded, playercards

###############################################################################
# [required] 4) Card game logic

#################################
# [optional] 4.1): Define a model of reports to store informations.

class GameReport(cardgame.GameReport):
  
  def __init__(self):
    super(GameReport, self).__init__()
    self.numberOfCanastras = 0
#  composite round
#qtde de canastras limpas, sujas, etc
#qtde de pontos
#qtde de coringas
 # FIXME

#################################s
# [required] 4.2) Create the logic of the game

class Game(cardgame.Game):

  def __init__(self, players, configurations):
    commandsManager = commands.SynchronousCommandsManager()
    commandsManager.registerCommand(GetOneCardOfTheDeckCommand)
    commandsManager.registerCommand(GetDiscardedCardsCommand)
    commandsManager.registerCommand(DiscardCommand)
    commandsManager.registerCommand(MakeNewCombinationCommand)
    commandsManager.registerCommand(PutCardsInCombinationCommand)
    super(Game, self).__init__(players, configurations, commandsManager,
                               GameReport(),
                               game.StartGameCommand(), 
                               game.EndGameCommand(), 
                               game.PlayerPlaysGameCommand(), Round)
    self.teamsScores = {}
    
    for player in self.players:
      if not player.team.name in self.teamsScores:
        self.teamsScores[player.team.name] = 0
  
  @classmethod
  def name(clazz):
    return 'Hole'
  
  def seeScore(self, team):
    return self.teamsScores[team.name]
    
  def sumScore(self, team, score):
    self.teamsScores[team.name] += score
    
  def conditionToWin(self, player):
    score = self.teamsScores[player.team.name]
    # if more than one team pass the limit, so the biggest score wins
    return score >= self.configurations.maximumScore and score >= max(self.teamsScores.values()) 
  
###############################################################################
# [required] 5) Round logic

#################################
# [optional] 5.1): Define a model of reports to store informations

class RoundReport(cardgame.RoundReport):
  
  def __init__(self):
    super(RoundReport, self).__init__()
#qtde de canastras limpas sujas, etc
#qtde de pontos
#qtde de coringas
 # FIXME

#################################
# [optional] 5.2): Round 

class Round(cardgame.Round):

  def __init__(self, game, players,  configurations, commandsManager):
    super(Round, self).__init__(game, players, configurations, commandsManager,
                               RoundReport(), StartGameRoundCommand(), 
                               EndGameRoundCommand(), PlayerPlaysGameRoundCommand())
    self.discardedCards = cards.StackOfCards()
    self.teamsCombinations = {} # { team => [stack]}
    self.deads = []
    self.teamsHaveAlreadyHit = []
    self.playersHaveAlreadyHit = []
    self.currentPlayerHasAlreadyGetCards = False
    self.currentPlayerHasAlreadyDiscarded = False
    
    for x in range(self.configurations.numberOfDeads):
      self.deads.append(cards.StackOfCards())
      
    for player in players:
      if not player.team.name in self.teamsCombinations:
        self.teamsCombinations[player.team.name] = []

  def addNewCombination(self, player, combination):
    self.teamsCombinations[player.team.name].append(combination)

  def seeCombination(self, player, index):
    return self.teamsCombinations[player.team.name][index]
  
  def hit(self, player):
    teamsHaveAlreadyHit.append(player.team.name)
    playersHaveAlreadyHit.append(player.name)
    if not player.team in teamsHaveAlreadyHit and len(self.deads) > 0:
      player.pushAll(deads.pop())
    # else, do nothing: player with 0 cards finish the round

  def currentPlayerPlays(self):
    self.currentPlayerHasAlreadyGetCards = False
    self.currentPlayerHasAlreadyDiscarded = False
    super(Round, self).currentPlayerPlays() # FIXME BUG, need notify

  def conditionToWin(self, player):
    return self.seeCards(player).height() == 0

###############################################################################
# [required] 6): Define game's commands

class StartGameRoundCommand(gameofrounds.StartGameRoundCommand):
  
  def execute(self, round):
    round.deck.shuffle()
    round.distributeCardsToAllPlayers(11)
    cards.distributeCards(round.deck, round.deads, 11)
    # como diferenciar primeiro round dos demais? organize? # FIXME context first round
    
class EndGameRoundCommand(gameofrounds.EndGameRoundCommand):
  
  def execute(self, round):
    for player,cards in round.playersCards:
      round.game.sumScore(player.team, - cards.score())
    for team,combinations in round.teamsCombinations:
      for combination in combinations:
        round.game.sumScore(team, combination.score() + scoreOfCanastra(combination))
    for team in round.teamsCombinations:
      if not team in teamsHaveAlreadyHit:
        round.game.sumScore(team, -100)
    
class PlayerPlaysGameRoundCommand(game.PlayerPlaysGameCommand):
  
  def execute(self, round):
    round.currentPlayerHasAlreadyGetCards = False
    round.currentPlayerHasAlreadyDiscarded = False
  
  
###############################################################################
# [required] 7): Define player's commands

class GetCardsError(errors.InvalidCommandError):
  '''Player has already been gotten cards'''
    
class DiscardCardsError(errors.InvalidCommandError):
  '''Player has already been discarded a card'''
    
class NotGetCardsError(errors.InvalidCommandError):
  '''Player has not been gotten cards'''
    
class NotDiscardCardsError(errors.InvalidCommandError):
  '''Player has not been discarded a card'''

class EmptyDeckError(errors.InvalidCommandError):
  '''Deck is empty'''
    
class DiscardedCardsEmptyError(errors.InvalidCommandError):
  '''No discarded cards'''
    
class InvalidCombinationError(errors.InvalidCommandError):
  '''Invalid combination'''
    
class CantHitError(errors.InvalidCommandError):
  '''Player cant hit'''
    
class CheatError(errors.CheatCommandError):
  '''Invalid cards'''

class GetOneCardOfTheDeckCommand(cardgame.PlayerCommand):
  
  def validate(self, context):
    if context.currentPlayerHasAlreadyGetCards: raise GetCardsError(self)
    if context.deckHeight == 0: raise EmptyDeckError(self)
  
  def call(self, game, round, playercards):
    playercards.push(round.deck.pop())
    round.currentPlayerHasAlreadyGetCards = True
    
class GetDiscardedCardsCommand(cardgame.PlayerCommand):
  
  def validate(self, context):
    if context.currentPlayerHasAlreadyGetCards: raise GetCardsError(self)
    if context.discardedCards.height() == 0: raise DiscardedCardsEmptyError(self)
  
  def call(self, game, round, playercards):
    playercards.pushAll(round.discardedCards.popAll())
    round.currentPlayerHasAlreadyGetCards = True
    

class DiscardCommand(cardgame.PlayerCommand):
  
  def validate(self, context):
    if not context.currentPlayerHasAlreadyGetCards: raise NotGetCardsError(self)
    if context.currentPlayerHasAlreadyDiscarded: raise DiscardCardsError(self)
    goingToHit = context.playercards.height() == 1
    if not context.teamCanHit(self.player.team) and goingToHit: raise CantHitError(self)
    if not context.playercards.containsCard(self.params): raise CheatError(self)
  
  def call(self, game, round, playercards):
    card = self.params
    round.discardedCards.push(playercards.popCard(card))
    round.currentPlayerHasAlreadyDiscarded = True
    if playercards.height() == 0: round.hit(player)
    
class MakeNewCombinationCommand(cardgame.PlayerCommand):
  
  def validate(self, context):
    selectedCards = self.params
    aux = StackOfCards()
    aux.pushAll(selectedCards)
    
    if not context.currentPlayerHasAlreadyGetCards: raise NotGetCardsError(self) 
    if context.currentPlayerHasAlreadyDiscarded: raise DiscardCardsError(self)
    if not context.playercards.containsAllCards(selectedCards): raise CheatError(self)
    if not aux.isValidCombination(): raise InvalidCombinationError(self)
    goingToHit = context.playercards.height() == aux.height()
    if not context.teamCanHit(self.player.team) and goingToHit: raise CantHitError(self)
  
  def call(self, game, round, playercards):
    selectedCards = self.params
    newCombination = cards.StackOfCards()
    newCombination.pushAll(playercards.popCards(selectedCards))
    newCombination.sortByValueAndSuit()
    round.addNewCombination(self.player, newCombination)
    if playercards.height() == 0: round.hit(player)
    
class PutCardsInCombinationCommand(cardgame.PlayerCommand):
  
  def validate(self, context):
    combinationIndex = self.params[0]
    selectedCards = cards.StackOfCards()
    selectedCards.pushAll(self.params[1])
    combination = context.teamsCombinations[self.player.team.name][combinationIndex]
    aux = StackOfCards()
    aux.pushAll(combination)
    aux.pushAll(selectedCards)
    if not context.currentPlayerHasAlreadyGetCards: raise NotGetCardsError(self)
    if context.currentPlayerHasAlreadyDiscarded: raise DiscardCardsError(self)
    if not context.playercards.containsAllCards(selectedCards): raise CheatError(self)
    if not aux.isValidCombination(): raise InvalidCombinationError(self)
    goingToHit = context.playercards.height() == selectedCards.height()
    if not context.teamCanHit(self.player.team) and goingToHit: raise CantHitError(self)
  
  def call(self, game, round, playercards):
    combinationIndex = self.params[0]
    selectedCards = self.params[1]
    combination = round.seeCombination(self.player, combinationIndex)
    combination.pushAll(playercards.popCards(selectedCards))
    combination.sortByValueAndSuit()
    if playercards.height() == 0: round.hit(player)
    
###############################################################################
# [required] 8): Define strategies to a player

class Strategy(players.Strategy):
  '''
  ==Implement this methods==
  def getCardFromDeckOrCardsFromDiscardedCards(self, addCommand, context): pass
  def createCombinations(self, addCommand, context): pass
  def discard(self, addCommand, context): pass
  
  ==Accessible informations==
  self.context.property:
  
  teamsScores = {} # map team name -> score
  deckHeight = 0 # int
  numberOfCardsOfAnothersPlayers = {} # map player name -> number of cards
  numberOfCardsOfAnothersTeams = {} # map team name -> number of cards
  discardedCards = None # cards.StackOfCards
  teamsCombinations = {} # map team name -> list of StackOfCards
  numberOfDeads = 0 # int
  teamsHaveAlreadyHit = [] # list of team names
  playersHaveAlreadyHit = [] # list of player names
  currentPlayerHasAlreadyGetCards = False
  currentPlayerHasAlreadyDiscarded = False
  teamHasCanastra(team)
  teamCanHit(team)
  
  # game
  player = None
  currentGamePlayers = None
  configurations = None
  # cardgame
  playercards = None
  currentRoundPlayers = None
  
  ==Commands==
  hole.command:
  
  GetDiscardedCardsCommand(self.player, None)
  GetOneCardOfTheDeckCommand(self.player, None)
  PutCardsInCombinationCommand(self.player, [combination-index, [cards]])
  MakeNewCombinationCommand(self.player, stack)
  DiscardCommand(self.player, card)
  
  ==Useful methods==
  StackOfCards().isSequenceWithSameSuit()
  StackOfCards().isSequenceWithSameSuitWithOneJoker()
  StackOfCards().isCombinationOfJokers()
  StackOfCards().isCombinationWithSameValue()
  StackOfCards().isCombinationWithSameValueWithOneJoker()
  StackOfCards().isValidCombination()
  
  StackOfCards().isCanastra()
  StackOfCards().isCleanCanastra()
  StackOfCards().isCanastraWithJoker()
  StackOfCards().isRealCanastra()
  StackOfCards().isCanastraOfJokers()
  StackOfCards().scoreOfCanastra()
  
  StackOfCards().allValidCombinationOfCards() => [s]
  StackOfCards.orderCombinationsByScore(listOfStacks)
  StackOfCards.orderCombinationsByNumberOfCards(listOfStacks)
  StackOfCards.orderCombinationsByNumberOfCardsAndScore(listOfStacks)
  StackOfCards.orderCombinationsByScoreAndNumberOfCards(listOfStacks)
  
  ==Observations==
  If you dont have choice to get a card from deck or discarded cards, this strategy will get
  using the valid way.
  '''
  
  def play(self, commandsManager):
    command = None
    if self.context.discardedCards.isEmpty(): command = GetOneCardOfTheDeckCommand(self.player)
    if self.context.deckHeight == 0: command = GetDiscardedCardsCommand(self.player)
    if command != None: commandsManager.addCommand(command)
    else:
      self.getCardFromDeckOrCardsFromDiscardedCards(commandsManager.addCommand, self.context)
    self.createCombinations(commandsManager.addCommand, self.context)
    self.discard(commandsManager.addCommand, self.context)
  
  def getCardFromDeckOrCardsFromDiscardedCards(self, addCommand, context): pass
  
  def createCombinations(self, addCommand, context): pass
  
  def discard(self, addCommand, context): pass
  

  '''
  player: who is playing
  context: class with all informations a player can know
  addCommand: addCommand to CommandsManager
  
  Accessible Classes:
  - StackOfCards
  - StackOfCards
  - CombinationGenerator
  
  ==Implement this methods==
  def getCardFromDeckOrCardsFromDiscardedCards(self, commandsManager): pass
  def createCombinations(self, commandsManager): pass
  def discard(self, commandsManager): pass
  
  ==Accessible informations in context==
  context.property:
  
  teamsScores = {} # map team name -> score
  deckHeight = 0 # int
  numberOfCardsOfAnothersPlayers = {} # map player name -> number of cards
  numberOfCardsOfAnothersTeams = {} # map team name -> number of cards
  discardedCards = None # cards.StackOfCards
  teamsCombinations = {} # map team name -> list of StackOfCards
  numberOfDeads = 0 # int
  teamsHaveAlreadyHit = [] # list of team names
  playersHaveAlreadyHit = [] # list of player names
  currentPlayerHasAlreadyGetCards = False
  currentPlayerHasAlreadyDiscarded = False
  teamHasCanastra(team)
  teamCanHit(team)
  
  # game
  player = None
  currentGamePlayers = None
  configurations = None
  # cardgame
  playercards = None
  currentRoundPlayers = None
  
  ==Commands==
  GetDiscardedCardsCommand(player, None)
  GetOneCardOfTheDeckCommand(player, None)
  PutCardsInCombinationCommand(player, [combination-index, [cards]])
  MakeNewCombinationCommand(player, stack)
  DiscardCommand(player, card)
  
  ==Useful methods==
  StackOfCards().isSequenceWithSameSuit()
  StackOfCards().isSequenceWithSameSuitWithOneJoker()
  StackOfCards().isCombinationOfJokers()
  StackOfCards().isCombinationWithSameValue()
  StackOfCards().isCombinationWithSameValueWithOneJoker()
  StackOfCards().isValidCombination()
  
  StackOfCards().isCanastra()
  StackOfCards().isCleanCanastra()
  StackOfCards().isCanastraWithJoker()
  StackOfCards().isRealCanastra()
  StackOfCards().isCanastraOfJokers()
  StackOfCards().scoreOfCanastra()
  
  StackOfCards().allValidCombinationOfCards() => [s]
  StackOfCards.orderCombinationsByScore(listOfStacks)
  StackOfCards.orderCombinationsByNumberOfCards(listOfStacks)
  StackOfCards.orderCombinationsByNumberOfCardsAndScore(listOfStacks)
  StackOfCards.orderCombinationsByScoreAndNumberOfCards(listOfStacks)
  '''
  
###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

class StackOfCards(cards.StackOfCards):

  def __init__(self, stack=None):
    if stack != None:
      self.cards = stack.cards
    else:
      self.cards = []

  def isSequenceWithSameSuit(self):
    if self.allCardsInSequenceWithSameSuit(): return True
    c = cards.StackOfCards()
    c.pushAll(self.cards)
  #  c = stack.clone()
    c.sortByValue()
    # Q K AS
    if c.containsCardWithValue(1): # AS
      cardAS = c.popIndex(0)
      c.push(cards.Card(14, cardAS.suit))
      if c.allCardsInSequenceWithSameSuit(): return True
    return False
  
  def isSequenceWithSameSuitWithOneJoker(self):
    if self.isSequenceWithSameSuit(): return False
    c = cards.StackOfCards()
    c.pushAll(self.cards)
  #  c = self.clone()
    c.sortByValue()
    numberOfJokers = c.numberOfCardsWithValue(0) + c.numberOfCardsWithValue(2)
    if numberOfJokers == 1:
      c.popCardsWithValue(2)
      c.popCardsWithValue(0)
      if c.allCardsInSequenceWithSameSuitWithJokers(1): return True
      # Q K AS
      if c.containsCardWithValue(1): # AS
        cardAS = c.popIndex(0)
        c.push(cards.Card(14, cardAS.suit))
        if c.allCardsInSequenceWithSameSuitWithJokers(1): return True
    if numberOfJokers == 2: # AS 2 2 4, AS 2 0 4, AS 2 3 2, AS 2 3 0 ...
      twos = c.popCardsWithValue(2)
      c.popCardsWithValue(0)
      referenceOfSuit = c.seeFirstCard().suit
      if twos.containsCardWithSuit(referenceOfSuit):
        c.push(cards.Card(2, referenceOfSuit))
        if c.allCardsInSequenceWithSameSuitWithJokers(1): 
          return True
        if c.containsCardWithValue(1): # AS ... AS
          cardAS = c.popIndex(0)
          c.push(cards.Card(14, cardAS.suit))
          return c.allCardsInSequenceWithSameSuitWithJokers(1)
    return False
  
  def isCombinationOfJokers(self):
    numberOfJokers = self.numberOfCardsWithValue(0) + self.numberOfCardsWithValue(2)
    return numberOfJokers == self.height()
  
  def isCombinationWithSameValue(self):
    return self.allCardsWithSameValue()
  
  def isCombinationWithSameValueWithOneJoker(self):
    c = cards.StackOfCards()
    c.pushAll(self.cards)
  #  c = self.clone()
    numberOfJokers = c.numberOfCardsWithValue(0) + c.numberOfCardsWithValue(2)
    c.popCardsWithValue(2)
    c.popCardsWithValue(0)
    return c.allCardsWithSameValue() and numberOfJokers == 1
  
  def isValidCombination(self):
    if self.height() < 3 or self.height() > 14: return False
    # FIXME
    #super lento: isSequenceWithSameSuit(stack) isSequenceWithSameSuitWithOneJoker()
    #lento: isCombinationWithSameValueWithOneJoker()
    #rapido: isCombinationOfJokers(stack) isCombinationWithSameValue()
    
    return self.isSequenceWithSameSuit() or \
            self.isSequenceWithSameSuitWithOneJoker() or \
            self.isCombinationOfJokers() or \
            self.isCombinationWithSameValue() or \
            self.isCombinationWithSameValueWithOneJoker()
  
  # Canastras
  
  def isCanastra(self):
    return self.height() >= 7
  
  def isCleanCanastra(self):
    return self.isCanastra() and \
    (self.isSequenceWithSameSuit() or self.isCombinationWithSameValue())
  
  def isCanastraWithJoker(self):
    return self.isCanastra() and \
    (self.isSequenceWithSameSuitWithOneJoker() or self.isCombinationWithSameValueWithOneJoker())
  
  def isRealCanastra(self):
    return self.isCanastra() and self.height() == 14 and self.isSequenceWithSameSuit()
  
  def isCanastraOfJokers(self):
    return self.isCanastra() and self.isCombinationOfJokers()
    
  def scoreOfCanastra(self):
    if self.isCanastra():
      if self.isRealCanastra(): return 1000
      if self.isCanastraOfJokers(): return 500
      if self.isCleanCanastra(): return 200
      if self.isCanastraWithJoker(): return 100
    return 0
  
  # Utils
  
  def allValidCombinationOfCards(self):
    combinations = self.allCombinationsOfCards(3, 7)
    validCombinations = []
    for combination in combinations:
      combination = StackOfCards(combination)
      if combination.isValidCombination():
        validCombinations.append(combination)
    self.orderCombinationsByNumberOfCardsAndScore(validCombinations)
    return validCombinations
  
  @staticmethod
  def orderCombinationsByScore(listOfStacks):
    def keyfunction(stack): return stack.score()
    listOfStacks.sort(key=keyfunction)
    
  @staticmethod
  def orderCombinationsByNumberOfCards(listOfStacks):
    def keyfunction(stack): return stack.height()
    listOfStacks.sort(key=keyfunction)
  
  @staticmethod
  def orderCombinationsByNumberOfCardsAndScore(listOfStacks):
    def keyfunction(stack): return stack.height(), stack.score()
    listOfStacks.sort(key=keyfunction)
    
  @staticmethod
  def orderCombinationsByScoreAndNumberOfCards(listOfStacks):
    def keyfunction(stack): return stack.score(), stack.height()
    listOfStacks.sort(key=keyfunction)


###############################################################################
# [required] 10) Define a factory

accessibleClasses = [utils.CombinationGenerator, StackOfCards]

class GameFactory(cardgame.GameFactory):
  
  def __init__(self):
    super(GameFactory, self).__init__(Game, Context, Configurations, accessibleClasses)

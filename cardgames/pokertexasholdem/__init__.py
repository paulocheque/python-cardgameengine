'''

@author: Ricardo Yamamoto (ricardoy@gmail.com)
@author: Paulo Cheque (paulocheque@gmail.com)

http://en.wikipedia.org/wiki/Texas_hold_%27em
http://pt.wikipedia.org/wiki/Texas_hold_%27em
http://en.wikipedia.org/wiki/Poker_probability_(Texas_hold_%27em)
'''

from cardgameengine import cardgame
from cardgameengine import commands
from cardgameengine import players
from cardgameengine import cards
from cardgameengine import utils

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class PokerTexasHoldEmCard(cards.ValueCard):
  values = cards.VALUES_ANGLO_AMERICAN
  suits = cards.SUITS_ANGLO_AMERICAN

###############################################################################
# [required] 2) Create the logic of the game: Probably this is easy to create than MyRound class.

class PokerTexasHoldEmCardGame(cardgame.CardGame):

  def __init__(self, players, configurations):
    super(PokerTexasHoldEmCardGame, self).__init__(PokerTexasHoldEmRound, players, configurations, PokerTexasHoldEmCardGameReport)
    self.playersChips = {}
    for player in players:
      if not player.name in self.playersChips:
        self.playersChips[player.name] = self.configurations.amountOfChipsPerPlayer
    # FIXME definir valor da rodada, blind, etc...
    
  def organize(self):
    # FIXME
    #    distribuir fichas
    # definir valor da rodada, blind, etc...
    pass
  
  def end(self): pass

  def conditionToWin(self, player):
    return len(self.players) == 1 # last player wins

###############################################################################
# [required] 2): Define the context where the commands will be executed:

#  informacao dos jogadores: 
#  level
#  nome
#  historico de blefes?
#  community cards
#  suas cartas
#  informacoes da aposta, quanto tem que cobrir
  
class PokerTexasHoldEmRoundContext(cardgame.RoundContext):
  def __init__(self):
    super(PokerTexasHoldEmRoundContext, self).__init__()
    # some variables
    # see method context on the round class (step to create the Round)
    # FIXME

  def summary(self):
    return super(PokerTexasHoldEmRoundContext, self).summary()

###############################################################################
# [required] 3): Define player's commands

class GiveUpCommand(commands.CardGameCommand):
  
  def validate(self, context):
    if self.flag: raise commands.InvalidCommandError('Player have already gived up')
  
  def execute(self, game, round):
    self.round.players.remove(self.player)
    
MyCardGame.registerCommand(GiveUpCommand)
    
class GiveUpShowingTheCardsCommand(commands.CardGameCommand):
  
  def validate(self, context):
    pass
  
  def execute(self, game, round):
    self.round.players.remove(self.player)
    self.round.loserCards.pushAll(self.mycards)
    
MyCardGame.registerCommand(GiveUpShowingTheCardsCommand)
    
class BetCommand(commands.CardGameCommand):
  
  def validate(self, context):
    pass
  
  def execute(self, game, round):
    # FIXME
    pass
  
MyCardGame.registerCommand(BetCommand)
  
class PayCommand(commands.CardGameCommand):
  
  def validate(self, context):
    pass
  
  def execute(self, game, round):
    # FIXME
    pass
  
MyCardGame.registerCommand(PayCommand)

###############################################################################
# [required] 4): Define strategies to a player

class PokerTexasHoldEmStrategy(cardgame.Strategy):
  def play(self, commandsManager, context):
    # implementation here
    self.smallBlindStrategy(commandsManager, context)
    self.bigBlindStrategy(commandsManager, context)
    self.firstRound(commandsManager, context)
    self.secondRound(commandsManager, context)
    self.thirdRound(commandsManager, context)

  # Let the developer implement this methods with his stratagies
  def smallBlindStrategy(self, commandsManager, context): pass
  def bigBlindStrategy(self, commandsManager, context): pass
  def firstRound(self, commandsManager, context): pass
  def secondRound(self, commandsManager, context): pass
  def thirdRound(self, commandsManager, context): pass
  
###############################################################################
# [optional] 5): Define a model of reports to store informations.
 
# All reports already have: players, initialNumberOfPlayers, durationTime, winners
# RoundReport has report of all commands (good to debug and undertandings algorithms)
# CardGameReport has report of all rounds (good to debug and undertandings algorithms)
# FIXME

class PokerTexasHoldEmRoundReport(cardgame.RoundReport):
  # need implementation
  pass
  
class PokerTexasHoldEmCardGameReport(cardgame.CardGameReport):
  # need implementation
  pass
  
###############################################################################
# [required] 6) Create the logic of a round of the game:
 
# Probably the hardest thing to create a game, ignoring other aspects besides the engine.

class PokerTexasHoldEmRound(cardgame.Round):

  # timeout: -1 = infinite  [, timeForPlay=-1]
  def __init__(self, game, players, commandsManager):
    super(PokerTexasHoldEmRound, self).__init__(game, players, commandsManager, 
                                                PokerTexasHoldEmRoundContext, 
                                                PokerTexasHoldEmRoundReport)

  def populateContext(self, context):
    # need implementation:
    # Set attributes to the context that a user need to know to play, like community cards, etc
    # Example: context.communitycards = self.communitycards
    # Dont do this: context.round = self or context.game = self.game. This variables are used to control cheat.
    # FIXME
    pass

  def organize(self):
    self.deck.shuffle()
    self.distributeCardsToAllPlayers(2)
    self.distributeCardsTo(self.communityCards, 3)
    #blind, small blind, etc
    # ve quem nao tem chips suficiente, sai do jogo
    # FIXME
  
  def end(self): pass
  #    vencedor ganha dinheiro da mesa ou divide entre quem ganhou
  # atualiza estatisticas?
  # FIXME
  
  def conditionToWin(self, player):
    pass
  # FIXME
  #    pode ser mais de um
# ordena combinacoes dos jogadores restantes
# pega todas que é igual a maior
    
###############################################################################
# [optional] 7) Define configurations of the game

class PokerTexasHoldEmConfigurations(cardgame.Configurations):
  
  def __init__(self, amountOfChipsPerPlayer=1000, timeForPlay=-1):
    deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(PokerTexasHoldEmCard, 4, 13, 1, 0)
    super(PokerTexasHoldEmConfigurations, self).__init__(deckPrototype, timeForPlay)
    
    self.amountOfChipsPerPlayer = amountOfChipsPerPlayer
    
###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

def isRoyalStraigthFlush(stack):
  return stack.allCardsInSequenceWithSameSuit() and stack.containsCardWithValue(13) and containsCardWithValue(1)

def isStraigthFlush(stack):
  return stack.allCardsInSequenceWithSameSuit()

def isFourOfAKind(stack):
  stack.sortByValue()
  return stack.numberOfCards(stack.seeFirstCard()) == 4 or stack.numberOfCards(stack.seeLastCard()) == 4
  
def isFullHouse(stack):
  stack.sortByValue()
  return \
    (stack.numberOfCards(stack.seeFirstCard()) == 2 and stack.numberOfCards(stack.seeLastCard()) == 3) or \
    (stack.numberOfCards(stack.seeFirstCard()) == 3 and stack.numberOfCards(stack.seeLastCard()) == 2)
  
def isFlush(stack):
  return stack.allCardsWithSameSuit()

def isStraigth(stack):
  return stack.allCardsInSequence()

def isThreeOfAKind(stack):
  stack.sortByValue()
  return \
    not isFullHouse(stack) and \
    (stack.numberOfCardsWithValue(stack.see(0).value) == 3 or \
     stack.numberOfCardsWithValue(stack.see(1).value) == 3 or \
     stack.numberOfCardsWithValue(stack.see(2).value) == 3)

def isTwoPair(stack):
  stack.sortByValue()
  return \
    not isFourOfAKind(stack) and \
    ((stack.numberOfCardsWithValue(stack.see(0).value) == 2 and stack.numberOfCardsWithValue(stack.see(2).value) == 2) or \
     (stack.numberOfCardsWithValue(stack.see(1).value) == 2 and stack.numberOfCardsWithValue(stack.see(3).value) == 2))

def isPair(stack):
  stack.sortByValue()
  return \
    not isFourOfAKind(stack) and not isTwoPair(stack) and \
    (stack.numberOfCardsWithValue(stack.see(0).value) == 2 or \
     stack.numberOfCardsWithValue(stack.see(1).value) == 2 or \
     stack.numberOfCardsWithValue(stack.see(2).value) == 2 or \
     stack.numberOfCardsWithValue(stack.see(3).value) == 2)

def isHighCard(stack):
  return not isRoyalStraigthFlush(stack) and not isStraigthFlush(stack) and \
          not isFourOfAKind(stack) and not isFullHouse(stack) and \
          not isFlush(stack) and not isStraigth(stack) and \
          not isThreeOfAKind(stack) and not isTwoPair(stack) and not isPair(stack)


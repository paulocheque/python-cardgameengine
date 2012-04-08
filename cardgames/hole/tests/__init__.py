'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest

from gameengine import commands, players, errors
from cardgameengine.constants import *
from cardgameengine import cardgame, cards

from cardgames import hole

###############################################################################
# [optional] 0): Define base class with common data to clear testcases

class GameTestsHelper(unittest.TestCase):

  def setUp(self):
    self.strategy = hole.Strategy()

    self.players = [players.Player('Player1', hole.Strategy, contextClass=hole.Context), 
                    players.Player('Player2', hole.Strategy, contextClass=hole.Context)]
    self.player = self.players[0]
    self.context = self.player.context
    
    self.params = None
    self.getCardCommand = hole.GetOneCardOfTheDeckCommand(self.player, self.params)
    self.getDiscardedCommand = hole.GetDiscardedCardsCommand(self.player, self.params)
    self.discardCommand = hole.DiscardCommand(self.player, self.params)
    self.newCombinationCommand = hole.MakeNewCombinationCommand(self.player, self.params)
    self.putCardCommand = hole.PutCardsInCombinationCommand(self.player, self.params)
    
    self.roundreport = hole.RoundReport()
    self.cardgamereport = hole.GameReport()
    self.configurations = hole.Configurations()
    self.deckPrototype = self.configurations.deckPrototype.clone()
    
    self.game = hole.Game(self.players, self.configurations)
    self.round = hole.Round(self.game, self.players[:], self.configurations, self.game.commandsManager)
    self.game.currentRound = self.round
    self.round.currentPlayer = self.player


###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class CardTests(GameTestsHelper):
  
  def testValues(self):
    self.assertEquals(cards.VALUES_ANGLO_AMERICAN, hole.Card.values)
    
  def testSuits(self):
    self.assertEquals(cards.SUITS_ANGLO_AMERICAN, hole.Card.suits)
    
################################################################################
## [optional] 2) Define configurations of the game

class ConfigurationsTests(GameTestsHelper):

  def testHeight(self):
    self.assertEquals(108, len(self.deckPrototype.cards))
    
  def testContainCards(self):
    self.assertTrue(self.deckPrototype.containsCard(hole.Card(0, 0)))
    self.assertFalse(self.deckPrototype.containsCard(hole.Card(15, 4)))
    
  def testScore(self):
    self.assertEquals(20, self.deckPrototype.popCard(hole.Card(0, 0)).score)
    self.assertEquals(15, self.deckPrototype.popCard(hole.Card(1, 1)).score)
    self.assertEquals(10, self.deckPrototype.popCard(hole.Card(2, 1)).score)
    self.assertEquals(5, self.deckPrototype.popCard(hole.Card(3, 1)).score)
    self.assertEquals(5, self.deckPrototype.popCard(hole.Card(7, 1)).score)
    self.assertEquals(10, self.deckPrototype.popCard(hole.Card(8, 1)).score)
    self.assertEquals(10, self.deckPrototype.popCard(hole.Card(13, 1)).score)

  def testAttributes(self):
    self.assertEquals(1000, self.configurations.maximumScore)
    self.assertEquals(2, self.configurations.numberOfDeads)
    self.assertEquals(-1, self.configurations.timeForPlay)
    
################################################################################
## [required] 3): Define the rules of command's execution

class HolePlayerContextTests(GameTestsHelper):
  
  def testAttributes(self):
    self.assertEquals(self.player, self.context.player)
    self.assertEquals(None, self.context.currentGamePlayers)
    self.assertEquals(None, self.context.configurations)
    
    self.assertEquals(None, self.context.playercards)
    
    self.assertEquals({}, self.context.teamsScores)
    self.assertEquals(0, self.context.deckHeight)
    self.assertEquals({}, self.context.numberOfCardsOfAnothersPlayers)
    self.assertEquals({}, self.context.numberOfCardsOfAnothersTeams)
    self.assertEquals(None, self.context.discardedCards)
    self.assertEquals({}, self.context.teamsCombinations)
    self.assertEquals(0, self.context.numberOfDeads)
    self.assertEquals([], self.context.teamsHaveAlreadyHit)
    self.assertEquals([], self.context.playersHaveAlreadyHit)
    self.assertEquals(False, self.context.currentPlayerHasAlreadyGetCards)
    self.assertEquals(False, self.context.currentPlayerHasAlreadyDiscarded)
    
  def testSummary(self):
    self.context.summary()
    
    
###############################################################################
# [required] 4) Card game logic

#################################
# [optional] 4.1): Define a model of reports to store informations.

class GameReportTests(GameTestsHelper):
  
  def testBasicAttributes(self):
    self.assertEquals([], self.cardgamereport.players)
    self.assertEquals(0, self.cardgamereport.initialNumberOfPlayers)
    self.assertEquals(None, self.cardgamereport.configurations)
    self.assertEquals([], self.cardgamereport.winners)
    self.assertEquals([], self.cardgamereport.losers)
    self.assertEquals([], self.cardgamereport.commands)
    self.assertEquals(0, self.cardgamereport.durationTime)
    
    self.assertEquals([], self.cardgamereport.roundsReports)
    
    self.assertEquals(0, self.cardgamereport.numberOfCanastras)
    
    
#################################s
# [required] 4.2) Create the logic of the game
    
class GameTests(GameTestsHelper):
  
  def setUp(self):
    super(GameTests, self).setUp()
    self.configurations.maximumScore = 100
  
  def testValidCommands(self):
    self.assertEquals(
          [hole.GetOneCardOfTheDeckCommand,
           hole.GetDiscardedCardsCommand,
           hole.DiscardCommand,
           hole.MakeNewCombinationCommand,
           hole.PutCardsInCombinationCommand], 
          self.game.commandsManager.validCommands)
    
  def testSeeScoreSumScore(self):
    self.assertEquals(0, self.game.seeScore(self.players[0].team))
    self.game.sumScore(self.players[0].team, 100)
    self.assertEquals(100, self.game.seeScore(self.players[0].team))
    
  def abstractTestOrganize(self):
    pass
  
  def abstractTestEnd(self):
    pass
  
  def testConditionToWin(self):
    self.assertFalse(self.game.conditionToWin(self.players[0]))
    self.game.sumScore(self.players[0].team, 101)
    self.assertTrue(self.game.conditionToWin(self.players[0]))
    self.game.sumScore(self.players[1].team, 110)
    self.assertFalse(self.game.conditionToWin(self.players[0]))
    self.assertTrue(self.game.conditionToWin(self.players[1]))
    
    
###############################################################################
# [required] 5) Round logic

#################################
# [optional] 5.1): Define a model of reports to store informations
    
class RoundReportTests(GameTestsHelper):
  
  def testBasicAttributes(self):
    self.assertEquals([], self.roundreport.players)
    self.assertEquals(0, self.roundreport.initialNumberOfPlayers)
    self.assertEquals(None, self.roundreport.configurations)
    self.assertEquals([], self.roundreport.winners)
    self.assertEquals([], self.roundreport.losers)
    self.assertEquals([], self.roundreport.commands)
    self.assertEquals(0, self.roundreport.durationTime)
    
#################################
# [required] 5.2) Create the logic of a round of the game:
    
class RoundTests(GameTestsHelper):
  
#  def testOrganize(self):
#    for playerCards in self.round.playersCards.values():
#      self.assertEquals(0, playerCards.height())
#    for dead in self.round.deads:
#      self.assertEquals(0, dead.height())
#    self.round.organize()
#    for dead in self.round.deads:
#      self.assertEquals(11, dead.height())
  
  def abstractTestEnd(self):
    pass
  
  def testConditionToWin(self):
    self.assertTrue(self.round.conditionToWin(self.players[0]))
    self.round.seeCards(self.players[0]).push(hole.Card(0,0))
    self.assertFalse(self.round.conditionToWin(self.players[0]))
  
  def testAddNewCombination(self):
    combination = cards.StackOfCards()
    combination.pushAll([hole.Card(0, 0), hole.Card(0, 0), hole.Card(0, 0)])
    self.round.addNewCombination(self.players[0], combination)
    self.round.addNewCombination(self.players[0], combination)
    self.assertEquals(2, len(self.round.teamsCombinations[self.players[0].team.name]))

  def testSeeCombination(self):
    combination = cards.StackOfCards()
    combination.pushAll([hole.Card(0, 0), hole.Card(0, 0), hole.Card(0, 0)])
    self.round.addNewCombination(self.players[0], combination)
    self.assertEquals(combination, self.round.seeCombination(self.players[0], 0))
  
###############################################################################
# [required] 6): Define player's commands

class GetOneCardOfTheDeckCommandTests(GameTestsHelper):

  def testValidate(self):
    self.context.currentPlayerHasAlreadyGetCards = False
    self.context.deckHeight = 1
    self.getCardCommand.validate(self.context)
    
  def testValidateRaiseAnInvalidCommandErrorAlreadyHaveBeenGottenCards(self):
    self.context.currentPlayerHasAlreadyGetCards = True
    try:
      self.getCardCommand.validate(self.context)
    except errors.InvalidCommandError: pass
    else: self.fail()
    
  def testValidateRaiseAnInvalidCommandErrorEmptyDeck(self):
    self.context.deckHeight = 0
    try:
      self.getCardCommand.validate(self.context)
    except errors.InvalidCommandError: pass
    else: self.fail()
    
  def testExecuteMustMoveACardOfDeckToPlayer(self):
    self.assertEquals(108, self.game.currentRound.deck.height())
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())
    
    self.getCardCommand.execute(self.game)
    self.assertEquals(107, self.game.currentRound.deck.height())
    self.assertEquals(1, self.game.currentRound.seeCards(self.player).height())
    
class GetDiscardedCardsCommandTests(GameTestsHelper):

  def testValidate(self):
    self.context.currentPlayerHasAlreadyGetCards = False
    self.context.discardedCards = cards.StackOfCards()
    self.context.discardedCards.push(cards.Card(0, 0))
    self.getDiscardedCommand.validate(self.context)
    
  def testValidateRaiseAnInvalidCommandErrorHasAlreadyBeenGottenCards(self):
    self.context.currentPlayerHasAlreadyGetCards = True
    try:
      self.getDiscardedCommand.validate(self.context)
    except errors.InvalidCommandError: pass
    else: self.fail()

  def testValidateRaiseAnInvalidCommandErrorEmptyDiscardedCards(self):
    self.context.currentPlayerHasAlreadyGetCards = False
    self.context.discardedCards = cards.StackOfCards()
    try:
      self.getDiscardedCommand.validate(self.context)
    except errors.InvalidCommandError: pass
    else: self.fail()
    
  def testExecuteMustMoveAllDiscardedCardsToPlayerDeck(self):
    self.game.currentRound.discardedCards.push(self.game.currentRound.deck.pop())
    self.game.currentRound.discardedCards.push(self.game.currentRound.deck.pop())
    
    self.getDiscardedCommand.execute(self.game)
    self.assertEquals(0, self.game.currentRound.discardedCards.height())
    self.assertEquals(2, self.game.currentRound.seeCards(self.player).height())
    
class DiscardCommandTests(GameTestsHelper):
#  
#    if not context.currentPlayerHasAlreadyGetCards:
#      raise commands.InvalidCommandError('Player must get card before discard')
#    goingToHit = context.playercards.height() == 1
#    if not context.teamCanHit(self.player.team) and goingToHit:
#      raise commands.InvalidCommandError('Player cant hit')
#    if not context.playercards.containsCard(self.params):
#      raise commands.CheatCommandError('Cheat? Bug?')

  def atestValidate(self):
    pass
#    self.game.currentRound.seeCards(self.player).push(cards.Card(0, 0))
#    self.context.currentPlayerHasAlreadyGetCards = True
#    self.discardCommand.params = cards.Card(0, 0)
#    self.discardCommand.validate(self.context)
    
#  def testValidateRaiseAnInvalidCommandErrorHaventGetCards(self):
#    self.context.currentPlayerHasAlreadyGetCards = False
#    try:
#      self.discardCommand.validate(self.context)
#    except commands.InvalidCommandError: pass
#    else: self.fail()

#  def testValidateRaiseAnInvalidCommandErrorHaveAlreadyBeenDiscarded(self):
#    self.context.currentPlayerHasAlreadyDiscarded = True
#    try:
#      self.discardCommand.validate(self.context)
#    except commands.InvalidCommandError: pass
#    else: self.fail()
#
#  def testValidateRaiseAnInvalidCommandErrorCantHit(self):
#    try:
#      self.discardCommand.validate(self.context)
#    except commands.InvalidCommandError: pass
#    else: self.fail()
#    
#  def testValidateRaiseACheatCommandErrorUnknownCards(self):
#    self.discardCommand.params = cards.Card(1, 1)
#    try:
#      self.discardCommand.validate(self.context)
#    except commands.CheatCommandError: pass
#    else: self.fail()
      
#  def testIsValidAcceptOnlyOnceByContext(self):
#    card = self.game.currentRound.deck.pop()
#    self.command.playercards.push(card)
#    self.command.params = card
#    self.assertTrue(self.command.isValid())
#    self.command.execute(self.game, self.game.currentRound)
#    self.assertFalse(self.command.isValid())
#    
#    self.command.context = hole.RoundContext()
#    self.command.playercards.push(card)
#    self.assertTrue(self.command.isValid())
#  
#  def testIsInvalidIfThePlayerDontHaveTheCard(self):
#    self.command.params = cards.Card(1, 1)
#    self.assertFalse(self.command.isValid())
#  
#  def testExecuteMustMovePlayerCardToDiscardedCards(self):
#    card = self.game.currentRound.deck.pop()
#    self.round.seeCardsOfCurrentPlayer().push(card)
#    self.command.params = card
#    self.assertEquals(0, self.game.currentRound.discardedCards.height())
#    self.assertEquals(1, self.round.seeCardsOfCurrentPlayer().height())
#    
#    self.command.execute(self.game)
#    self.assertEquals(1, self.game.currentRound.discardedCards.height())
#    self.assertEquals(0, self.round.seeCardsOfCurrentPlayer().height())
#    
##    self.newCombinationCommand = hole.MakeNewCombinationCommand(self.player, self.params, self.context)
#class MakeNewCombinationCommandTests(GameTestsHelper):
#  
#  def testIsInvalidDependsIfTheCombinationsIsValid(self):
#    pass # FIXME pending
#  
#  def createValidState(self):
#    combination = cards.StackOfCards()
#    self.command.playercards.pushAll([cards.Card(3, 1), cards.Card(4, 1), cards.Card(5, 1)])
#    self.command.params = self.command.playercards.cards
#    self.assertEquals(3, self.command.playercards.height())
#    self.assertEquals(0, len(self.game.currentRound.teamsCombinations[self.player.team.name]))
#    
#  def testIsInvalidIfTryToHitWithoutCanastra(self):
#    pass
#    
#  def testIsInvalidIfMyTeamCantHitAndIAmGoingToHit(self):
#    self.createValidState()
#    self.command.context.myTeamCanHit = False
#    self.assertFalse(self.command.isValid())
#    
#    self.command.context.myTeamCanHit = True
#    self.assertTrue(self.command.isValid())
#    
#  def testExecuteMustMovePlayerCardsToNewTeamCombination(self):
#    self.createValidState()
#    self.command.context.myTeamCanHit = True
#    
#    self.command.execute(self.game)
#    combinations = self.game.currentRound.teamsCombinations[self.player.team.name]
#    self.assertEquals(1, len(combinations))
#    self.assertEquals(3, combinations[0].height())
#    self.assertEquals(0, self.command.playercards.height())
#    
##    self.putCardCommand = hole.PutCardsInCombinationCommand(self.player, self.params, self.context)
#class PutCardsInCombinationCommandTests(GameTestsHelper):
#  
#  def testIsInvalidDependsIfTheCombinationsIsValid(self):
#    pass # FIXME pending
#    
#  def testIsInvalidIfTryToHitWithoutCanastra(self):
#    pass
#
#  def createValidState(self):
#    combination = cards.StackOfCards()
#    combination.pushAll([cards.Card(3, 1), cards.Card(4, 1), cards.Card(5, 1)])
#    self.game.currentRound.addNewCombination(self.player, combination)
#    self.command.playercards.push(cards.Card(6, 1))
#    self.command.params = [0, self.command.playercards.cards]
#    self.assertEquals(3, self.game.currentRound.seeCombination(self.player, 0).height())
#    self.assertEquals(1, self.command.playercards.height())
#    
#  def testIsInvalidIfMyTeamCantHitAndIAmGoingToHit(self):
#    self.createValidState()
#    self.command.context.myTeamCanHit = False
#    self.assertFalse(self.command.isValid())
#
#  def testExecuteMovePlayerCardsToTeamCombination(self):
#    self.createValidState()
#    self.command.context.myTeamCanHit = True
#    
#    self.command.execute(self.game)
#    self.assertEquals(4, self.game.currentRound.seeCombination(self.player, 0).height())
#    self.assertEquals(0, self.command.playercards.height())
    

###############################################################################
# [required] 7): Define strategies to a player

class StrategyTests(GameTestsHelper):

  def testPlay(self):
    self.strategy.getCardFromDeckOrCardsFromDiscardedCards(self.game.commandsManager, self.context)
    self.strategy.createCombinations(self.game.commandsManager, self.context)
    self.strategy.discard(self.game.commandsManager, self.context)

################################################################################
## [optional] 8) Another classes (custom) to encapsulate things and algorithms. 

class HoleUtilsTest(GameTestsHelper):
  
  def setUp(self):
    self.sequence_combination = hole.StackOfCards(cards.strToStackOfCards('3-1 4-1 5-1'))
    self.sequence_withjoker_combination = hole.StackOfCards(cards.strToStackOfCards('3-1 0-0 5-1'))
    self.sequenceas22_combination = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 2-2'))
    self.sequenceas20_combination = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 0-0'))
    self.sequenceas22_invalid_combination = hole.StackOfCards(cards.strToStackOfCards('1-1 2-2 2-2'))
    self.sequenceas22_invalid_combination = hole.StackOfCards(cards.strToStackOfCards('1-3 2-1 2-2'))
    self.sequenceas20_invalid_combination = hole.StackOfCards(cards.strToStackOfCards('1-1 2-2 0-0'))
    self.sequenceQKAS_combination = hole.StackOfCards(cards.strToStackOfCards('12-1 13-1 1-1'))
    self.sequenceQKASwithjoker_combination = hole.StackOfCards(cards.strToStackOfCards('0-0 13-1 1-1'))
    self.samevalue_combination = hole.StackOfCards(cards.strToStackOfCards('3-1 3-1 3-2'))
    self.samevaluewithjoker_combination = hole.StackOfCards(cards.strToStackOfCards('3-1 3-2 0-0'))
    self.jokers_combination = hole.StackOfCards(cards.strToStackOfCards('2-1 0-0 2-2'))
    
    self.sequence_canastra = hole.StackOfCards(cards.strToStackOfCards('3-1 4-1 5-1 6-1 7-1 8-1 9-1'))
    self.sequence_withjoker_canastra = hole.StackOfCards(cards.strToStackOfCards('3-1 0-0 5-1 6-1 7-1 8-1 9-1'))
    self.real_canastra = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.realwithjoker_canastra = hole.StackOfCards(cards.strToStackOfCards('1-1 2-2 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.samevalue_canastra = hole.StackOfCards(cards.strToStackOfCards('3-1 3-1 3-2 3-3 3-4 3-4 3-3'))
    self.samevaluewithjoker_canastra = hole.StackOfCards(cards.strToStackOfCards('3-1 3-2 3-3 3-4 3-1 3-2 0-0'))
    self.jokers_canastra = hole.StackOfCards(cards.strToStackOfCards('2-1 0-0 2-2 0-0 0-0 0-0 2-3'))
    
  def testIsSequenceWithSameSuit(self):
    self.assertTrue(self.sequence_combination.isSequenceWithSameSuit())
    self.assertTrue(self.sequenceQKAS_combination.isSequenceWithSameSuit())
    self.assertFalse(self.sequenceQKASwithjoker_combination.isSequenceWithSameSuit())
    self.assertFalse(self.sequence_withjoker_combination.isSequenceWithSameSuit())
    self.assertFalse(self.sequenceas22_combination.isSequenceWithSameSuit())
    self.assertFalse(self.sequenceas20_combination.isSequenceWithSameSuit())
    self.assertFalse(self.samevalue_combination.isSequenceWithSameSuit())
    self.assertFalse(self.samevaluewithjoker_combination.isSequenceWithSameSuit())
    self.assertFalse(self.jokers_combination.isSequenceWithSameSuit())
  
  def testIsSequenceWithSameSuitWithOneJoker(self):
    self.assertTrue(self.sequence_withjoker_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertTrue(self.sequenceas22_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertTrue(self.sequenceas20_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertTrue(self.sequenceQKASwithjoker_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertFalse(self.sequenceQKAS_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertFalse(self.sequence_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertFalse(self.samevalue_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertFalse(self.samevaluewithjoker_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertFalse(self.jokers_combination.isSequenceWithSameSuitWithOneJoker())
    self.assertFalse(self.real_canastra.isSequenceWithSameSuitWithOneJoker())
    
  def testIsCombinationWithSameValue(self):
    self.assertTrue(self.samevalue_combination.isCombinationWithSameValue())
    self.assertFalse(self.samevaluewithjoker_combination.isCombinationWithSameValue())
    self.assertFalse(self.sequence_combination.isCombinationWithSameValue())
    self.assertFalse(self.sequence_withjoker_combination.isCombinationWithSameValue())
    self.assertFalse(self.sequenceas22_combination.isCombinationWithSameValue())
    self.assertFalse(self.sequenceas20_combination.isCombinationWithSameValue())
    self.assertFalse(self.jokers_combination.isCombinationWithSameValue())
  
  def testIsCombinationWithSameValueWithOneJoker(self):
    self.assertTrue(self.samevaluewithjoker_combination.isCombinationWithSameValueWithOneJoker())
    self.assertFalse(self.samevalue_combination.isCombinationWithSameValueWithOneJoker())
    self.assertFalse(self.sequence_combination.isCombinationWithSameValueWithOneJoker())
    self.assertFalse(self.sequence_withjoker_combination.isCombinationWithSameValueWithOneJoker())
    self.assertFalse(self.sequenceas22_combination.isCombinationWithSameValueWithOneJoker())
    self.assertFalse(self.sequenceas20_combination.isCombinationWithSameValueWithOneJoker())
    self.assertFalse(self.jokers_combination.isCombinationWithSameValueWithOneJoker())
  
  def testIsCombinationOfJokers(self):
    self.assertTrue(self.jokers_combination.isCombinationOfJokers())
    self.assertFalse(self.sequence_combination.isCombinationOfJokers())
    self.assertFalse(self.sequence_withjoker_combination.isCombinationOfJokers())
    self.assertFalse(self.sequenceas22_combination.isCombinationOfJokers())
    self.assertFalse(self.sequenceas20_combination.isCombinationOfJokers())
    self.assertFalse(self.samevalue_combination.isCombinationOfJokers())
    self.assertFalse(self.samevaluewithjoker_combination.isCombinationOfJokers())
    
  # Canastras

  def testIsCleanCanastra(self):
    self.assertTrue(self.sequence_canastra.isCleanCanastra())
    self.assertFalse(self.sequence_withjoker_canastra.isCleanCanastra())
    self.assertTrue(self.real_canastra.isCleanCanastra())
    self.assertFalse(self.realwithjoker_canastra.isCleanCanastra())
    self.assertTrue(self.samevalue_canastra.isCleanCanastra())
    self.assertFalse(self.samevaluewithjoker_canastra.isCleanCanastra())
    self.assertFalse(self.jokers_canastra.isCleanCanastra())
  
  def testIsCanastraWithJoker(self):
    self.assertFalse(self.sequence_canastra.isCanastraWithJoker())
    self.assertTrue(self.sequence_withjoker_canastra.isCanastraWithJoker())
    self.assertFalse(self.real_canastra.isCanastraWithJoker())
    self.assertTrue(self.realwithjoker_canastra.isCanastraWithJoker())
    self.assertFalse(self.samevalue_canastra.isCanastraWithJoker())
    self.assertTrue(self.samevaluewithjoker_canastra.isCanastraWithJoker())
    self.assertFalse(self.jokers_canastra.isCanastraWithJoker())
  
  def testIsRealCanastra(self):
    self.assertFalse(self.sequence_canastra.isRealCanastra())
    self.assertFalse(self.sequence_withjoker_canastra.isRealCanastra())
    self.assertTrue(self.real_canastra.isRealCanastra())
    self.assertFalse(self.realwithjoker_canastra.isRealCanastra())
    self.assertFalse(self.samevalue_canastra.isRealCanastra())
    self.assertFalse(self.samevaluewithjoker_canastra.isRealCanastra())
    self.assertFalse(self.jokers_canastra.isRealCanastra())
  
  def testIsCanastraOfJokers(self):
    self.assertFalse(self.sequence_canastra.isCanastraOfJokers())
    self.assertFalse(self.sequence_withjoker_canastra.isCanastraOfJokers())
    self.assertFalse(self.real_canastra.isCanastraOfJokers())
    self.assertFalse(self.realwithjoker_canastra.isCanastraOfJokers())
    self.assertFalse(self.samevalue_canastra.isCanastraOfJokers())
    self.assertFalse(self.samevaluewithjoker_canastra.isCanastraOfJokers())
    self.assertTrue(self.jokers_canastra.isCanastraOfJokers())
  
  def testScoreOfCanastra(self):
    self.assertEquals(0, self.sequence_combination.scoreOfCanastra())
    self.assertEquals(100, self.sequence_withjoker_canastra.scoreOfCanastra())
    self.assertEquals(200, self.sequence_canastra.scoreOfCanastra())
    self.assertEquals(500, self.jokers_canastra.scoreOfCanastra())
    self.assertEquals(1000, self.real_canastra.scoreOfCanastra())
  
  # Valid combinations
  
  def testCombinationWithLessThan3Cards(self):
    deck = hole.StackOfCards()
    deck.pushAll([cards.Card(1, 1), cards.Card(1, 1)])
    self.assertFalse(deck.isValidCombination())
    
  def testCombinationWithMoreThan14Cards(self):
    deck = hole.StackOfCards()
    for x in range(15): deck.push(cards.Card(1, 1))
    self.assertFalse(deck.isValidCombination())
    
  def testSequenceWithSameSuit(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('3-1 4-1 5-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('12-2 13-2 11-2'))
    self.assertTrue(deck.isValidCombination())

  def testSequenceWithDifferentSuit(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('3-1 4-1 5-2'))
    self.assertFalse(deck.isValidCombination())

  def testSameValueAndDifferentSuits(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 1-2 1-3'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('2-1 2-2 2-3'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('13-2 13-2 13-3'))
    self.assertTrue(deck.isValidCombination())
    
  def testCombinationOfTwoAndJokers(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('2-1 2-2 0-0'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('2-1 2-2 0-0 2-5 0-0'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('2-1 2-2 0-0 2-5 1-0'))
    self.assertFalse(deck.isValidCombination())

  def testCombinationWithAS23(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 3-1'))
    self.assertTrue(deck.isValidCombination())
    
  def testCombinationWithQKAS(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('12-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    
  def testInvalidCombinationWithQKAS(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('10-1 12-1 13-1 1-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('11-2 12-1 13-1 1-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 12-1 13-1 1-1'))
    self.assertFalse(deck.isValidCombination())
    
  def testRealCanastra(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1 2-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('3-1 4-1 5-2 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1 2-1 3-1'))
    self.assertFalse(deck.isValidCombination())

  def testRealCanastraWithJoker(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-2 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 0-0 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 2-2 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 0-0 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 3-2 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('1-2 2-2 3-2 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('1-2 2-1 3-2 0-0 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 1-1'))
    self.assertFalse(deck.isValidCombination())

  def testCardsWithDifferentValuesThatIsNotSequenceAndDontHaveJoker(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('10-1 12-1 13-1'))
    self.assertFalse(deck.isValidCombination())
    
  def testCombinationWithJoker(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('2-2 10-1 12-1 13-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 10-1 12-1 13-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 10-1 12-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 10-1 11-1'))
    self.assertTrue(deck.isValidCombination())
    
  def testCombinationWithTwoCardsWithSameValueAndJoker(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 8-1 8-2'))
    self.assertTrue(deck.isValidCombination())
    
  def testCombinationWithAS2Joker(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 0-0'))
    self.assertTrue(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 0-0 3-1'))
    self.assertTrue(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 2-2'))
    self.assertTrue(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 2-2 3-1'))
    self.assertTrue(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-1 2-2 3-2'))
    self.assertFalse(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('1-1 2-2 2-2'))
    self.assertFalse(deck.isValidCombination())
    
  def testCombinationWithQKASJoker(self):
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 12-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 11-1 13-1 1-1'))
    self.assertTrue(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 11-1 12-1 1-1'))
    self.assertTrue(deck.isValidCombination())

    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 8-1 10-1 12-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 0-0 8-1 10-1 12-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 0-0 11-1 13-1 1-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 0-0 10-1 12-1 1-1'))
    self.assertFalse(deck.isValidCombination())
    
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 11-1 12-2 1-1'))
    self.assertFalse(deck.isValidCombination())
    deck = hole.StackOfCards(cards.strToStackOfCards('0-0 11-1 12-1 1-2'))
    self.assertFalse(deck.isValidCombination())
    
#    orderCombinationsByScore
#    orderCombinationsByNumberOfCards
#    orderCombinationsByNumberOfCardsAndScore
#    orderCombinationsByScoreAndNumberOfCards

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
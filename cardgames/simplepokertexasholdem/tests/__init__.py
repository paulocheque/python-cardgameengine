'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest

from gameengine import commands, players, errors
from cardgameengine.constants import *
from cardgameengine import cards, cardgame

from cardgames import simplepokertexasholdem

###############################################################################
# [optional] 0): Define base class with common data to clear testcases

class GameTestsHelper(unittest.TestCase):

  def setUp(self):
    
    self.players = [players.Player('Player1', 
                                   strategy=simplepokertexasholdem.Strategy(), 
                                   contextClass=simplepokertexasholdem.Context), 
                    players.Player('Player2', 
                                   strategy=simplepokertexasholdem.Strategy(), 
                                   contextClass=simplepokertexasholdem.Context)]

    self.player = self.players[0]
    self.strategy = self.player.strategy
    self.context = self.player.context
    
    self.params = None
    self.startGameCommand = simplepokertexasholdem.StartGameCommand()
    self.endGameCommand = simplepokertexasholdem.EndGameCommand()
    self.startGameRoundCommand = simplepokertexasholdem.StartGameRoundCommand()
    self.endGameRoundCommand = simplepokertexasholdem.EndGameRoundCommand()
    self.stepGameCommand = simplepokertexasholdem.StepCommand()
    
    self.playerPlaysCommand = simplepokertexasholdem.PlayerPlaysGameCommand()
    self.giveUpCommand = simplepokertexasholdem.FoldCommand(self.player, self.params)
    self.giveUpShowingTheCardsCommand = simplepokertexasholdem.FoldShowingTheCardsCommand(self.player, self.params)
    self.betCommand = simplepokertexasholdem.BetCommand(self.player, self.params)
    self.payCommand = simplepokertexasholdem.PayCommand(self.player, self.params)
    self.allInCommand = simplepokertexasholdem.AllInCommand(self.player, self.params)
    
    self.roundreport = simplepokertexasholdem.RoundReport()
    self.report = simplepokertexasholdem.GameReport()
    self.configurations = simplepokertexasholdem.Configurations()
    self.deckPrototype = self.configurations.deckPrototype.clone()
    
    self.game = simplepokertexasholdem.Game(self.players, self.configurations)
    self.round = simplepokertexasholdem.Round(self.game, self.players[:], self.configurations, self.game.commandsManager)
    self.round.currentPlayer = self.player
    self.game.currentRound = self.round

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class CardTests(GameTestsHelper):
  
  def testValues(self):
    self.assertEquals(cards.VALUES_ANGLO_AMERICAN, 
                      simplepokertexasholdem.Card.values)
    
  def testSuits(self):
    self.assertEquals(cards.SUITS_ANGLO_AMERICAN, 
                      simplepokertexasholdem.Card.suits)
    
###############################################################################
# [optional] 2) Define configurations of the game

class ConfigurationsTests(GameTestsHelper):

  def setUp(self):
    super(ConfigurationsTests, self).setUp()
    self.deckPrototype = simplepokertexasholdem.Configurations().deckPrototype.clone()

  def testHeight(self):
    self.assertEquals(52, len(self.deckPrototype.cards))
    
  def testContainCards(self):
    self.assertFalse(self.deckPrototype.containsCard(simplepokertexasholdem.Card(0, 0)))
    self.assertFalse(self.deckPrototype.containsCard(simplepokertexasholdem.Card(15, 4)))
    
  def testScore(self):
    self.assertEquals(0, self.deckPrototype.popCard(simplepokertexasholdem.Card(13, 4)).score)
    self.assertEquals(0, self.deckPrototype.popCard(simplepokertexasholdem.Card(3, 1)).score)

  def testAttributes(self):
    self.assertEquals(-1, self.configurations.timeForCommand)
    self.assertEquals(-1, self.configurations.timeForPlay)
    self.assertEquals(-1, self.configurations.timeForGame)
    self.assertEquals(1000, self.configurations.amountOfChipsPerPlayer)
    self.assertEquals(256, simplepokertexasholdem.Configurations(256).amountOfChipsPerPlayer)
    self.assertEquals(10, self.configurations.roundsPrice)
    self.assertEquals(15, simplepokertexasholdem.Configurations(256, 15).roundsPrice)
    self.assertEquals(100, self.configurations.maxBet)
    self.assertEquals(200, simplepokertexasholdem.Configurations(256, 15, 200).maxBet)
    
###############################################################################
# [required] 3): Define the rules of command's execution

class ContextTests(GameTestsHelper):
  
  def testAttributes(self):
    self.assertEquals(self.player, self.context.player)
    self.assertEquals(None, self.context.currentGamePlayers)
    self.assertEquals(None, self.context.configurations)
    
    self.assertEquals(None, self.context.playercards)
    
    self.assertEquals(0, self.context.step)
    self.assertEquals({}, self.context.playersChips)
    self.assertEquals(None, self.context.communityCards)
    self.assertEquals(0, self.context.pot)
    self.assertEquals(0, self.context.bigBet)
    self.assertEquals(False, self.context.currentPlayerDecided)
    # http://en.wikipedia.org/wiki/Betting_(poker)
  
###############################################################################
# [required] 4) Card game logic

#################################
# [optional] 4.1): Define a model of reports to store informations.

class GameReportTests(GameTestsHelper):
  
  def testBasicAttributes(self):
    self.assertEquals([], self.report.players)
    self.assertEquals(0, self.report.initialNumberOfPlayers)
    self.assertEquals(None, self.report.configurations)
    self.assertEquals([], self.report.winners)
    self.assertEquals([], self.report.losers)
    self.assertEquals([], self.report.commands)
    self.assertEquals(0, self.report.durationTime)

#################################s
# [required] 4.2) Create the logic of the game

class GameTests(GameTestsHelper):
  
  def setUp(self):
    super(GameTests, self).setUp()
    
  def testAttributes(self):
    self.game.playersChips
  
  def testValidCommands(self):
    self.assertTrue(simplepokertexasholdem.StartGameCommand in self.game.commandsManager.validCommands)
    self.assertTrue(simplepokertexasholdem.EndGameCommand in self.game.commandsManager.validCommands)
    self.assertTrue(simplepokertexasholdem.PlayerPlaysGameCommand in self.game.commandsManager.validCommands)
    self.assertTrue(simplepokertexasholdem.StepCommand in self.game.commandsManager.validCommands)

    self.assertTrue(simplepokertexasholdem.FoldCommand in self.game.commandsManager.validCommands)
    self.assertTrue(simplepokertexasholdem.FoldShowingTheCardsCommand in self.game.commandsManager.validCommands)
    self.assertTrue(simplepokertexasholdem.BetCommand in self.game.commandsManager.validCommands)
    self.assertTrue(simplepokertexasholdem.PayCommand in self.game.commandsManager.validCommands)
    self.assertTrue(simplepokertexasholdem.AllInCommand in self.game.commandsManager.validCommands)
  
  def testConditionToWin(self):
    self.assertFalse(self.game.conditionToWin(self.players[0]))
    self.assertFalse(self.game.conditionToWin(self.players[1]))
    self.game.players = [self.players[0]] 
    self.assertTrue(self.game.conditionToWin(self.players[0]))
    self.assertFalse(self.game.conditionToWin(self.players[1]))

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
    self.roundreport.typeWinnerCombination

#################################
# [required] 5.2) Create the logic of a round of the game:

class RoundTests(GameTestsHelper):
  
  def testAttributes(self):
    self.round.step
    self.round.communityCards
    self.round.pot
    self.round.currentPlayerDecided
    self.round.winnerCombination
  
  def testConditionToWin(self):
    # TODO
    # todos jogadores desistiram ou no final o ganha o que tem maior jogo 
    self.assertFalse(self.round.conditionToWin(self.players[0]))
    self.assertFalse(self.round.conditionToWin(self.players[1]))
    self.round.players = [self.players[0]] 
    self.assertTrue(self.round.conditionToWin(self.players[0]))
    self.assertFalse(self.round.conditionToWin(self.players[1]))

###############################################################################
# [required] 6): Define game's commands

class StartGameCommandTests(GameTestsHelper):

  def testExecuteMustGiveChips(self):
    self.game.configurations.amountOfChipsPerPlayer = 2350
    self.assertEquals(0, self.game.amountOfChips(self.players[0]))
    self.assertEquals(0, self.game.amountOfChips(self.players[1]))
    self.startGameCommand.execute(self.game)
    self.assertEquals(2350, self.game.amountOfChips(self.players[0]))
    self.assertEquals(2350, self.game.amountOfChips(self.players[1]))
    
class EndGameCommandTests(GameTestsHelper):

  def a_testExecuteMustDoSomething(self): pass
    
class StartGameRoundCommandTests(GameTestsHelper):

  def a_testExecuteMustDoSomething(self): pass
    
class EndGameRoundCommandTests(GameTestsHelper):

  def testExecuteMustMoveBetToWinner(self):
    self.game.currentRound.pot = 1456
    self.round.winners = lambda: [self.players[0]]
    self.endGameRoundCommand.execute(self.game.currentRound)
    self.assertEquals(1456, self.game.amountOfChips(self.players[0]))
    self.assertEquals(0, self.game.currentRound.pot)
    
  def testExecuteMustDivideEvenBetBetweenWinners(self):
    self.game.currentRound.pot = 2000
    self.round.winners = lambda: self.players
    self.endGameRoundCommand.execute(self.game.currentRound)
    self.assertEquals(1000, self.game.amountOfChips(self.players[0]))
    self.assertEquals(1000, self.game.amountOfChips(self.players[1]))
    self.assertEquals(0, self.game.currentRound.pot)
    
  def testExecuteMustDivideOddBetBetweenWinners(self):
    self.game.currentRound.pot = 1001
    self.round.winners = lambda: self.players
    self.endGameRoundCommand.execute(self.game.currentRound)
    self.assertEquals(500.5, self.game.amountOfChips(self.players[0]))
    self.assertEquals(500.5, self.game.amountOfChips(self.players[1]))
    self.assertEquals(0, self.game.currentRound.pot)
    
class PlayerPlaysGameCommandTests(GameTestsHelper):

  def testExecuteMustResetVariableDecided(self):
    self.currentPlayerDecided = True
    self.playerPlaysCommand.execute(self.game.currentRound)
    self.assertFalse(self.game.currentRound.currentPlayerDecided)
    
class StepCommandTests(GameTestsHelper):
  
  def testExecuteMustGiveTwoCardsToEachPlayerAnd3CommunityCardsFirstStep(self):
    self.assertEquals(0, self.game.currentRound.seeCards(self.players[0]).height())
    self.assertEquals(0, self.game.currentRound.seeCards(self.players[1]).height())
    self.assertEquals(0, self.game.currentRound.communityCards.height())
    self.stepGameCommand.execute(self.game.currentRound)
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[0]).height())
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[1]).height())
    self.assertEquals(3, self.game.currentRound.communityCards.height())
    
  def testExecuteMustAddOneCardToCommunityCardsSecondStep(self):
    self.stepGameCommand.execute(self.game.currentRound)
    self.stepGameCommand.execute(self.game.currentRound)
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[0]).height())
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[1]).height())
    self.assertEquals(4, self.game.currentRound.communityCards.height())
    
  def testExecuteMustAddOneCardToCommunityCardsThirdStep(self):
    self.stepGameCommand.execute(self.game.currentRound)
    self.stepGameCommand.execute(self.game.currentRound)
    self.stepGameCommand.execute(self.game.currentRound)
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[0]).height())
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[1]).height())
    self.assertEquals(5, self.game.currentRound.communityCards.height())
    self.assertEquals(None, self.game.currentRound.winnerCombination)
    
  def testExecuteMustAddOneCardToCommunityCardsFourthStep(self):
    self.stepGameCommand.execute(self.game.currentRound)
    self.stepGameCommand.execute(self.game.currentRound)
    self.stepGameCommand.execute(self.game.currentRound)
    self.stepGameCommand.execute(self.game.currentRound)
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[0]).height())
    self.assertEquals(2, self.game.currentRound.seeCards(self.players[1]).height())
    self.assertEquals(5, self.game.currentRound.communityCards.height())
    self.assertNotEquals(None, self.game.currentRound.winnerCombination)
  

###############################################################################
# [required] 7): Define player's commands

class PokerCommandTests(GameTestsHelper):
  
  def testValidate(self):
    self.context.currentPlayerDecided = False
    self.giveUpCommand.validate(self.context)
    
  def testValidateRaiseAnInvalidCommandError(self):
    self.context.currentPlayerDecided = True
    try:
      self.giveUpCommand.validate(self.context)
    except simplepokertexasholdem.AlreadyDecidedInvalidCommandError: pass
    else: self.fail()

class FoldCommandTests(GameTestsHelper):
  
  def testExecuteMustRemovePlayerFromRound(self):
    self.giveUpCommand.execute(self.game.currentRound)
    self.assertEquals(1, len(self.game.currentRound.players))
    self.assertFalse(self.player in self.game.currentRound.players)
    
class FoldShowingTheCardsCommandTests(GameTestsHelper):
  
  def testExecuteMustRemovePlayerFromRound(self):
    self.giveUpShowingTheCardsCommand.execute(self.game.currentRound)
    self.assertEquals(1, len(self.game.currentRound.players))
    self.assertFalse(self.player in self.game.currentRound.players)
    # FIXME showed cards

class BetCommandTests(GameTestsHelper):
  
#  FIXME
#  validate: mais do que tem
#  menos do que o que tem pra cobrir e nao e allin
  
  def testExecuteMustMoveChipsToBet(self):
    self.betCommand.params = 50
    self.betCommand.execute(self.game.currentRound)
    self.assertEquals(50, self.game.currentRound.pot)
    self.assertEquals(-50, self.game.amountOfChips(self.player))

#class PayCommandTests(GameTestsHelper):
#  
#  def testExecuteMustDoSomething(self):
#    self.context.flag = True
#    self.command.validate(self.context)
#    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())

class AllInCommandTests(GameTestsHelper):
  
  def testExecuteMustMoveAllPlayerChipsToBet(self):
    self.game.playersChips[self.player.name] = 467
    self.allInCommand.execute(self.game.currentRound)
    self.assertEquals(467, self.game.currentRound.pot)
    self.assertEquals(0, self.game.amountOfChips(self.player))
    
  
###############################################################################
# [required] 8): Define strategies to a player

class StrategyTests(GameTestsHelper):

  def testPlay(self):
    self.strategy.compulsoryBets(self.game.commandsManager) # roundProce, smallBlind, bigBlind
    self.strategy.preFlop(self.game.commandsManager)
    self.strategy.flop(self.game.commandsManager)
    self.strategy.turn(self.game.commandsManager)
    self.strategy.river(self.game.commandsManager)
#    self.strategy.showdown(self.game.commandsManager)
    
      
###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

# more tests here


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

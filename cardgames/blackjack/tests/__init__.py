'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest

from cardgameengine import cardgame
from cardgameengine import commands
from cardgameengine import players
from cardgameengine import cards
from cardgameengine.constants import *

from cardgames import blackjack

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class BlackJackCardTests(unittest.TestCase):
  
  def testValues(self):
    self.assertEquals([], blackjack.BlackJackCard.values)
    
  def testSuits(self):
    self.assertEquals([], blackjack.BlackJackCard.suits)
    
###############################################################################
# [required] 2): Define the rules of command's execution

class BlackJackRoundContextTests(unittest.TestCase):
  
  def setUp(self):
    self.context = blackjack.BlackJackRoundContext()
    
  def testAttributes(self):
    # self.assertEquals(somevalue, self.context.someattr)
    pass
  
  def testSummary(self):
    self.assertEquals('BlackJackRoundContext', self.context.summary())
    
###############################################################################
# [required] 3): Define player's commands

class BlackJackCommandTests(unittest.TestCase):
  
  def setUp(self):
    self.context = blackjack.BlackJackRoundContext()
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.player = self.players[0]
    self.params = None
    self.game = blackjack.BlackJackCardGame(self.players)
    self.game.newRound()
    self.command = blackjack.BlackJackCommand(self.player, self.params, self.context)
  
  def testIsValid(self):
    self.assertTrue(self.command.isValid())
    # self.context.someflag = False
    self.command.execute(self.game, self.currentRound)
    self.assertFalse(self.command.isValid())
  
  def testExecuteMustDoSomething(self):
    self.command.execute(self.game, self.currentRound)
    self.assertEquals(0, self.game.currentRound.seeBlackJackCards(self.player).height())
  
###############################################################################
# [required] 4): Define strategies to a player

class BlackJackStrategyTests(unittest.TestCase):

  def setUp(self):
    self.deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(blackjack.BlackJackCard, 4, 13, 2, 2)
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = blackjack.BlackJackCardGame(self.players)
    self.round = blackjack.BlackJackRound(self.game, self.players, commands.CommandsManager(self.game))
    self.strategy = blackjack.BlackJackStrategy()
    self.context = blackjack.BlackJackRoundContext()

  def testPlay(self):
    self.strategy.play(self.game.commandsManager, self.context)
      
###############################################################################
# [optional] 5): Define a model of reports to store informations.

class BlackJackRoundReportTests(unittest.TestCase):
  
  def setUp(self):
    self.report = blackjack.BlackJackRoundReport()
  
  def testBasicAttributes(self):
    self.report.players
    self.report.initialNumberOfPlayers
    self.report.durationTime
    self.report.winners
    self.report.commands
    self.report.algorithmsErrors
  
class BlackJackCardGameReportTests(unittest.TestCase):
  
  def setUp(self):
    self.report = blackjack.BlackJackCardGameReport()
  
  def testBasicAttributes(self):
    self.report.players
    self.report.initialNumberOfPlayers
    self.report.durationTime
    self.report.winners
    self.report.roundsReports

###############################################################################
# [required] 6) Create the logic of a round of the game:

class BlackJackRoundTests(unittest.TestCase):
  
  def setUp(self):
    self.deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(blackjack.BlackJackCard, 4, 13, 2, 2)
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = blackjack.BlackJackCardGame(self.players)
    self.round = blackjack.BlackJackRound(self.game, self.players, commands.CommandsManager(self.game))
  
  def testPopulateContext(self):
    context = blackjack.BlackJackRoundContext()
    self.round.populateContext(context)
    # self.assertEquals('', context.attr1)
  
  def testOrganize(self):
    pass
  
  def testEnd(self):
    pass
  
  def testConditionToWin(self): 
    pass

###############################################################################
# [optional] 7) Define configurations of the game

class BlackJackConfigurationsTests(unittest.TestCase):

  def setUp(self):
    self.deckPrototype = blackjack.BlackJackConfigurations().deckPrototype.clone()
    
  def testHeight(self):
    self.assertEquals(108, len(self.deckPrototype.cards))
    
  def testContainCards(self):
    self.assertTrue(self.deckPrototype.containsCard(blackjack.BlackJackCard(0, 0)))
    self.assertFalse(self.deckPrototype.containsCard(blackjack.BlackJackCard(15, 4)))
    
  def testScore(self):
    self.assertEquals(20, self.deckPrototype.popCard(hole.HoleCard(0, 0)).score)
    self.assertEquals(5, self.deckPrototype.popCard(hole.HoleCard(3, 1)).score)

  def testAttributes(self):
    pass
    
###############################################################################
# [required] 8) Create the logic of the game: Probably this is easy to create than BlackJackRound class.

class BlackJackCardGameTests(unittest.TestCase):
  
  def setUp(self):
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = blackjack.BlackJackCardGame(self.players)
  
  def testValidCommands(self):
    self.assertEquals([], blackjack.BlackJackCardGame.validCommands)
  
  def testOrganize(self):
    pass
  
  def testEnd(self):
    pass
  
  def testConditionToWin(self): 
    pass


###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

# more tests here


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
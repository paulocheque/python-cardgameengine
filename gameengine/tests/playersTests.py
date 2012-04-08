'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest
 
from gameengine import players, utils, testhelper, errors, game

###############################################################################
# Player

class PlayerTest(unittest.TestCase):
  
  def setUp(self):
    self.strategy = players.Strategy
    self.context = game.Context
  
  def testPlayerNameAndStrategyAreMandatoryAndContextHasDefaultValue(self):
    strategy = self.strategy()
    player = players.Player('Player1', strategy, self.context)
    self.assertEquals('Player1', player.name)
    self.assertEquals(strategy, player.strategy)
    self.assertTrue(isinstance(player.context, game.Context))
    
  def testPlayerMayReceiveAContextClass(self):
    strategy = self.strategy()
    player = players.Player('Player1', strategy, self.context)
    self.assertEquals('Player1', player.name)
    self.assertEquals(strategy, player.strategy)
    self.assertTrue(isinstance(player.context, self.context))
    
  def testEqualsByName(self):
    self.assertEquals(players.Player('Player1', self.strategy()), players.Player('Player1', self.strategy()))
    self.assertNotEquals(players.Player('Player1', self.strategy()), players.Player('Player2', self.strategy()))
    
  def testOnePlayerPlay(self):
    # abstract method
    try:
      players.Player('Player', self.strategy()).play(None)
    except NotImplementedError: pass
    else: self.fail()
    
  def testPlayerHasTeam(self):
    player = players.Player('Player', strategy=self.strategy(), team=players.Team('myteam'))
    self.assertEquals('myteam', player.team.name)
    
  def testDefaultTeamOfAPlayerIsATeamWithYourName(self):
    self.assertEquals('Player', players.Player('Player', self.strategy()).team.name)
    self.assertEquals('Player', players.Player('Player', self.strategy()).team.players[0].name)
    
  def testStrategyHasLinkToPlayer(self):
    self.assertEquals('Player', players.Player('Player', self.strategy()).strategy.player.name)
    
  def testStrategyHasLinkToContext(self):
    strategy = self.strategy()
    self.assertEquals(players.Player('Player', strategy).context, strategy.context)

###############################################################################
# Team

class TeamTest(unittest.TestCase):
  
  def setUp(self):
    self.strategy = players.Strategy
  
  def testTeamHasName(self):
    team = players.Team('AgileTeam')
    self.assertEquals('AgileTeam', team.name)
    
  def testTeamHasPlayers(self):
    team = players.Team('AgileTeam')
    self.assertEquals([], team.players)
    
  def testEqualsByName(self):
    self.assertEquals(players.Team('AgileTeam1'), players.Team('AgileTeam1'))
    self.assertNotEquals(players.Team('AgileTeam1'), players.Team('AgileTeam2'))
    
  def testTeamHasNumberOfPlayers(self):
    team = players.Team('AgileTeam')
    p = players.Player('Player', self.strategy())
    team.addPlayer(p)
    self.assertEquals(1, team.numberOfPlayers())
    self.assertEquals([p], team.players)


###############################################################################
# Strategy

class StrategyTests(unittest.TestCase):
  
  def testAttributes(self):
    players.Strategy().player
    players.Strategy().context
    
  def testAbstractPlay(self):
    try:
      players.Strategy().play(None)
    except NotImplementedError: pass
    else: self.fail()
  
class RuntimeStrategyTests(testhelper.GameEngineTests):
  
  def testValidSource(self):
    sourcecode = """
    def play(self, commandsManager):
      x = 1
      commandsManger.addCommand(MyCommand, [\'1\', 2])
    """
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except: self.fail()
    
  def testStrategyWithImportsIsMaliciousSource(self):
    sourcecode = """
    import os
    def play(self, commandsManager):
      x = 1
      commandsManger.addCommand(MyCommand, [\'1\', 2])
    """
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except errors.MailiciousStrategyError: pass
    else: self.fail()
    
  def testStrategyWithExecsIsMaliciousSource(self):
    sourcecode = """
    def play(self, commandsManager):
      x = 1
      exec('print('xxx')')
      commandsManger.addCommand(MyCommand, [\'1\', 2])
    """
    text = "def method(self, commandsManager):\n  x = 1\n  commandsManger.addCommand(MyCommand, \'1\'\n  exec('print('xxx')')"
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except errors.MailiciousStrategyError: pass
    else: self.fail()
    
  def testStrategyWithEvalsIsMaliciousSource(self):
    sourcecode = """
    def play(self, commandsManager):
      x = eval('1')
      commandsManger.addCommand(MyCommand, [\'1\', 2])
    """
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except errors.MailiciousStrategyError: pass
    else: self.fail()
    
  def testStrategyWithCompileIsMaliciousSource(self):
    sourcecode = """
    def play(self, commandsManager):
      x = compile('1')
      commandsManger.addCommand(MyCommand, [\'1\', 2])
    """
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except errors.MailiciousStrategyError: pass
    else: self.fail()
    
  def testStrategyWithOpenIsMaliciousSource(self):
    sourcecode = """
    def play(self, commandsManager):
      x = open('filename')
      commandsManger.addCommand(MyCommand, [\'1\', 2])
    """
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except errors.MailiciousStrategyError: pass
    else: self.fail()
                    
  def testStrategyCantGetTheGameObject(self):
    sourcecode = """
    def play(self, commandsManager):
      x = commandsManger.game
    """
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except errors.CheatStrategyError: pass
    else: self.fail()

  def testStrategyWithReservedTermGameIsCheat(self):
    sourcecode = """
    def play(self, commandsManager):
      x = commandsManger
      y = x.game
    """
    strategy = players.RuntimeStrategy(sourcecode)
    try:
      strategy.validate()
    except errors.CheatStrategyError: pass
    else: self.fail()
  
  def testGetGameEnvironmentMustHasContextAndPlayerAndAddCommand(self):
    strategy = players.RuntimeStrategy('')
    player = players.Player('Player', strategy)
    self.assertEquals(player.context, strategy.context)
    localsenv = strategy.getGameEnvironment(self.game.commandsManager)
    self.assertTrue(len(localsenv.keys()) > 5)
    self.assertTrue('context' in localsenv.keys())
    self.assertEquals(player.context, localsenv['context'])
    self.assertEquals(player, localsenv['player'])
    self.assertEquals(self.game.commandsManager.addCommand, localsenv['addCommand'])
    
  def testPythonEnvironmentMustNotHasExecEvalCompileOpen(self):
    strategy = players.RuntimeStrategy('')
    player = players.Player('Player', strategy)
    self.assertEquals(player.context, strategy.context)
    globalsevn = strategy.getPythonEnvironment()
    self.assertTrue('exec' not in globalsevn['__builtins__'].keys())
    self.assertTrue('eval' not in globalsevn['__builtins__'].keys())
    self.assertTrue('compile' not in globalsevn['__builtins__'].keys())
    self.assertTrue('open' not in globalsevn['__builtins__'].keys())

  def testStrategyCanUseALotOfBuiltinsFunctions(self):
    sourcecode = """
x = str({})
x = bool(True)
x = int('1')
x = float('1')
x = complex('1')
x = divmod(1, 1)
x = dict()
x = list()
x = tuple()
x = set()
x = hex(1)
x = oct(1)
x = min([1])
x = max([1])
x = any([1])
x = all([1])
x = sum([])
x = abs(1)
x = len([])
x = filter(True, [])
x = range(1)
x = zip([])
x = slice([])
x = reversed([])
x = sorted([])
x = enumerate([])
x = hash(11)
x = frozenset()
x = iter([])
x = repr(1)
x = ord('1')
x = pow(1, 1)
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode))
    try:
      player.play(self.game.commandsManager)
    except Exception, e: self.fail(str(e))
    
  def testStrategyCanReadPlayerAndContext(self):
    sourcecode = """
player
context.player
context.currentGamePlayers
context.configurations
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode))
    try:
      player.play(self.game.commandsManager)
    except: self.fail()
  
  def testAllRegisteredCommandsInGameAreAccessibleToStrategy(self):
    sourcecode = """
NeutralCommand
InvalidCommand
BuggedCommand
SlowCommand
ParamsCommand
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode))
    try:
      player.play(self.game.commandsManager)
    except: self.fail()
    
    sourcecode = """
UnknownCommand
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode))
    try:
      player.play(self.game.commandsManager)
    except: pass
    else: self.fail()
    
  def testAllRegisteredClassesAccessibleToStrategy(self):
    accessibleClasses = [utils.CombinationGenerator]
    sourcecode = """
generator = CombinationGenerator(2, 1)
while generator.hasNext():
  generator.next()
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode, accessibleClasses))
    try:
      player.play(self.game.commandsManager)
    except: self.fail()
    
    sourcecode = """
clazz = UnregisteredClass()
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode))
    try:
      player.play(self.game.commandsManager)
    except: pass
    else: self.fail()
    
  def testStrategyHasShortcutToAddCommandMethodToCommandsManager(self):
    sourcecode = """
addCommand(NeutralCommand(player))
# print(id(context))
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode))
    try:
      self.assertEquals(0, len(self.game.commandsManager.executedCommands))
      player.play(self.game.commandsManager)
      self.assertEquals(1, len(self.game.commandsManager.executedCommands))
    except: self.fail()
    
  def testStrategyAccessibleInformationsAndShortcutsMustBeAccessibleInEntireSourceCode(self):
    sourcecode = """
def x():
  addCommand(NeutralCommand(player))
x()
"""
    player = players.Player('Player1', players.RuntimeStrategy(sourcecode))
    try:
      self.assertEquals(0, len(self.game.commandsManager.executedCommands))
      player.play(self.game.commandsManager)
      self.assertEquals(1, len(self.game.commandsManager.executedCommands))
    except: self.fail()
  
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
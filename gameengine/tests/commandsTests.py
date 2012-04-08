'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import time
import threading

import unittest

from gameengine import players, commands, errors, testhelper

class GameCommandTest(testhelper.GameEngineTests):
    
  def testNameMustBeTheClassNameWithoutCommand(self):
    self.assertEquals('Slow', self.slowcommand.name())
    self.assertEquals('Neutral', self.neutralcommand.name())
    
class PlayerCommandTest(testhelper.GameEngineTests):
    
  def testDefaultReturnForIsValidMustBeTrue(self):
    self.assertTrue(self.neutralcommand.isValid(self.context))

  def testValidateMustRaiseAnInvalidCommandErrorIfCommandIsForbiddenByContext(self):
    try:
      self.invalidcommand.validate(self.game)
    except errors.InvalidCommandError: pass
    else: self.fail()

class CommandsManagerTest(testhelper.GameEngineTests):
  
  def testHasGameAndExecutedCommands(self):
    self.assertEquals(self.game, commands.CommandsManager(self.game).game)
    self.assertEquals([], commands.CommandsManager(self.game).executedCommands)
    
  def testValidateMustRaiseAnUnknownCommandErrorIfCommandIsNotInTheList(self):
    try:
      self.game.commandsManager.validateRegisteredCommand(self.unknowncommand)
    except errors.UnknownCommandError: pass
    else: self.fail()
    
class SynchronousCommandsManagerTest(testhelper.GameEngineTests):
  
  def testHasGameAndExecutedCommands(self):
    self.assertEquals(self.game, commands.SynchronousCommandsManager(self.game).game)
    self.assertEquals([], commands.SynchronousCommandsManager(self.game).executedCommands)
    
class AsynchronousCommandsManagerTest(testhelper.GameEngineTests):
  
  def setUp(self):
    super(AsynchronousCommandsManagerTest, self).setUp()
    commandsManager = commands.AsynchronousCommandsManager()
    commandsManager.registerCommand(testhelper.FinishCommand)
    commandsManager.registerCommand(testhelper.NeutralCommand)
    commandsManager.registerCommand(testhelper.InvalidCommand)
    commandsManager.registerCommand(testhelper.BuggedCommand)
    commandsManager.registerCommand(testhelper.SlowCommand)
    commandsManager.registerCommand(testhelper.ParamsCommand)
    commandsManager.game = self.game
    self.game.commandsManager = commandsManager
  
  def testHasGameAndExecutedCommands(self):
    self.assertEquals([], commands.AsynchronousCommandsManager().executedCommands)
    
  def testNextCommandMustReturnTheFirstElementOfTheQueue(self):
    self.game.commandsManager.addCommand(self.neutralcommand)
    self.game.commandsManager.addCommand(self.paramscommand)
    self.assertEquals(self.neutralcommand, self.game.commandsManager.popEvent())
    self.assertEquals(self.paramscommand, self.game.commandsManager.popEvent())
    
  def testStartMustRunInAnotherThread(self):
    threads = threading.activeCount()
    self.game.commandsManager.start()
    self.assertEquals(threads + 1, threading.activeCount())
    
  def testStartMustConsumeValidCommands(self):
    self.game.commandsManager.start()
    self.game.commandsManager.addCommand(self.slowcommand)
    self.game.commandsManager.addCommand(self.paramscommand)
    self.game.commandsManager.addCommand(self.neutralcommand)
    self.assertEquals(3, self.game.commandsManager.queueHeight())
    time.sleep(1)
    self.assertEquals(3, len(self.game.commandsManager.executedCommands))
  
  def testStartMustRaiseAnExceptionForUnknownCommands(self):
    try:
      self.game.commandsManager.executeCommand(self.unknowncommand)
    except errors.UnknownCommandError: pass
    else: self.fail()
    self.assertEquals(0, len(self.game.commandsManager.executedCommands))
    self.assertEquals(0, self.slowcommand.durationTime)
    
  def testStartMustRaiseAnExceptionForInvalidCommands(self):
    try:
      self.game.commandsManager.executeCommand(self.invalidcommand)
    except errors.InvalidCommandError: pass
    else: self.fail()
    self.assertEquals(0, len(self.game.commandsManager.executedCommands))
    self.assertEquals(0, self.slowcommand.durationTime)

  def testStartMustRaiseAnExceptionForBuggedCommands(self):
    try:
      self.game.commandsManager.executeCommand(self.buggedcommand)
    except errors.BuggedCommandError: pass
    else: self.fail()
    self.assertEquals(0, len(self.game.commandsManager.executedCommands))
    self.assertEquals(0, self.slowcommand.durationTime)
    
  def testStartMustRaiseAnExceptionForSlowCommands(self):
    try:
      self.game.configurations.timeForCommand = 0.1
      self.game.commandsManager.executeCommand(self.slowcommand)
    except errors.TimeoutCommandError: pass
    else: self.fail()
    self.assertEquals(0, len(self.game.commandsManager.executedCommands))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest
from gameengine import game, players, factory, testhelper

class GameFactoryTests(testhelper.GameEngineTests):
  
  def testCreationOfOnePlayer(self):
    mapPlayersToStrategy = {'Player1': self.strategy()}
    players = self.gamefactory.createPlayers(mapPlayersToStrategy)
    self.assertEquals(1, len(players))
    self.assertEquals('Player1', players[0].name)
    self.assertTrue(isinstance(players[0].strategy, self.strategy))
    self.assertEquals('Player1', players[0].team.name)
    
  def testCreationOfTwoPlayersFreeForAll(self):
    mapPlayersToStrategy = {'Player1': self.strategy(), 'Player2': self.strategy()}
    players = self.gamefactory.createPlayers(mapPlayersToStrategy)
    self.assertEquals(2, len(players))
    self.assertEquals('Player1', players[0].name)
    self.assertEquals('Player2', players[1].name)
    self.assertTrue(isinstance(players[0].strategy, self.strategy))
    self.assertTrue(isinstance(players[1].strategy, self.strategy))
    self.assertNotEquals(id(players[0].strategy), id(players[1].strategy))
    self.assertEquals('Player1', players[0].team.name)
    self.assertEquals('Player2', players[1].team.name)
    
  def testCreationOfPlayersWithTeamsAndWithoutTeams(self):
    mapPlayersToStrategy = {'Player1': self.strategy(), 'Player2': self.strategy()}
    mapPlayersTeams = {'Player1': 'Team1'}
    players = self.gamefactory.createPlayers(mapPlayersToStrategy, mapPlayersTeams)
    self.assertEquals('Team1', players[0].team.name)
    self.assertEquals('Player2', players[1].team.name)
    
  def testCreationOfPlayersWithAllPlayersInTheSameTeam(self):
    mapPlayersToStrategy = {'Player1': self.strategy(), 'Player2': self.strategy()}
    mapPlayersTeams = {'Player1': 'Team1', 'Player2': 'Team1'}
    players = self.gamefactory.createPlayers(mapPlayersToStrategy, mapPlayersTeams)
    self.assertEquals('Team1', players[0].team.name)
    self.assertEquals('Team1', players[1].team.name)
    
  def testCreationOfPlayersWithEachPlayerInADifferentTeam(self):
    mapPlayersToStrategy = {'Player1': self.strategy(), 'Player2': self.strategy()}
    mapPlayersTeams = {'Player1': 'Team1', 'Player2': 'Team2'}
    players = self.gamefactory.createPlayers(mapPlayersToStrategy, mapPlayersTeams)
    self.assertEquals('Team1', players[0].team.name)
    self.assertEquals('Team2', players[1].team.name)
    
  def testStringStrategyMustBeConvertedToRuntimeStrategy(self):
    mapPlayersToStrategy = {'Player1': 'some source code'}
    listOfPlayers = self.gamefactory.createPlayers(mapPlayersToStrategy)
    self.assertTrue(isinstance(listOfPlayers[0].strategy, players.RuntimeStrategy))
    self.assertEquals('some source code', listOfPlayers[0].strategy.sourcecode)
    
  def testPlayerContextMustBeDecidedByFactory(self):
    mapPlayersToStrategy = {'Player1': self.strategy()}
    players = self.gamefactory.createPlayers(mapPlayersToStrategy)
    self.assertTrue(isinstance(players[0].context, self.gamefactory.contextClass))
    
  def testConfigurationsMustBeDecidedByFactory(self):
    mapOfConfigurations = {}
    configurations = self.gamefactory.createConfiguration(mapOfConfigurations)
    self.assertTrue(isinstance(configurations, self.gamefactory.configurationsClass))
    
  def testCreationOfConfigurations(self):
    mapOfConfigurations = {'timeForPlay': 156}
    configurations = self.gamefactory.createConfiguration(mapOfConfigurations)
    self.assertEquals(156, configurations.timeForPlay)
    
  def testCreateMustReturnGameWithPlayersAndConfigurations(self):
    mapPlayersToStrategy = {'Player1': self.strategy()}
    mygame = self.gamefactory.createGame(mapPlayersToStrategy)
    self.assertTrue(isinstance(
                    mygame, 
                    testhelper.MyGame))
    self.assertTrue(isinstance(
                    mygame.players[0].context, 
                    testhelper.MyPlayerContext))
    self.assertTrue(isinstance(
                    mygame.configurations, 
                    testhelper.MyConfigurations))
    
  def testCreateCanAcceptTeams(self):
    mapPlayersToStrategy = {'Player1': self.strategy(), 'Player2': self.strategy()}
    mapPlayersTeams = {'Player1': 'Team1', 'Player2': 'Team2'}
    mygame = self.gamefactory.createGame(mapPlayersToStrategy, mapPlayersTeams)
    
  def testCreateCanAcceptConfigurations(self):
    mapPlayersToStrategy = {'Player1': self.strategy(), 'Player2': self.strategy()}
    mapPlayersTeams = {'Player1': 'Team1', 'Player2': 'Team2'}
    mapOfConfigurations = {'timeForPlay': 156}
    mygame = self.gamefactory.createGame(mapPlayersToStrategy, mapPlayersTeams, mapOfConfigurations)
    
class FactoryManagerTests(testhelper.GameEngineTests):
  
  def setUp(self):
    super(FactoryManagerTests, self).setUp()
    self.manager = factory.FactoryManager()
  
  def testAddRemoveFactory(self):
    self.assertEquals(0, len(self.manager.registeredFactories))
    self.manager.addFactory(testhelper.MyGameFactory())
    self.assertEquals(1, len(self.manager.registeredFactories))
    self.assertEquals(testhelper.MyGameFactory, self.manager.registeredFactories['My'].__class__)
    self.manager.removeFactory(testhelper.MyGameFactory())
    self.assertEquals(0, len(self.manager.registeredFactories))
    
  def testCreateGame(self):
    self.assertEquals(0, len(self.manager.registeredFactories))
    self.manager.addFactory(testhelper.MyGameFactory())
    self.assertEquals(1, len(self.manager.registeredFactories))
    mapPlayersToStrategy = {'Player1': self.strategy()}
    mygame = self.manager.createGame('My', mapPlayersToStrategy)
    self.assertTrue(isinstance(mygame, testhelper.MyGame))
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
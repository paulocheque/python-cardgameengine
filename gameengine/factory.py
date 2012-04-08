'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

from gameengine import game, players

# Abstract Factory
# TODO: follow conventions and create a generic factory: 
# for key, value in self.module.__dict__.items():
class GameFactory(object):
  
  def __init__(self, gameClass, contextClass, configurationsClass, accessibleClasses=[]):
    self.gameClass = gameClass
    self.contextClass = contextClass
    self.configurationsClass = configurationsClass
    self.accessibleClasses = accessibleClasses
  
  def createGame(self, mapPlayersToStrategy, mapPlayersTeams={}, mapOfConfigurations=None):
    listOfPlayers = self.createPlayers(mapPlayersToStrategy, mapPlayersTeams)
    configurations = self.createConfiguration(mapOfConfigurations)
    return self.gameClass(players=listOfPlayers, configurations=configurations)
  
  def createConfiguration(self, mapOfConfigurations):
    configurations = self.configurationsClass()
    if mapOfConfigurations != None:
      for key, value in mapOfConfigurations.items():
        configurations.__dict__[key] = value
    return configurations
  
  def createPlayers(self, mapPlayersToStrategy, mapPlayersTeams={}):
    listOfPlayers = []
    for playerName, strategy in sorted(mapPlayersToStrategy.items()):
      if isinstance(strategy, basestring): # string or unicode 
        strategy = players.RuntimeStrategy(strategy, self.accessibleClasses)
      if playerName in mapPlayersTeams.keys():
        team = players.Team(mapPlayersTeams[playerName])
        listOfPlayers.append(players.Player(playerName, strategy, team, contextClass=self.contextClass))
      else:
        listOfPlayers.append(players.Player(playerName, strategy, contextClass=self.contextClass))
    return listOfPlayers
  
class FactoryManager(object):
  
  def __init__(self):
    self.registeredFactories = {}
  
  def addFactory(self, factory):
    self.registeredFactories.update({factory.gameClass.name(): factory})
    
  def removeFactory(self, factory):
    del(self.registeredFactories[factory.gameClass.name()])
    
  def createGame(self, game, mapPlayersToStrategy, mapPlayersTeams={}, mapOfConfigurations=None):
    return self.registeredFactories[game].createGame(mapPlayersToStrategy, 
                                                       mapPlayersTeams, 
                                                       mapOfConfigurations)
  
  
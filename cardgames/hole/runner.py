'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

from cardgames import hole

class BasicStrategy(hole.Strategy):
  '''
  GetDiscardedCardsCommand
  GetOneCardOfTheDeckCommand
  PutCardsInCombinationCommand
  MakeNewCombinationCommand
  DiscardCommand
  '''
  
  def getCardFromDeckOrCardsFromDiscardedCards(self, addCommand, context):
    command = None
    
    # Se esta para bater, compra do baralho
    context.playercards = hole.StackOfCards(context.playercards)
    if context.playercards.isValidCombination():
      command = hole.GetOneCardOfTheDeckCommand(self.player)
    else:
      aux = hole.StackOfCards()
      aux.pushAll(context.discardedCards)
      aux.pushAll(context.playercards)
      listOfStacks1 = aux.allValidCombinationOfCards()
      listOfStacks2 = context.playercards.allValidCombinationOfCards()
      # Se as cartas da mesa sao uteis para se montar um jogo, entao compra da mesa
      if len(listOfStacks2) > len(listOfStacks1):
        command = hole.GetDiscardedCardsCommand(self.player)
      # caso contrario compra do baralho
      else:
        command = hole.GetOneCardOfTheDeckCommand(self.player)
    addCommand(command)
  
  def createCombinations(self, addCommand, context):
    combinations = context.teamsCombinations[self.player.team.name]
    for index in range(len(combinations)):
      combination = combinations[index]
      for card in context.playercards.cards:
        aux = hole.StackOfCards()
        aux.pushAll(combination)
        aux.pushAll(card)
        if aux.isValidCombination():
          # Se da para baixar alguma carta na maior combinacao, entao baixa
          command = hole.PutCardsInCombinationCommand(self.player, [index, card])
          addCommand(command)
    
    context.playercards = hole.StackOfCards(context.playercards)
    listOfStacks = context.playercards.allValidCombinationOfCards()
    # Se tem alguma combinacao para baixar, entao baixa
    if len(listOfStacks) > 0:
      # Se ja tem canastra, entao baixa a com mais pontos
      if context.teamCanHit(self.player.team):
        hole.StackOfCards.orderCombinationsByScoreAndNumberOfCards(listOfStacks)
        command = hole.MakeNewCombinationCommand(self.player, listOfStacks.pop())
        addCommand(command)
      # Se ainda nao tem canastra, entao tambem baixa a mais alta tambem 
      else:
        hole.StackOfCards.orderCombinationsByNumberOfCardsAndScore(listOfStacks)
        command = hole.MakeNewCombinationCommand(self.player, listOfStacks.pop())
        addCommand(command)
  
  def discard(self, addCommand, context):
    # baixa carta mais alta
    context.playercards.sortByScore()
    command = hole.DiscardCommand(self.player, context.playercards.seeLastCard())
    addCommand(command)

sourcecode = u'''
command = None

def getCardFromDeckOrCardsFromDiscardedCards():
  #############################################################################
  if len(context.teamsHaveAlreadyHit) == 0:
    
    tmp = StackOfCards()
    tmp.pushAll(context.playercards)
    mycombinations = None
    
    if context.playercards.isValidCombination():
      addCommand(GetOneCardOfTheDeckCommand(player))
    else:
      #############################################
      # priority to sequences
      
      numberofsequences = 0
      
      while True:
        mycombinations = tmp.allValidCombinationOfCards()
        StackOfCards.orderCombinationsByNumberOfCards(mycombinations)
      
        breakloop = True
        
        while len(mycombinations) > 0:
          combination = mycombinations.pop()
          if combination.isSequenceWithSameSuit() or combination.isSequenceWithSameSuitWithOneJoker():
            tmp.popCards(combination)
            numberofsequences += 1
            breakloop = False
            break
          
        if breakloop: break
      
      #############################################
      # try to hit: priority to same value
      
      numberofsamevalue = 0
      
      while True:
        mycombinations = tmp.allValidCombinationOfCards()
        StackOfCards.orderCombinationsByNumberOfCards(mycombinations)
      
        breakloop = True
        
        if len(mycombinations) > 0:
          combination = mycombinations.pop()
          tmp.popCards(combination)
          numberofsamevalue += 1
          breakloop = False
          
        if breakloop: break
      
      #############################################
      # examine discardedcards
      
      numberofnewcombinations = 0
      tmp.pushAll(context.discardedCards)
      mycombinations = tmp.allValidCombinationOfCards()
      if len(mycombinations) > 0:
        addCommand(GetDiscardedCardsCommand(player))
      else:
        addCommand(GetOneCardOfTheDeckCommand(player))
    
  #############################################################################
  else: # some team have already hitted
    #############################################################################
    if player.team in teamsHaveAlreadyHit:
      #############################################################################
      if len(context.teamsHaveAlreadyHit) == 1: # just my team has already hitted
        # decide to make points
        if len(context.discardedCards) > 3: addCommand(GetDiscardedCardsCommand(player))
        else: addCommand(GetOneCardOfTheDeckCommand(player))
      #############################################################################
      else:
        # my team need to hit, suppose that another players dont discard useful cards
        addCommand(GetOneCardOfTheDeckCommand(player))
    #############################################################################
    else: # another team has already hitted
      # my team need to hit, suppose that another players dont discard useful cards
      addCommand(GetOneCardOfTheDeckCommand(player))

#############################################################################
def createCombinations():
  
#  command = hole.PutCardsInCombinationCommand(self.player, [index, card])
    
  while True:
    mycombinations = context.playercards.allValidCombinationOfCards()
    StackOfCards.orderCombinationsByNumberOfCards(mycombinations)
  
    breakloop = True
    
    while len(mycombinations) > 0:
      combination = mycombinations.pop()
      if combination.isSequenceWithSameSuit() or combination.isSequenceWithSameSuitWithOneJoker():
        addCommand(MakeNewCombinationCommand(player, combination))
        breakloop = False
        break
    if breakloop: break
  
  #############################################################################
  if len(context.teamsHaveAlreadyHit) == 0:
    pass
  #############################################################################
  else:
    #############################################################################
    if player.team in teamsHaveAlreadyHit:
      #############################################################################
      if len(context.teamsHaveAlreadyHit) == 1:
        pass
      #############################################################################
      else:
        pass
    #############################################################################
    else:
      pass

def discard():
#  mycombinations = context.playercards.allValidCombinationOfCards()
#  StackOfCards.orderCombinationsByNumberOfCards(mycombinations)
  
  addCommand(DiscardCommand(player, context.playercards.seeLastCard()))
  
  #############################################################################
  if len(context.teamsHaveAlreadyHit) == 0:
    pass
  #############################################################################
  else:
    #############################################################################
    if player.team in teamsHaveAlreadyHit:
      #############################################################################
      if len(context.teamsHaveAlreadyHit) == 1:
        pass
      #############################################################################
      else:
        pass
    #############################################################################
    else:
      pass


command = None
if context.discardedCards.isEmpty(): command = GetOneCardOfTheDeckCommand(player)
if context.deckHeight == 0: command = GetDiscardedCardsCommand(player)
if command != None: addCommand(command)
else:
  getCardFromDeckOrCardsFromDiscardedCards()
createCombinations()
discard()
'''

simpleStrategy = u'''
addCommand(GetOneCardOfTheDeckCommand(player))
addCommand(DiscardCommand(player, context.playercards.seeLastCard()))'''

from gameengine import players
interactiveStrategy = players.InteractiveStrategy()
# required
mapPlayersToStrategy = {'Player1': BasicStrategy(), 'Player2': sourcecode}
mapPlayersToStrategy = {'Player1': interactiveStrategy, 'Player2': sourcecode}
#mapPlayersToStrategy = {'Player1': sourcecode}

# [optional]
mapPlayersTeams = {'Player1': 'Team1', 'Player2': 'Team2'}

# optional
mapOfConfigurations = {'timeForCommand': 2, 'timeForPlay': 30, 'timeForGame': 60, 'maximumScore': 1000, 'numberOfDeads': 2}
#mapOfConfigurations = {'timeForCommand': 1, 'timeForPlay': 1, 'timeForGame': 5, 'maximumScore': 1000, 'numberOfDeads': 2}
# BUG timeForGame expires, thread continue executing ate timeForPlay or timeForCommand expires

if __name__ == "__main__":
  game = hole.GameFactory().createGame(mapPlayersToStrategy, mapPlayersTeams, mapOfConfigurations)
  try:
    game.start()
  except:
    print(game.report().summary())
    raise

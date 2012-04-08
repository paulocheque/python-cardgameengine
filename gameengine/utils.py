'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

import threading
from gameengine import threading2

class Error(Exception):
  
  def __init__(self, extra_information=None):
    if extra_information is not None:
      super(Error, self).__init__(self.__doc__ + ': ' + extra_information)
    else:
      super(Error, self).__init__(self.__doc__)

###############################################################################

class Observable(object):
  
  def __init__(self):
    self.observers = []
    
  def registerObserver(self, observer):
    self.observers.append(observer)
    
  def unregisterObserver(self, observer):
    self.observers.remove(observer)
  
  def notifyObservers(self, event):
    for observer in self.observers:
      observer.notify(event)
      
class Observer(object):
  
  def notify(self, event):
    pass
  
###############################################################################

# http://docs.python.org/library/itertools.html
# itertools.combinations(iterable, r)
# itertools.permutations(iterable[, r])

class CombinationGenerator(object):
  
  def __init__(self, n, r):
    if r > n or n < 1: raise Exception('Invalid argument')
    self.n = n
    self.r = r
    # total = n! / r! * (n - r)!
    self.total = self.factorial(n) / self.factorial(r) * self.factorial(n-r)
    self.current = []
    
  def factorial(self, x):
    return (1 if x==0 else x * self.factorial(x-1))
    
  def __firstCombination(self):
    return list(range(self.r))
  
  def __lastCombination(self):
    return list(range(self.n - self.r, self.n))
  
  def __getIndexOfLastValidElementToIncrement(self):
    for index in reversed(range(self.r)):
      possibleValue = self.current[index] + 1
      possibleValueIsValid = (possibleValue <= (self.n - (self.r - index)))
      if possibleValueIsValid:
        return index
    return None
    
  # Algorithm from Rosen
  def next(self):
    '''
    Return a list of indexes
    '''
    if len(self.current) == 0: 
      self.current = self.__firstCombination()
    else:
      theIndex = self.__getIndexOfLastValidElementToIncrement()
      if theIndex == None: 
        self.current = self.__firstCombination()
      else:
        self.current[theIndex] += 1
        ref = self.current[theIndex]
        for index in range(theIndex + 1, self.r):
          ref += 1
          self.current[index] = ref
    return self.current
  
  def hasNext(self):
    return self.current != self.__lastCombination()
  
  def reset(self):
    self.current = []
  
###############################################################################

class AsyncQueueManager(object):
  
  def __init__(self, name):
    self.name = name
    self.__queue = []
    
    self.__control = threading.Condition()
    self.__thread = None
    self.__finishAfterNextEvent = False
  
  # Productor
  def pushEvent(self, event):
    if len(self.__queue) == 0:
      self.__control.acquire()
      self.__pushEvent(event)
      self.__control.notify()
      self.__control.release()
    else:
      self.__pushEvent(event)
    
  def __pushEvent(self, event):
    self.__queue.append(event)
    
  def popEvent(self):
    event = self.__queue.pop(0)
    return event

  def start(self):
    if self.__thread != None: raise Exception('This queue manager has already been started')
    self.__thread = threading2.KThread(target=self.run, name=self.name)
    self.__thread.daemon = True
    self.__thread.start()

  def stop(self):
    if self.__thread is not None: 
      self.__finishAfterNextEvent = True
      self.__control.acquire()
      self.__control.notify()
      self.__control.release()

  # Consumer
  def run(self):
    while not self.__finishAfterNextEvent:
      self.__control.acquire()
      while not self.__finishAfterNextEvent and len(self.__queue) == 0:
        self.__control.wait()
      self.__control.release()
      self.processEvent(self.popEvent())
      
  def processEvent(self, event):
    pass
  
  def queueHeight(self):
    return len(self.__queue)

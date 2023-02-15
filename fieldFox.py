import time
from queue import Queue

class FieldFox:
  
  def __init__(self):
    self.ourTime = Queue(maxSize = 200)
    self.sigStrength = Queue(maxSize = 200)
    self.az = Queue(maxsize = 200)
    self.el = Queue(maxsize = 200)

    #?
  
  def readSig(self):
    return 0

  def sigMakeQsAndLists(self):
    # has a queue of time and signal data
    if(self.ourTime.full() != True):
       self.ourTime.put(time.time())
    else:
      self.ourTime.get()
      self.ourTime.put(time.time())

    if(self.sigStrength.full() != True):
        self.sigStrength.put(self.readSig())
    else:
      self.sigStrength.get()
      self.sigStrength.put(self.readSig())

    if(self.az.full() != True):
        self.az.put(self.readSig())
    else:
      self.az.get()
      self.az.put(self.readSig())

    if(self.el.full() != True):
        self.el.put(self.readSig())
    else:
      self.el.get()
      self.el.put(self.readSig())

    timeList = list(self.ourTime.queue)
    sigList = list(self.sigStrength.queue)
    azList = list(self.az.queue)
    elList = list(self.el.queue)

    return timeList, sigList, azList, elList
    
  def orientPol():
    return
    # rotate feed to angle of polarization? is this angle known?
    
  def findPeakSig():
    return
    # moves up/down left/right till polarization reaches max
    
  def maintainPeakSig():
    return
    # if gain decreases, rerun findPeakPol

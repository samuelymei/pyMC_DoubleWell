#!/usr/bin/env python

class state:
  def __potential(self,xi):
    from math import sqrt
    return xi**2 + 1.0 - sqrt(4*xi**2 + 0.04)

  def __init__(self, x0, T):
    self.x = x0
    self.temperature = T
    self.U = self.__potential(self.x)

  def MC_propagate(self):
    import random
    from math import exp
    xtrial = self.x + random.random() - 0.5
    Utrial = self.__potential(xtrial)
    if Utrial < self.U :
      self.x = xtrial
      self.U = Utrial
      iaccepted = 1
    elif exp(-(Utrial-self.U)/self.temperature) > random.random() :
      self.x = xtrial
      self.U = Utrial
      iaccepted = 1
    else :
      self.x = self.x
      self.U = self.U
      iaccepted = 0
    return iaccepted

  def write_state(self,fout,istep,iaccepted):
    xi = self.x
    Ui = self.U
    fout.write("%(istep)10d %(xi)8.3f %(Ui)8.3f %(iaccepted)2d\n" %vars())

##########################################################################################
# End of Class state
##########################################################################################

def getPara():
    try:
      T = float(raw_input("input temperature: "))
      assert T > 0.0
    except (ValueError, AssertionError), e:
      print 'input a positive float number for Temperature'
      print e
    
    try:
      x0 = float(raw_input("input initial position: "))
    except ValueError:
      print 'input a float number for initial position'

    try:
      Nstep = int(raw_input("input the number of MC steps: "))
      assert Nstep > 0
    except (ValueError, AssertionError), e:
      print 'input a positive integer number for MC steps'
      print e

    trajfile = raw_input("input the trajectory file: ")
    return T, x0, Nstep, trajfile

def runWithDefaultPara():
    s = state(-1.0, 0.4)
    Nstep = 100000
    trajfile = 'traj.out'
    istep = 1
    fout = open(trajfile,'w')
    while istep <= Nstep :
      iaccepted = s.MC_propagate()
      s.write_state(fout,istep,iaccepted)
      istep += 1
    fout.close()

def runWithCustomizedPara():
   T, x0, Nstep, trajfile = getPara()
   s = state(x0, T)
   fout = open(trajfile,'w')
   istep = 1
   while istep <= Nstep :
      iaccepted = s.MC_propagate()
      s.write_state(fout,istep,iaccepted)
      istep += 1
   fout.close()

if __name__ == '__main__': runWithDefaultPara()


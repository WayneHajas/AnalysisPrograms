#Functions to make queries specific to geoducks.  There are corresponding units for other animals.
from numpy import log,exp
from numpy.random import normal

def QnumDepthCount(key):
    result= 'SELECT cint(Density.TransDist/5.) as QuadNum, '
    result+='iif (Density.DepthCorM is NULL,-100,Density.DepthCorM)as   Depth, '
    result+='iif(Density.NumGdkLeft  is NULL,0,Density.NumGdkLeft)+'
    result+='iif(Density.NumGdkRight is NULL,0,Density.NumGdkRight)  as CountTotal '
    result+='FROM Headers INNER JOIN Density ON Headers.Key = Density.HKey '
    result+='WHERE (((Headers.Key)='
    result+=str(key)
    result+=') AND ((Density.QuadratNum)>0) and  (Density.QuadratNum  Is Not Null)  ) '
    result+='ORDER BY Density.QuadratNum;'

    return(result)
def QuadWithMeas(key):return(None)

QuadArea=10.
TranWidth=2.0
species='californicus'

class AlloEqn:
    def __init__(self):
        return

    def DetermAE(self):
        return(None)

    def AvgWgtDetermAE(self):
        return(None)

    def RndAE(self):
        return(None)

    def AvgWgtRndAE(self):
        return(None)
                             
        
        

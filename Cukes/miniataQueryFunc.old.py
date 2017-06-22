#Functions to make queries specific to californicus (commercially harvested species of sea cucumber).  There are corresponding units for other animals.
from numpy import log,exp
from numpy.random import normal

def QnumDepthCount(key):
    result= 'SELECT Densities.QuadratNum as QuadNum, '
    result+='iif (Densities.ChartDepth is NULL,-100,Densities.ChartDepth)as   Depth, '
    result+='Densities.CountC_Miniata  as CountTotal '
    result+='FROM Headers INNER JOIN Densities ON Headers.Key = Densities.HKey '
    result+='WHERE (((Headers.Key)='
    result+=str(key)
    result+=') AND ((Densities.QuadratNum)>0) and  (Densities.QuadratNum  Is Not Null)  ) '
    result+='ORDER BY Densities.QuadratNum;'

    return(result)
def QuadWithMeas(key):return(None)


QuadArea=10.
TranWidth=2.0
species='miniata'

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
                             
        
        

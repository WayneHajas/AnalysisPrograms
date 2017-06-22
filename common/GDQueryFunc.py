#Functions to make queries specific to GSU.  There are corresponding units for other animals.
from numpy import log,exp
from numpy.random import normal

def QnumDepthCount(key):
    result= 'SELECT Density.QuadratNum AS QuadNum,  '
    result+='Density.DepthCorM AS Depth,  '
    result+='Density.NumGdkLeft+Density.NumGdkRight AS CountTotal '
    result+='FROM Headers INNER JOIN Density ON Headers.Key = Density.HKey '
    result+='WHERE (((Density.QuadratNum)<>0) AND ((Headers.Key)= '
    result+=str(key)
    result+=')) '
    result+='ORDER BY Density.QuadratNum;'
    
    return(result)

def MeasInQuad(key,qnum):
    return(None)

def QuadWithMeas(key):
    return(None)

QuadArea=10.0
TranWidth=2.0

#There are no length or weight measurements for geoducks.  Therefore this class is trivial.
class AlloEqn:
    def __init__(self,mnlw30=2.41753,sdlnw30=0.129231,mnbeta=2.754085,sdbeta=0.00699,sigmawithin=0.122298):
        return
    def DetermAE(self):
        return(None)
    def AvgWgtDetermAE(self):
        return(None)
    def RndAE(self):
        return(None)
    def AvgWgtRndAE(self):
        return(None)
                             
        
        

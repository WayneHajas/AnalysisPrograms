#Functions to make queries specific to GSU.  There are corresponding units for other animals.
from numpy import log,exp
from numpy.random import normal

def QnumDepthCount(key):
    result= 'SELECT Density.QuadratNum as QuadNum, '
    result+='iif (Density.ChartDepth is NULL,-100,Density.ChartDepth)as   Depth, '
    result+='Density.CountTotal as CountTotal '
    result+='FROM Headers INNER JOIN Density ON Headers.Key = Density.HKey '
    result+='WHERE (((Headers.Key)='
    result+=str(key)
    result+=') AND ((Density.QuadratNum)>0) and  (Density.QuadratNum  Is Not Null)  ) '
    result+='ORDER BY Density.QuadratNum;'

    return(result)


QuadArea=1.0
TranWidth=1.0
ln30=log(30.)
CB=[0.99,0.95,0.90,0.75,.5]
pval=[.5]
for x in CB:pval+=[(1.-x)/2.,.5+x/2.]

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
                             
        
        

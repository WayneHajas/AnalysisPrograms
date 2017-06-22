#Functions to make queries specific to GSU.  There are corresponding units for other animals.
from numpy import log,exp
from numpy.random import normal

def QnumDepthCount(key):
    result= 'SELECT Density.QuadratNum as QuadNum, '
    result+='iif (Density.GageDepth is NULL,-100,(Density.GageDepth-Density.TideHgt) *0.3048)  as Depth, '
    result+='iif (Densities.CountTotal is NULL,   0,Densities.CountTotal) as CountTotal '
    result+='FROM Headers INNER JOIN Density ON Headers.Key = Density.HKey '
    result+='WHERE (((Headers.Key)='
    result+=str(key)
    result+=') AND ((Density.QuadratNum)>0)) '
    result+='ORDER BY Density.QuadratNum;'

    return(result)

def MeasInQuad(key,qnum):
    result ="SELECT  SF.Diameter as AnimalLength "
    result+="FROM Density INNER JOIN SF ON (Density.QuadratNum = SF.QuadratNum) "
    result+=" AND (Density.HKey = SF.HKey) "
    result+="WHERE (((Density.HKey)= "
    result+=str(key)
    result+=") AND ((Density.QuadratNum)= "
    result+=str(qnum)
    result+=") And (SF.Diameter Is Not Null) AND  "
    result+="((SF.Sp)='G' Or (SF.Sp)='' Or (SF.Sp) Is Null));"
    return(result)

def QuadWithMeas(key):
    result= 'Select Distinct SF.QuadratNum as QuadNum '
    result+='FROM Density INNER JOIN SF ON Density.HKey = SF.HKey '
    result+='WHERE (Density.HKey='
    result+=str(key)
    result+=') '
    result+='order by SF.QuadratNum;'
    return(result)

QuadArea=1.0
TranWidth=1.0
ln30=log(30.)
CB=[0.99,0.95,0.90,0.75,.5]
pval=[.5]
for x in CB:pval+=[(1.-x)/2.,.5+x/2.]

class AlloEqn:
    def __init__(self,mnlw30=2.41753,sdlnw30=0.129231,mnbeta=2.754085,sdbeta=0.00699,sigmawithin=0.122298):
        self.mnlw30=mnlw30
        self.sdlnw30=sdlnw30
        self.mnbeta=mnbeta
        self.sdbeta=sdbeta
        self.sigmawithin=sigmawithin
        return

    def DetermAE(self):
        if self.mnlw30==None: return(None)
        def f(L):
            lnresult=self.mnlw30+self.mnbeta*(log(L)-ln30)
            result=exp(lnresult)
            return(result)
        return(f)

    def AvgWgtDetermAE(self):
        if self.mnlw30==None: return(None)
        f1=self.DetermAE()
        def f2(L):
            result=f1(L)*exp(.5*float(self.sigmawithin)*float(self.sigmawithin))
            return(result)
        return(f2)

    def RndAE(self):
        if self.mnlw30==None: return(None)
        lw30=normal(self.mnlw30,self.sdlnw30)
        b=normal(self.mnbeta,self.sdbeta)
        def f(L):
            lnresult=lw30+b*(log(L)-ln30)
            result=exp(lnresult)
            return(result)
        return(f)

    def AvgWgtRndAE(self):
        if self.mnlw30==None: return(None)
        f1=self.RndAE()
        def f2(L):
            result=f1(L)*exp(.5*float(self.sigmawithin)*float(self.sigmawithin))
            return(result)
        return(f2)
                             
        
        

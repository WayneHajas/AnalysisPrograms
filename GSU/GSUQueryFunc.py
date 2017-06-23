'''
2016-01-20
Modify so that the standard intercept (based on a 1mm urchin) is used in the allometric equation.
Default parameter-values generated in D:\Analyses\20160129.GSU.CSAS.Allom

2015-11-20
Modified QuadWithMeas to require that quadrats specifically require gsu-measurments'''


#Functions to make queries specific to GSU.  There are corresponding units for other animals.
from numpy import log,exp
from numpy.random import normal

def QnumDepthCount(key):
    result= 'SELECT Density.QuadratNum as QuadNum, '
    result+='iif (Density.GageDepth is NULL,-100,(Density.GageDepth-Density.TideHgt) *0.3048)  as Depth, '
    result+='iif (Density.CountTotal is NULL,   0,Density.CountTotal) as CountTotal '
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
    result+=')and (Density.CountTotal>0) and (SF.QuadratNum is not Null) and '
    result+=" ((SF.Sp='G') Or (SF.Sp='') Or (SF.Sp Is Null)) "
    result+='order by SF.QuadratNum;'
    return(result)

QuadArea=1.0
TranWidth=1.0
CB=[0.99,0.95,0.90,0.75,.5]
pval=[.5]
for x in CB:pval+=[(1.-x)/2.,.5+x/2.]

class AlloEqn:
    def __init__(self,intcpt=-6.8664802585167077,sdintcpt=0.034723646241811214,mnbeta=2.7276732805478963,sdbeta=0.0088232364135380891,sigmawithin=0.15967472910118682):
        self.intcpt=intcpt
        self.sdintcpt=sdintcpt
        self.mnbeta=mnbeta
        self.sdbeta=sdbeta
        self.sigmawithin=sigmawithin
        return

    def DetermAE(self):
        if self.intcpt==None: return(None)
        def f(L):
            lnresult=self.intcpt+self.mnbeta*log(L)
            result=exp(lnresult)
            return(result)
        return(f)

    def AvgWgtDetermAE(self):
        if self.intcpt==None: return(None)
        f1=self.DetermAE()
        def f2(L):
            result=f1(L)*exp(.5*float(self.sigmawithin)*float(self.sigmawithin))
            return(result)
        return(f2)

    def RndAE(self):
        if self.intcpt==None: return(None)
        lw=normal(self.intcpt,self.sdintcpt)
        b=normal(self.mnbeta,self.sdbeta)
        def f(L):
            lnresult=lw+b*log(L)
            result=exp(lnresult)
            return(result)
        return(f)

    def AvgWgtRndAE(self):
        if self.intcpt==None: return(None)
        f1=self.RndAE()
        def f2(L):
            result=f1(L)*exp(.5*float(self.sigmawithin)*float(self.sigmawithin))
            return(result)
        return(f2)
                             
        
        

#Functions to make queries specific to GSU.  There are corresponding units for other animals.
from numpy import log,exp
from numpy.random import normal

def QnumDepthCount(key):
    result= 'SELECT Density.QuadratNum as QuadNum, '
    result+='iif (Density.ChartDepth is NULL,-100,Density.ChartDepth)as   Depth, '
    result+='iif (Density.CountTotal is NULL,   0,Density.CountTotal) as CountTotal '
    result+='FROM Headers INNER JOIN Density ON Headers.Key = Density.HKey '
    result+='WHERE (((Headers.Key)='
    result+=str(key)
    result+=') AND ((Density.QuadratNum)>0) and  (Density.QuadratNum  Is Not Null)  ) '
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
    result+="((SF.Sp)='R' Or (SF.Sp)='' Or (SF.Sp) Is Null));"
    return(result)

def QuadWithMeas(key):
    result= 'Select Distinct SF.QuadratNum as QuadNum '
    result+='FROM Density INNER JOIN SF ON Density.HKey = SF.HKey '
    result+='WHERE (Density.HKey='
    result+=str(key)
    result+=') and (Density.CountTotal>0) and (SF.QuadratNum is not Null) and '
    result+=" ((SF.Sp='R') Or (SF.Sp='') Or (SF.Sp Is Null)) "
    result+='order by SF.QuadratNum;'
    return(result)

QuadArea=1.0
TranWidth=1.0
ln30=log(30.)
CB=[0.99,0.95,0.90,0.75,.5]
pval=[.5]
for x in CB:pval+=[(1.-x)/2.,.5+x/2.]

class AlloEqn:
    def __init__(self,alpha=-6.51697106793219225,beta=2.6400052786127439,mngamma=0.0,sdgamma=0,sigmawithin=0.15343724699331349):
        '''These default values were used with the previous (C+++) version of RUAP.  We have gone
        back to these values for consistency sake.
        
           Estimated values are taken from a simple regression (log scales)        
	   Price Island 1996 data was not included.  Other 12 surveys were.
       
        At one time (April 2014), there was set of parameter values corresponding to a quadratic-allometric relationship.
        Estimated values were estimated from all 13 surveys (including Price Island 1999).  I am going to record the 
        quadratic-values here just in case we change back:
       	   alpha=-6.73097749272,
       	   beta=2.70155385016,
       	   mngamma=0.00868078256821,
       	   sdgamma=exp(-5.55493420318),
       	   sigmawithin=0.152802138481'''
       	   
        self.alpha=alpha
        self.beta=beta
        self.mngamma=mngamma
        self.sdgamma=sdgamma
        self.sigmawithin=sigmawithin
        return

    def DetermAE(self):
        if self.alpha==None: return(None)
        def f(L):
            lnresult=self.alpha+self.beta*log(L)+self.mngamma*log(L)*log(L)
            result=exp(lnresult)
            return(result)
        return(f)

    def AvgWgtDetermAE(self):
        if self.alpha==None: return(None)
        f1=self.DetermAE()
        def f2(L):
            result=f1(L)*exp(.5*float(self.sigmawithin)*float(self.sigmawithin))
            return(result)
        return(f2)

    def RndAE(self):
        if self.alpha==None: return(None)
        if self.sdgamma<=1.e-6:
            rgam=self.mngamma
        else:
          rgam=normal(self.mngamma,self.sdgamma)
        def f(L):
            lnresult=self.alpha+self.beta*log(L)+rgam*log(L)*log(L)
            result=exp(lnresult)
            return(result)
        return(f)

    def AvgWgtRndAE(self):
        if self.alpha==None: return(None)
        f1=self.RndAE()
        def f2(L):
            result=f1(L)*exp(.5*float(self.sigmawithin)*float(self.sigmawithin))
            return(result)
        return(f2)
                             
        
        

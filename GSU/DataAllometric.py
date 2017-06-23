'''
2016-01-29 
Converted parameterization of allometric equation.  No 30mm.  W=exp(alpha +beta*log(L))
'''


from numpy import ndarray,log,std,average,sqrt
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from ADO import adoBaseClass as OpenDB
from GSUQueryFunc import AlloEqn


class DataAllometric:
    def __init__(self,ODB,keys):
        '''DataAllometric(ODB,keys)
       ODB is an ADOB connection to a GSU biodatabase.
       keys is a list of key-values from the Header-list'''
        query=self.BuildQuery(keys)
        self.TD=[]
        self.W=[]
        if query!=None:
            ODB.execute(query)
            self.TD=ODB.GetVariable('Diameter')
            self.W=ODB.GetVariable('WetWgt')
        self.BuildAlloEqun()


    def BuildAlloEqun(self):
        #Do nothing if there is no data
        if (self.TD==[]) or (self.TD==None) or (self.W==[]) or (self.W==None) :
            self.Allo=AlloEqn(None,None,None,None,None)
            return
        x=list(map(lambda t:log(t),self.TD))
        y=list(map(lambda t:log(t), self.W))
        #Follow Draper and Smith page 25
        xbar=average(x)
        ybar=average(y)
        n=len(x)

        Sxx=sum(list(map(lambda s:(s-xbar)**2,x)))               
        Syy=sum(list(map(lambda t:(t-ybar)**2,y)))               
        Sxy=sum(list(map(lambda s,t:(s-xbar)*(t-ybar),x,y)))
        b1=Sxy/Sxx
        b0=ybar-b1*xbar
        eps=list(map(lambda s,t:t-b0-b1*s,x,y))
        sigmaW=std(eps,ddof=2)

        #page 34
        SDbeta=sigmaW/sqrt(Sxx)
        sumXsqr=sum(list(map(lambda t:t*t,x)))
        sdintcpt=sigmaW*sqrt(sumXsqr/float(n)/Sxx)
        self.Allo=AlloEqn(b0,sdintcpt,b1,SDbeta,sigmaW)
            


    def BuildQuery(self,keys):
        if keys==None:return(None)
        if keys==[]:return(None)
        if isinstance(keys,int):return(self.BuildQuery[keys])
        result ='SELECT Dissection.Diameter, Dissection.WetWgt '
        result+='FROM Dissection '
        result+='WHERE ( '
        result+='(Dissection.Diameter Is Not Null )'
        result+='and (Dissection.Diameter <>0 )'
        result+='and (Dissection.WetWgt Is Not Null )'
        result+='and (Dissection.WetWgt <>0 )'
        result+='and ('
        result+=   '(Dissection.HKey='+str(keys[0])+' )'
        for k in keys[1:]:
            result+=   'or (Dissection.HKey='+str(k)+' )'
        result+=    ')'#end of or's for keys
        result+=');'   #end of and's for where
        return(result)

def GetAllo(ODB,keys):
    DA=DataAllometric(ODB,keys)
    return (DA.Allo)

if __name__ == "__main__":


    databasepath='h:\SampleMDB\GreenUrchin_NoLink.mdb'
    ODB=OpenDB(databasepath)
    keys=[11736, 11737, 11738, 11739]

    test=DataAllometric(ODB,keys)
    print(test.BuildQuery(keys))
    print (test.Allo.mnlw30)
    print (test.Allo.sdintcpt)
    print (test.Allo.mnbeta)
    print (test.Allo.sdbeta)
    print (test.Allo.sigmawithin)
     

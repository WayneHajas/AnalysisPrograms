from numpy import ndarray,average
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from mquantiles import mquantiles
#from InterpProd import WCHinterp
from wchNorm import InvNorm,NormCDF
from mquantiles import mquantiles
from KeyValues import MinInt
import pdb

def BCA(determEst,probSample,JackSample,p=[.025,.975]):
   '''BCA(determEst,probSample)

   Supports bootstrap operations for the analysis programs.
   Implementation of bias-corrected-and-accelerated method of calculating confidence bounds.
   Taken from page 392 of Hollander and Wolfe

   determEst is just some deterministic estimate of value
   probSample is a sample of estimates corresponding to the bootstrap iterations
   '''
   #pdb.set_trace()
   if isinstance(determEst,dict):
       result={}
       for k in determEst.keys():
           #pdb.set_trace()
           dE=determEst[k]
           
           #Ignore iterations where there are no quadrats in depth range
           pS2=list(filter(lambda t:t!=None,probSample))
           try:
               pS=list(map(lambda x:x[k],pS2))
           except:
                print ('BCA 24,k,probSample\n',k,'\n')
                for i in range(len(probSample)):
                    print(i,probSample[i][k])
                pS=list(map(lambda x:x[k],probSample))
           
           if (JackSample==None) or (JackSample==[None]):
              js=None
           else:
              try:
                 js=list(map(lambda x:x[k],JackSample))
              except:
                  print('\nBCA 35')
                  print('k, len(JackSample),type(JackSample)',k, len(JackSample),type(JackSample))
                  print('JackSample',JackSample)
           
           try:
               result[k]=BCA(dE,pS,js,p=p)
           except:
                print ('\nBCA 42 , k',k)
                print ('dE',dE)
                print ('pS',pS)
                print ('js',js)
                print ('p',p)
                result[k]=BCA(dE,pS,js,p=p)
       return(result)
   if isinstance(determEst,(list,ndarray)):
       result=[]
       for k in range(len(determEst)):
           #pdb.set_trace()
           dE=determEst[k]
           pS=probSample[k]
           if JackSample==None:
              js=None
           else: 
              js=JackSample[k]
           result+=[BCA(dE,pS,js,p=p)]
       return(result)
   if  determEst==None:return(None)

   #Simple one-dimensional
   if (JackSample==None) and (isinstance(p,(list,ndarray))):return(list(map(lambda t:MinInt,p)))
   if (JackSample==None):return(MinInt)

   #Trivial case where there is no variability
   if all(map(lambda t:t==determEst,probSample)):
      return(list(map(lambda t:determEst,p)))

   try:
     B=len(probSample)
   except:
       print ('BCA 44, probSample\n',probSample)
   if determEst<=min(probSample):
      z0hat=InvNorm(1.-1./float(B))
   elif  determEst>=max(probSample):
      z0hat=InvNorm(1./float(B))
   else:
      z0hat=InvNorm(1.-average(list(map(lambda x:  x<determEst,probSample))))

   thetadothat=average(JackSample)
   if all(map(lambda t:t==thetadothat,JackSample)):
      ahat=0.
   else:
      try:
         ahat=(sum(list(map(lambda jk:(thetadothat-jk)**3,JackSample))))/6.\
               /( (sum(list(map(lambda jk:(thetadothat-jk)**2,JackSample))))**(1.5))
      except:
         print('BCA 72')
         print('thetadothat',thetadothat)
         print('JackSample',JackSample)
         ahat=(sum(list(map(lambda jk:(thetadothat-jk)**3,JackSample))))/6.\
            /((sum(list(map(lambda jk:(thetadothat-jk)**2,JackSample))))**(1.5))
               
   try:
       z=CorrectedZ(p,z0hat,ahat)
       corP=CorrectedP(z)
   except:
       print ('\nBCA 74')
       print ('p',p)
       print ('z0hat',z0hat)
       print ('ahat',ahat)
       print ('determEst,average(probSample)',determEst,average(probSample))
       print ('average(list(map(lambda x:  x<determEst,probSample)))',average(list(map(lambda x:  x<determEst,probSample))))
       z=CorrectedZ(p,z0hat,ahat)
       corP=CorrectedP(z)

   #mquantiles gives an ndarray
   try:
      aresult=mquantiles(probSample,prob=corP)
   except:
      print('\nBCA 101 p,z0hat,ahat,z,corP,probSample\n',p,z0hat,ahat,z,corP,'\n',probSample)
      aresult=mquantiles(probSample,prob=corP)
   if isinstance(p,float):return(aresult[0])
   return(list(aresult))
    
    


def CorrectedZ(p,z0hat,ahat):
    if isinstance(p,(list,ndarray)):
        return(list(map( lambda t:CorrectedZ(t,z0hat,ahat),p)))
    z=InvNorm(1.-p)
    result=(z0hat+(z0hat+z))/(1.-ahat*(z0hat+z))
    return(result)
def CorrectedP(z):
    if isinstance(z,(list,ndarray)):
        return(list(map( lambda t:CorrectedP(t),z)))
    result=NormCDF(z)
    return(result)

def BCA_CB(determEst,probSample,JackSample,CB):
   '''BCA_CB(etermEst,probSample,JackSample,CB)

   Very similar to BCA except that it takes confidence bounds instead of p-values.
   Implementation of bias-corrected-and-accelerated method of calculating confidence bounds.
   Taken from page 392 of Hollander and Wolfe

   determEst is just some deterministic estimate of value
   probSample is a sample of estimates corresponding to the bootstrap iterations
   JackSample is a list of jacknife values
   0<CB<1 the confidence level - or a list of confidence levels
   '''


   if isinstance(determEst,dict):
       result={}
       for k in determEst.keys():
           dE=determEst[k]
           pS=list(map(lambda x:x[k],probSample))

           if JackSample==None: #Probably a sample of one
              js=None
           else: 
              js=list(map(lambda x:x[k],JackSample))
           try:
               result[k]=BCA_CB(dE,pS,js,CB)
           except:
                print ('\nBCA 169 , k',k)
                print ('dE',dE)
                print ('pS',pS)
                print ('js',js)
                print ('p',p)
                result[k]=BCA(BCA_CB,pS,js,CB)
       return(result)
   if isinstance(determEst,(list,ndarray)):
       result=[]
       for k in range(len(determEst)):
           dE=determEst[k]
           pS=list(map(lambda x:x[k],probSample))
           js=list(map(lambda x:x[k],JackSample))
           result+=[BCA_CB(dE,pS,js,CB)]
       return(result)
   if  determEst==None:return(None)

   #determEst,probSample and JackSample are now known to be simple structures
   if isinstance(CB,float):
      p=[(1.-CB)/2.,.5*(1.+CB)]
      nCB=1
   else:
      nCB=len(CB)
      p=[]
      for cb in CB:
         p+=[(1.-cb)/2.,.5*(1.+cb)]
   try:
      q=BCA(determEst,probSample,JackSample,p=p)
   except:
      print('\nBCA line 178 p\n',p)
   if nCB==1:
      result=q
   else:
      result=list(map(lambda i: q[i*2:i*2+2]   ,range(nCB)))
   return(result)
         
def Naive(probSample,p=[.025,.975]):
   oldy=sorted(probSample)
   nsample=len(oldy)
   #oldx=list(map(lambda i: (float(i)+.5)/float(nsample),range(nsample)))
   result=mquantiles(oldy,p)
   return(result)

def Naive_CB(probSample,CB=[0.99,0.95,0.90,0.75,0.50]):
   if isinstance(CB,float):
      CB2=CB
      if CB>1:CB2=CB/100.
      p=[(1.-CB2)/2.,.5*(1.+CB2)]
      nCB=1
   
   else:
      nCB=len(CB)
      CB2=CB
      if max(CB)>1:
         CB2=list(map(lambda t:t/100,CB))
      p=[]
      for cb in CB2:
        p+=[(1.-cb)/2.,(1.+cb)/2.]
   q=Naive(probSample,p=p)
   if nCB==1:
      result=q
   else:
      result=list(map(lambda i: q[i*2:i*2+2]   ,range(nCB)))
   return(result)



if __name__ == "__main__":
    from numpy.random import choice,normal
    from numpy import average,std
    
    nboot=5
    n=5
    x1=list(range(-49, 50))
    x2=list(range( 51,150))
    x3=normal(size=len(x1))
    x4=list(range(251,350))
    x5=list(range(351,450))
    x6=list(range(451,550))
    x7=list(range(551,650))

    def MakeSample(x,nboot):
        n=len(x)
        sumx=sum(x)
        determEst=average(x)
        JackSample=list(map(lambda t:(sumx-t)/float(n-1),x))
        probSample=list(map(lambda t: average(choice(x,size=n,replace=True))  ,range(nboot)))
        return([determEst,probSample,JackSample])


    determEst1,probSample1,JackSample1=MakeSample(x1,nboot)
    determEst2,probSample2,JackSample2=MakeSample(x2,nboot)
    determEst3,probSample3,JackSample3=MakeSample(x3,nboot)
    determEst4,probSample4,JackSample4=MakeSample(x4,nboot)
    determEst5,probSample5,JackSample5=MakeSample(x5,nboot)
    determEst6,probSample6,JackSample6=MakeSample(x6,nboot)
    determEst7,probSample7,JackSample7=MakeSample(x7,nboot)
    

    determEsta=[determEst1,determEst2,determEst3]
    probSamplea=[probSample1,probSample2,probSample3]
    JackSamplea=[JackSample1,JackSample2,JackSample3]
    
    determEstb={'1':determEst1,'2':determEst2,'a':determEsta}
    probSampleb={'1':probSample1,'2':probSample2,'a':probSamplea}
    JackSampleb={'1':JackSample1,'2':JackSample2,'a':JackSamplea}
    
    p=[.025,0.5,.975]
    print('x1\n')
    print (BCA(determEst1,probSample1,JackSample1,p=p))
    print (BCA(determEst2,probSample2,JackSample2,p=p))
    print (BCA(determEst3,probSample3,JackSample3,p=p))
    print (BCA(determEsta,probSamplea,JackSamplea,p=p))
    print (average(x3),std(x3)/10*1.96)
    print (BCA(determEstb,probSampleb,JackSampleb,p=p))

    


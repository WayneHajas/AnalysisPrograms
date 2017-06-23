from numpy import ndarray
from numpy.random import beta

from datetime import datetime,timedelta

class SFMeas():
    def __init__(self,date,Nshow=None,Nduck=None):
        if isinstance(date,list):self.date=datetime(date[0],date[1],date[2])
        else:self.date=date
        self.Nshow=Nshow
        self.Nduck=Nduck

    def Add(self,datetime2):
        if self.date!=datetime2.date:
            print('\n SFMeas 13. Trying to add mismatched dates')
            print('self.date',self.date)
            print('datetime2.date',datetime2.date)
            dummy=1./0.
        self.Nshow+=datetime2.Nshow
        self.Nduck+=datetime2.Nduck

class SFQuad():
    def __init__(self,FirstData=None):
        self.SFMeas=[]
        self.append(FirstData)
        
    def append(self,newSFMeas):
        if newSFMeas==None:return
        if isinstance(newSFMeas,SFQuad):
            self.append(newSFMeas.SFdata)
            return
        if isinstance(newSFMeas,list):
            for x in newSFMeas:
                self.append(x)
            return
        
        if not(isinstance(newSFMeas,SFMeas)):
            print('\nSFMeas line 53\nNduckSFMeas is invalid\n',newSFMeas)

        for sfd in self.SFMeas:
            try:
                if newSFMeas.date==sfd.date:
                    sfd.Add(newSFMeas)
                    return
            except:
                print('\nSFMeas 61')
                print('type(newSFMeas)', type(newSFMeas))
                print('type(sfd)', type(sfd))
                print('type(newSFMeas.date)', type(newSFMeas.date))
                print('type(sfd.date)', type(sfd.date))
                if newSFMeas.date==sfd.date:
                    sfd.Add(sfd)
                    return
        # A new date
        self.SFMeas.append(newSFMeas)
        if len(self.SFMeas)==1:return
        if self.SFMeas[-1].date<self.SFMeas[-2].date:
            self.SFMeas.sort(key=lambda x:x.date)

    def CalcNumDuck(self):
        self.NumDuck=max(list(map(lambda x: x.Nduck     ,self.SFMeas)))

    def GetNumDuck(self,CalcNumDuck=True):
        if CalcNumDuck:
            self.CalcNumDuck()
            return(self.NumDuck)
        if not('NumDuck' in locals()):
            self.CalcNumDuck()
            return(self.NumDuck)
        return(self.NumDuck)


    def GetNumShow(self, date=None):
      if len(self.SFMeas)<1:return(None)
      if isinstance(date,list):
        #date is in form of three integers
        if (len(date)==3) and isinstance(date[0],int):
            date2=datetime(date[0],date[1],date[2])
            result=self.GetNumShow(date=date2)
            return(result)

        result=list(map( lambda d:self.GetNumShow(date=d)))
        return (result)

      #single date-value
      if date<=self.SFMeas[0].date:
            result=float(self.SFMeas[0].Nshow)
            return(result)
      if date>=self.SFMeas[-1].date:
            result=float(self.SFMeas[-1].Nshow)
            return(result)
    
      prevShow=self.SFMeas[0].Nshow
      prevDate=self.SFMeas[0].date
      for sfd in self.SFMeas[1:]:
        if date==sfd.date:
            nshow=sfd.Nshow
            result=float(sfd.Nshow)
            return(result)

        if sfd.date>date:
            y2=float(sfd.Nshow)
            y1=float(prevShow)
            x2=sfd.date
            x1=prevDate
            x=date
            y=float(y1)+(x-x1)/(x2-x1)*float(y2-y1)
            return(y)
        prevShow=sfd.Nshow
        prevDate=sfd.date
      return(None)



    def EstSF(self, date=None,CalcNumDuck=True):

        #Make sure the estimated number of ducks is defined
        if CalcNumDuck:self.GetNumDuck()
        if not('NumDuck' in locals()):self.CalcNumDuck()
        if self.NumDuck==0:return(1)

        NumShow=self.GetNumShow( date=date)
        if isinstance(NumShow,list):
            result=list(map(lambda x:x/self.NumDuck,NumShow))
        else:
            try:
                result=float(NumShow)/float(self.NumDuck)
            except:
                print('SFdate 121 ')
                print('NumShow',NumShow)
                print('self.NumDuck',self.NumDuck)
        return(result)

    def RandSF(self, date=None,CalcNumDuck=True,Randomize=True):

        #Make sure the estimated number of ducks is defined
        if CalcNumDuck:self.GetNumDuck()
        if not('NumDuck' in locals()):self.CalcNumDuck()

        NumShow=self.GetNumShow( date=date)
        NumDuck=self.GetNumDuck(CalcNumDuck,date=date,CalcNumDuck=CalcNumDuck)

        if not(Randomize):#Actually a deterministic estimate of show-factor
            return(float(NumDuck)/float(NumDuck))
        
        #Finally, a random show-factor value
        result=beta(NumShow+1,NumDuck-NumShow+1)
        return(result)
    def GetDailyFixed(self):#Corresponds to DailyFixed field in Results_Transect
        return('D')
class SFplot(SFQuad):
    def __init__(self,FirstQuad=None):
        self.quad=[]
        self.append(FirstQuad)
        

    def append(self,newSFQuad):
        if newSFQuad==None: return
        if isinstance(newSFQuad,list):
            for q in newSFQuad:self.append(q)
            return
        if isinstance(newSFQuad,SFQuad):
            self.quad.append(newSFQuad)
            return
        if isinstance(newSFQuad,newSFQuad):
            self.quad+=newSFQuad.quad
            return
        print('SFdate 147.  SFplot has failed')
        print('newSFQuad',newSFQuad)
            

    def CalcNumDuck(self):
        self.NumDuck=sum(list(map(lambda x: x.GetNumDuck()     ,self.quad)))

    def GetNumDuck(self,CalcNumDuck=True):
        if CalcNumDuck:
            self.CalcNumDuck()
            return(self.NumDuck)
        if not('NumDuck' in locals()):
            self.CalcNumDuck()
            return(self.NumDuck)
        return(self.NumDuck)


    def GetNumShow(self, date=None):
      if isinstance(date,list):
        #date is in form of three integers
        if (len(date)==3) and isinstance(date[0],int):
            date2=datetime(date[0],date[1],date[2])
            result=self.GetNumShow(date=date2)
            return(result)

        result=list(map( lambda d:self.GetNumShow(date=d),date))
        return (result)

      if date==None:
          drange=self.GetDateRange()
          nday=(drange[1]-drange[0]).days
          date2=list(map(lambda t:drange[0]+timedelta(days=t),range(nday+1)))
          return(self.GetNumShow(date=date2))
                         

      #single date-value
      result=sum(list(map(lambda sfq:sfq.GetNumShow(date=date),self.quad)))
      return(result)

    def GetDateRange(self):
        if len(self.quad)==0:return([None,None])
        try:            
            MinDate=min(list(map(lambda q:q.SFMeas[0 ].date,self.quad)))
            MaxDate=max(list(map(lambda q:q.SFMeas[-1].date,self.quad)))
        except:
            print('SFdate 211')
            MinDate=min(list(map(lambda q:q.SFMeas[0 ].date,self.quad)))
            MaxDate=max(list(map(lambda q:q.SFMeas[-1].date,self.quad)))
        return([MinDate,MaxDate])

    def EstSF(self, date=None,CalcNumDuck=True):

        #Make sure the estimated number of ducks is defined
        if CalcNumDuck:self.GetNumDuck()
        if not('NumDuck' in locals()):self.GetNumDuck()
        if self.NumDuck==0:return(1.)

        NumShow=self.GetNumShow( date=date)
        ND=self.NumDuck
        if isinstance(NumShow,list):
            result=list(map(lambda x:float(x)/float(ND),NumShow))
        else:
            result=float(NumShow)/float(ND)
        return(result)
    
    def CalcNumDuck(self):
        if len(self.quad)==0:
            self.NumDuck=0
            return
        self.NumDuck=sum(list(map(lambda q: q.GetNumDuck()   ,self.quad)))

    def GetNumDuck(self,CalcNumDuck=True):
        if CalcNumDuck:
            self.CalcNumDuck()
            return(self.NumDuck)
        if not('NumDuck' in locals()):
            self.CalcNumDuck()
            return(self.NumDuck)
        return(self.NumDuck)


    def RandSF(self, date=None,CalcNumDuck=True,rerandomize=True,deterministic=False):

        if not(rerandomize):
            if not('sf' in locals()):self.Randomize()# if self.sf dosen't exist, make it exist
            if date==None:return(self.sf)

            if isinstance(date,(list,ndarray)):
                if (len(date==3) and (isinstance(data[0],(int,float)))):#date has been given as three integers
                    date2=datetime(date[0],date[1],date[2])
                    return(self.RandSF(date=date2,CalcNumDuck=CalcNumDuck,rerandomize=False,deterministic=deterministic))

                return(list(map(lambda d: self.RandSF(date=d,CalcNumDuck=CalcNumDuck,rerandomize=False,deterministic=deterministic),   date)))
            else:
                #in case date is outside the data range
                if date<=self.sf[0 ][0]:return(self.sf[0 ][1])
                if date>=self.sf[-1][0]:return(self.sf[-1][1])

                #this is the 'normal' case      
                result=list(filter(lambda x:x[0]==date,self.sf))[0]
                return(result)

        else:
        
            self.Randomize(deterministic=False,CalcNumDuck=CalcNumDuck)
            result=self.RandSF(date=date,CalcNumDuck=False,rerandomize=False,deterministic=deterministic)
            return(result)

    def Randomize(self,deterministic=False,CalcNumDuck=True):
        '''SFplot.Randomize(deterministic=False,CalcNumDuck=True)
       Generate a random show-factor value for each date in the life of the show-factor plot
       If deterministic=True, then generate deterministic estimates.'''

        #Make sure the estimated number of ducks is defined
        if CalcNumDuck:self.GetNumDuck()
        if not('NumDuck' in locals()):self.GetNumDuck()
        if self.NumDuck==0:
            self.sf=[1]
            return
        drange=self.GetDateRange()
        nday=(drange[1]-drange[0]).days
        date2=list(map(lambda t:drange[0]+timedelta(days=t),range(nday+1)))

        if deterministic:
            self.sf=list(map( lambda d: [d,float(self.GetNumShow( date=d))/float(self.NumDuck)],  date2))
            return
        try:
            self.sf=list(map( lambda d: [d,beta(self.GetNumShow( date=d)+1,self.NumDuck-self.GetNumShow( date=d)+1)],  date2))
        except:
            print('SFdate 285')
            print( type(date2))
            print( len(date2))
            print(type(date2[0]))
            print((date2[0]))
                   
            for d in date2:
                print(d, \
                      self.GetNumShow( date=d)+1,\
                      self.NumDuck-self.GetNumShow( date=d)+1)#,\
                      #beta(self.GetNumShow( date=d)+1,self.NumDuck-self.GetNumShow( date=d)+1) )
                self.sf=list(map( lambda d: [d,beta(self.GetNumShow( date=d)+1,self.NumDuck-self.GetNumShow( date=d)+1)],  date2))
       

class multiSFplot(SFplot):
    def __init__(self,lSFplot):
        '''multiSFplot(lSFplot)
           * lSFplot is a list of SFplot's'''
        self.lSFplot=lSFplot
        if isinstance(lSFplot,SFplot):
            self.lSFplot=[lSFplot]
        self.CalcNumDuck()

    def GetDateRange(self):
        if len(self.lSFplot)==0:return([None,None])
        DateRange=list(map(lambda lsfp:lsfp.GetDateRange(),self.lSFplot))
        DateRange=list(filter(lambda x:x!=[None, None],DateRange))
        try:
            MinDate=min(list(map(lambda x:x[0],DateRange)))
            MaxDate=max(list(map(lambda x:x[1],DateRange)))
        except:
            print('\n SFdate 260')
            print('DateRange\n',DateRange)
            MinDate=min(list(map(lambda x:x[0],DateRange)))
            MaxDate=max(list(map(lambda x:x[1],DateRange)))
        return([MinDate,MaxDate])
            

    def CalcNumDuck(self):
        self.NumDuck=sum(list(map(lambda x: x.GetNumDuck(),self.lSFplot)))

    def GetNumShow(self, date=None):
        if date==None:
          drange=self.GetDateRange()
          nday=(drange[1]-drange[0]).days
          date2=list(map(lambda t:drange[0]+timedelta(days=t),range(nday+1)))
          return(self.GetNumShow(date=date2))

        if isinstance(date,(list,ndarray)):
            result=list(map(lambda d:self.GetNumShow( date=d),date))
            return(result)

        try:
            result=sum(list(map(lambda x: x.GetNumShow(date=date),self.lSFplot)))
        except:
            print('\n SFdate 262 multiSFplot.GetNumShow')
            print('len(self.lSFplot)',len(self.lSFplot) )
            print('date',date )
            for lsf in self.lSFplot:print(lsf.GetNumShow(date=date))
            result=sum(list(map(lambda lsf: lsf.GetNumShow(date=date),self.lSFplot)))
        return(result)
    
    def CalcNumDuckuck(self):
        if len(self.lSFplot)==0:
            self.NumDuck=0
            return
        self.NumDuck=sum(list(map(lambda q: q.GetNumDuck()   ,self.lSFplot)))
        return

    
if __name__ == "__main__":

    sfm11=SFMeas(datetime(2013,9,10),Nshow=11,Nduck=14)
    sfm12=SFMeas(datetime(2013,9,13),Nshow=12,Nduck=14)
    sfm13=SFMeas(datetime(2013,9,16),Nshow=13,Nduck=14)

    sfm21=SFMeas(datetime(2013,9,11),Nshow=18,Nduck=18)
    sfm22=SFMeas(datetime(2013,9,14),Nshow=17,Nduck=18)
    sfm23=SFMeas(datetime(2013,9,17),Nshow=16,Nduck=19)


    quad1=SFQuad(FirstData=[sfm11,sfm12])
    quad2=SFQuad()
    quad2.append([sfm23,sfm22])
    quad2.append(sfm21)    

    print('\n')
    for t in range(9,19):
        print(t,quad1.GetNumShow([2013,9,t]))

    
    
    plot1=SFplot(FirstQuad=[quad1,quad2])
    print('\nNumDuck',plot1.GetNumDuck)
                 
    print('\n')
    for t in range(9,19):
        print(t,plot1.GetNumShow([2013,9,t]))
                 
    print('\n')
    for t in range(9,19):
        print(t,plot1.EstSF([2013,9,t]))
              

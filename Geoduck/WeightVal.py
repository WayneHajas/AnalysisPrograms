from numpy import ndarray,average,std,sqrt
from numpy import iinfo,int16,average,array
MinInt=iinfo(int16).min

class WeightVal():
    def __init__(self,x):
        if not(isinstance(x,(list,ndarray))):
            print('WeightVal 6.  Did not get an array for the weight value')
            print(type(x))
        self.FilterValues(x)
        self.CalcStats()

    #filter the values before incorporating them 
    def FilterValues(self,x):
        x2=list(filter(lambda y:y!=None,x))
        self.W=list(filter(lambda y:y>0,x2))

    #Calculate Statistics
    def CalcStats(self):
        self.n=len(self.W)

        if self.n<1:
            self.EstMeanWeight=MinInt
        else:
            self.EstMeanWeight=average(self.W)

        if self.n<2:
            self.StDeviaWeight=MinInt
            self.StErrMeanWeig=MinInt
        else:
            self.StDeviaWeight=  std(self.W,ddof=1)
            self.StErrMeanWeig=self.StDeviaWeight/sqrt(self.n)

if __name__ == "__main__":

    x=[2.,3.,2,3,2.5]
    x=[2.,3.,2.,3.,2.5]
    wv=WeightVal(x)
    print('wv.n',wv.n)
    print('wv.EstMeanWeight',wv.EstMeanWeight)
    print(type())
    print('wv.StDeviaWeight',wv.StDeviaWeight)
    print('wv.StErrMeanWeig',wv.StErrMeanWeig)
        

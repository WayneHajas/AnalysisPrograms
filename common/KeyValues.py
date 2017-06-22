from numpy import iinfo,int16
MinInt=iinfo(int16).min

class KeyValues:
    def __init__(self,InitValue=MinInt):
        '''KeyValues(InitValue=MinIt)
        InitValue is first value to use in the table.
        MinInt =-32768 is the lowest possible 16 bit integer

        Primarily intended to manage keys in output-database'''
        
        self.CurValue=InitValue

    def GetValue(self,IncrementFirst=False):
        if IncrementFirst:self.Increment()
        return(self.CurValue)
    def Increment(self):
        self.CurValue+=1

if __name__ == "__main__":
    x=KeyValues()
    print('\n')
    print ('x.CurValue ',x.CurValue)
    print ('x.GetValue() ', x.GetValue())
    print ('x.GetValue() ', x.GetValue())
    print ('x.GetValue() ', x.GetValue())
    print ('x.GetValue(IncrementFirst=False) ', x.GetValue(IncrementFirst=False))
    print ('x.GetValue(IncrementFirst=True) ', x.GetValue(IncrementFirst=True))
    print ('x.GetValue(IncrementFirst=True) ', x.GetValue(IncrementFirst=True))
    print ('x.GetValue(IncrementFirst=True) ', x.GetValue(IncrementFirst=True))
    print ('x.GetValue(IncrementFirst=True) ', x.GetValue(IncrementFirst=True))
    print ('x.GetValue() ', x.GetValue())
    print ('x.GetValue() ', x.GetValue())
    print ('x.GetValue() ', x.GetValue())
    print ('x.Increment() ', x.Increment())

    print ('x.GetValue() ', x.GetValue())
    print ('x.GetValue() ', x.GetValue())
    print ('x.GetValue() ', x.GetValue())
    print ('x.Increment() ', x.Increment())


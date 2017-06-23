'''
2015-12-23
Add sum-function to add-up an arbitrary number of distributions
'''


from numpy import sqrt,average


def Add(samp0,samp1):

    n0=len(samp0)
    n1=len(samp1)

    n=max([n0,n1])
    nsqrt=int(sqrt(n))

    use0=ReduceSamp(samp0,nsqrt)
    use1=ReduceSamp(samp1,nsqrt)
    permut=[]
    for x0 in use0:
        try:
            permut+=[  x0+x1 for x1 in use1]  
        except:
            print('\n',x0)
            print('\n',x1)
            permut+=[  x0+x1 for x1 in use1]  
    result=ReduceSamp(permut,n)
    return(result)

def Summ(multisamp):
    if len(multisamp)==0:return(None)
    if len(multisamp)==1:return(multisamp)
    
    result=multisamp[0]
    for nextsamp in multisamp[1:]:
        result=Add(result,nextsamp)
    return(result)
    
        

def Divide(samp0,samp1):
    '''samp0/samp1'''

    n0=len(samp0)
    n1=len(samp1)

    n=max([n0,n1])
    nsqrt=int(sqrt(n))

    use0=ReduceSamp(samp0,nsqrt)
    use1=ReduceSamp(samp1,nsqrt)
    permut=[]
    for x0 in use0:permut+=list(map(lambda x1:x0/x1,use1))
    result=ReduceSamp(permut,n)
    return(result)
def DivideByAverage(samp0,samp1):
    '''samp0/avg(samp1)'''

    avg1=average(samp1) 
    result=list(map(lambda t:  t/avg1,samp0))
    result.sort()
    return(result)

def Multiply(samp0,samp1):
    '''samp0*samp1'''

    n0=len(samp0)
    n1=len(samp1)

    n=max([n0,n1])
    nsqrt=n
    if nsqrt>100:nsqrt=int(sqrt(n))

    use0=ReduceSamp(samp0,nsqrt)
    use1=ReduceSamp(samp1,nsqrt)
    permut=[]
    for x0 in use0:permut+=list(map(lambda x1:x0*x1,use1))
    result=ReduceSamp(permut,n)
    return(result)



def ReduceSamp(s,n):
    s2=s
    s2.sort()
    nsamp=len(s2)
    if(n>=nsamp):return(s2)

    i=list(map(lambda k:int((k+.5)*float(nsamp)/float(n)),range(n)))
    s3=list(map(lambda k:s2[k],i))
    return(s3)
if __name__ == "__main__":

  from numpy import average,var  
  n=1000
  samp0=list(range( 0,n))
  samp1=list(range(int(-1*n/4),int(n-1*n/4)))
  samp2=list(range(int(-2*n/4),int(n-2*n/4)))
  samp3=list(range(int(-3*n/4),int(n-3*n/4)))
  test=Summ([samp0,samp1])
  print('\n')
  print(average(samp0),average(test))
  print(var(samp0),var(test))



  test=Summ([samp0,samp1,samp2,samp3])
  print('\n')
  print(average(samp0),average(samp1),average(samp2),average(samp3),average(test))
  print(var(samp0),var(samp1),var(samp2),var(samp3),var(test))

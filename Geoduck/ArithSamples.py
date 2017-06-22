from numpy import sqrt

import pdb

def Add(samp0,samp1):

    n0=len(samp0)
    n1=len(samp1)

    n=min([n0,n1])
    nsqrt=int(sqrt(n))

    use0=ReduceSamp(samp0,nsqrt)
    use1=ReduceSamp(samp1,nsqrt)
    permut=[]
    for x0 in use0:permut+=list(map(lambda x1:x0+x1,use1))
    result=ReduceSamp(permut,n)
    return(result)

def Divide(samp0,samp1):
    '''samp0/samp1'''

    n0=len(samp0)
    n1=len(samp1)

    n=min([n0,n1])
    nsqrt=int(sqrt(n))

    use0=ReduceSamp(samp0,nsqrt)
    use1=ReduceSamp(samp1,nsqrt)
    permut=[]
    for x0 in use0:permut+=list(map(lambda x1:x0/x1,use1))
    result=ReduceSamp(permut,n)
    return(result)

def Multiply(samp0,samp1):
    '''samp0*samp1'''

    n0=len(samp0)
    n1=len(samp1)

    n=min([n0,n1])
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
    if(n==nsamp):return(s2)

    i=list(map(lambda k:int((k+.5)*float(nsamp)/float(n)),range(n)))
    s3=list(map(lambda k:s2[k],i))
    return(s3)
if __name__ == "__main__":

  samp0=[1,2,3,4,5,6]
  samp1=[1,2,3,4,5,6]
  test=Multiply(samp0,samp1)
  print(test)

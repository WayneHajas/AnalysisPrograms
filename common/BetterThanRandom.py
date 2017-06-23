'''
A library to enable me to put elements of a list into a better-than-random order.

The result can be smaller than the original list.
The size of the new list is the square of a prime number - up to a maximum size of 1069*1069.

A 10000 member list will reduce to a 97*97=9409 member list

I call the order better-than-random because if I apply it to two different 
variables with two different offsets, then there is an even distribution of combinations
of high and low values of the two variables.

Should be very useful for stochastic arithmatic.

'''

from numpy import sqrt

def BetterThanRandom(x,offset=0):
    '''BetterThanRandom(x,offset=0)
    Put x in a contrived-random order
    0<=offset<=sqrn controls the structure of the result
    Results corresponding to two different values of offset will have zero correlation    
    '''
    y=sorted(x)
    index=MixInt2(len(y),offset=offset)
    result=[y[i] for i in index  ]
    return(result)

def MixInt2(n,offset=0):
    '''Generate indeces corresponding to the better-than-random order'''
    sqrn=LargestPrimeFactor(n)
    offset=int(n+offset)%sqrn

    result=[]
    for i in range(sqrn):
        t1= [    sqrn*((offset*i+j)%sqrn)    for j in range(-i-offset,sqrn-i-offset  ) ]
        t2= [         ((offset*i-j)%sqrn)    for j in range(-i+offset,sqrn-i+offset  ) ]
        t3=[ int((t1[j]+t2[j])*(n-1)/(sqrn*sqrn-1)) for j in range(sqrn) ]
        result+=t3
    return(result)
       
def LargestPrimeFactor(n):
    '''return the largest prime number less than sqrt(n)
    Largest possible result from this implementation is 1069'''
    sqrn=int(sqrt(n))   
    if sqrn>=1069:
        print('BetterThanRandom 41\nRan out of prime numbers.\nUsing 1069 because it is the biggest one I have.''')
        return(1069)
        
    #Prime numbers from https://primes.utm.edu/lists/small/1000.txt

    pn=[   2,     3 ,     5 ,     7  ,   11 ,    13 ,    17 ,    19 ,    23 ,    29 ,\
          31,     37,     41,     43 ,    47,     53,     59,     61,     67,     71,\
          73,     79,     83,     89 ,    97,    101,    103,    107,    109,    113,\
         127,    131,    137,    139 ,   149,    151,    157,    163,    167,    173,\
         179,    181,    191,    193 ,   197,    199,    211,    223,    227,    229,\
        233,    239,    241,    251 ,   257,    263,    269,    271,    277,    281,\
        283,    293,    307,    311 ,   313,    317,    331,    337,    347,    349,\
        353,    359,    367,    373 ,   379,    383,    389,    397,    401,    409,\
        419,    421,    431,    433 ,   439,    443,    449,    457,    461,    463,\
        467,    479,    487,    491 ,   499,    503,    509,    521,    523,    541,\
        547,    557,    563,    569 ,   571,    577,    587,    593,    599,    601,\
        607,    613,    617,    619 ,   631,    641,    643,    647,    653,    659,\
        661,    673,    677,    683 ,   691,    701,    709,    719,    727,    733,\
        739,    743,    751,    757 ,   761,    769,    773,    787,    797,    809,\
        811,    821,    823,    827 ,   829,    839,    853,    857,    859,    863,\
        877,    881,    883,    887 ,   907,    911,    919,    929,    937,    941,\
        947,    953,    967,    971 ,   977,    983,    991,    997,   1009,   1013,\
       1019,   1021,   1031,   1033 ,  1039,   1049,   1051,   1061,   1063 \
    ]    
    pn.reverse()
    for t in pn:
        if sqrn>=t:
            return(t)

if __name__ == "__main__":
    offset=1
    n=10000
    
    from numpy.random import seed,normal
    t0= normal(size=n)   
    t1= normal(size=n)   
    t2= normal(size=n)   
    t3= normal(size=n)   
    t4= normal(size=n)   
    
    x0= MixInt2(n,offset=0)
    x1= MixInt2(n,offset=1)
    x2= MixInt2(n,offset=2)
    x3= MixInt2(n,offset=3)
    x4= MixInt2(n,offset=4)
    
    y0=BetterThanRandom(t0,offset=0)    
    y1=BetterThanRandom(t0,offset=1)    
    y2=BetterThanRandom(t0,offset=2)    
    y3=BetterThanRandom(t0,offset=3)    
    y4=BetterThanRandom(t0,offset=4)    
    
    LPF=LargestPrimeFactor(n)
    inc=int(n/LPF)
    

    
    from numpy import cov
    print(cov([x0,x1,x2,x3,x4]))
    import matplotlib.pyplot as plt

    plt.close()
    plt.plot(y0,y2, '*r')
    
#    for i in range(LPF+1):
#        plt.plot( [0,n], 2*[i*inc],       'b--'     )
#        plt.plot(        2*[i*inc], [0,n],'b--'     )
#    plt.xlim(-.05*n,1.05*n)
#    plt.ylim(-.05*n,1.05*n)
    plt.show()
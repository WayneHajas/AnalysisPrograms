'''I wasn't getting consistently repeatable results using scipy.stats.mstats.mquantiles.
Here is my own version of choice.'''


from numpy.random import sample,seed

def mquantiles(a, prob=[0.25, 0.5, 0.75]):
    x=sorted(a)
    UseSize=len(x)
    
    try:
        result=[ x[int(t*UseSize)]  for t in prob   ]
    except:
        print('\nwchmquantile 14')     
        print(min(prob),max(prob),UseSize)
        print( int(min(prob)*UseSize), int(max(prob)*UseSize)   )
        result=[ x[int(t*UseSize)]  for t in prob   ]
    return(result)
    
    
if __name__ == "__main__":
    
    seed(756)
    
    x=[0,1,2,9,8,7,4,5,6,3]
    print(mquantiles(x))
    print(mquantiles(x,prob=[.0001,1-.0001,0.0999,0.100001  ]))
    print(mquantiles(x,prob=[1-.0001, ]))
    
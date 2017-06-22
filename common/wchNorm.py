# These routines are necessary because cx_freeze had trouble with scipy.stats.norm.
#  By hand-coding the following to methods, I make it possile to freeze the applications.
from numpy import sign,sqrt,exp,abs,ndarray,inf,pi,log

def NormCDF(z):
    '''Taken from
    http://www.johndcook.com/cpp_phi.html'''
    if isinstance(z,(list,ndarray)):return(list(map(lambda w:NormCDF(w),z)))
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    try:
        s=sign(z)
        x = abs(z)/sqrt(2.0)
        t = 1.0/(1.0 + p*x)
        y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x)
        result=.5*(1+s*y)
        return(result)
    except:
        print('\nwchNorm 23')
        print('\z',z)
        s=sign(z)
        x = abs(z)/sqrt(2.0)
        t = 1.0/(1.0 + p*x)
        y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x)
        result=.5*(1+s*y)

def InvNorm(p):
    '''Taken fromhttp://home.online.no/~pjacklam/notes/invnorm/impl/lea/lea.c'''
    if isinstance(p,(list,ndarray)):return(list(map(lambda s:InvNorm(s),p)))


    if p>=1:return(inf)
    if p<=0:return(-inf)
    a=[-3.969683028665376e+01,  2.209460984245205e+02,  -2.759285104469687e+02,  1.383577518672690e+02,  -3.066479806614716e+01,  2.506628277459239e+00]
    b=[-5.447609879822406e+01,  1.615858368580409e+02,  -1.556989798598866e+02,  6.680131188771972e+01,  -1.328068155288572e+01]

    c=[ -7.784894002430293e-03, -3.223964580411365e-01,  -2.400758277161838e+00, -2.549732539343734e+00,   4.374664141464968e+00,  2.938163982698783e+00]
    d=[7.784695709041462e-03,  3.224671290700398e-01,   2.445134137142996e+00,  3.754408661907416e+00]

    q = min([p,1-p])
    if (q>0.02425):
        try:
            u = q-0.5
            t = u*u
            u = u*(((((a[0]*t+a[1])*t+a[2])*t+a[3])*t+a[4])*t+a[5])\
              /(((((b[0]*t+b[1])*t+b[2])*t+b[3])*t+b[4])*t+1)
        except:
            print('\nwchNorm 52, p',p)
            u = q-0.5
            t = u*u
            u = u*(((((a[0]*t+a[1])*t+a[2])*t+a[3])*t+a[4])*t+a[5])\
              /(((((b[0]*t+b[1])*t+b[2])*t+b[3])*t+b[4])*t+1)
    else:
      try:
          t = sqrt(-2*log(q))
          u = (((((c[0]*t+c[1])*t+c[2])*t+c[3])*t+c[4])*t+c[5])\
               /((((d[0]*t+d[1])*t+d[2])*t+d[3])*t+1)
      except:
          print('\nwchNorm 63, p',p)
          t = sqrt(-2*log(q))
          u = (((((c[0]*t+c[1])*t+c[2])*t+c[3])*t+c[4])*t+c[5])\
               /((((d[0]*t+d[1])*t+d[2])*t+d[3])*t+1)

    try:
        t = NormCDF(u)-q
        t = t*sqrt(2.*pi)*exp(u*u/2)  
        u = u-t/(1+u*t/2)
        if p<=0.5:return(-u)
        return(u)
    except:
        print('\nwchNorm 75, p,t,u',p,t,u)
        t = NormCDF(u)-q
        t = t*sqrt(2.*pi)*exp(u*u/2)  
        u = u-t/(1+u*t/2)
        if p<=0.5:return(-u)
        return(u)
     

    

if __name__ == "__main__":

    print('\n.025',InvNorm(.025))
    print('\n.500',InvNorm(.500))
    print('\n.975',InvNorm(.975))

    #print('\n-1.96',NormCDF(-1.96))
    #print('\n 1.96',NormCDF( 1.96))
    #print('\n 0.00',NormCDF( 0.00))

    #print('\n [-1.96. 0., 1.96,3.0]',NormCDF( [-1.96, 0., 1.96,3.0]))

  

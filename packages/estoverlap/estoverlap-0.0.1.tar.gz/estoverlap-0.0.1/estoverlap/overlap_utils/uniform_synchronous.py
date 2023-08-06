import numpy as np
import pandas as pd

import numpy.random as rd
import scipy.linalg as spl


def OverlapCalc(n,Ret):
    
    N_1=np.shape(Ret)[0]
    NSeries=np.shape(Ret)[1]
    N=N_1-n+1   
    ORet=np.zeros((N,NSeries)) 
    
    for cc in range(0,n):
        ORet[:,:]=ORet[:,:]+Ret[cc:N+cc,:]

    return ORet


def Estimate_SD(Novr,N_A,Ret_Window):

    # Novr is ignored -- included to match the function signature of the otheres...
    mu_1 = N_A*np.mean(Ret_Window[:,0])
    mu_2 = N_A*np.mean(Ret_Window[:,1])
    # ddof=1 divides by N-1

    var_1 = N_A*np.var(Ret_Window[:,0],ddof=1)
    var_2 = N_A*np.var(Ret_Window[:,1],ddof=1)

#    sigma_1 = np.sqrt(N_A)*np.std(Ret_Window[:,0],ddof=1)
#    sigma_2 = np.sqrt(N_A)*np.std(Ret_Window[:,1],ddof=1)
    sigma_1=np.sqrt(var_1) 
    sigma_2=np.sqrt(var_2) 

    cov=N_A*np.cov(Ret_Window[:,0],Ret_Window[:,1],ddof=1)[0,1]
    
#    corr = np.corrcoef(Ret_Window[:,0],Ret_Window[:,1],ddof=1)[0,1]
    corr=cov/sigma_1/sigma_2

    RET={}
    RET['mu_1']=mu_1
    RET['mu_2']=mu_2
    RET['var_1']=var_1
    RET['var_2']=var_2
    RET['sigma_1']=sigma_1
    RET['sigma_2']=sigma_2
    RET['cov']=cov
    RET['corr']=corr

    return RET

def Estimate_EW(Novr,N_A,Ret_Window):

    N_1=np.shape(Ret_Window)[0]
    N=N_1-Novr+1

    ORet=OverlapCalc(Novr,Ret_Window)
   
# deals with the cases where the overlap is too small for the closed form:    
    if( Novr <= N ):
        rhosum=N*Novr-(Novr*Novr-1)/3.0
    else:
        rho_toeplitz=np.maximum(0.0,1-np.linspace(0,N-1,N)/Novr) 
        rho=spl.toeplitz(rho_toeplitz)
        rhosum=np.sum(rho)

# testing
#    rhosum=N*Novr-(Novr*Novr-1)/3.0
#    rho_toeplitz=np.maximum(0.0,1-np.linspace(0,N-1,N)/Novr) 
#    rho=spl.toeplitz(rho_toeplitz)
#    rhosum_exact=np.sum(rho)
#    print(N,Novr,rhosum,rhosum_exact)    

    B_v = N*(N-1)/(N*N-rhosum)
   
    mu_1 = (N_A/Novr)*np.mean(ORet[:,0])
    mu_2 = (N_A/Novr)*np.mean(ORet[:,1])

    var_1 = (B_v*N_A/Novr)*np.var(ORet[:,0],ddof=1)
    var_2 = (B_v*N_A/Novr)*np.var(ORet[:,1],ddof=1)
    
    sigma_1=np.sqrt(var_1)
    sigma_2=np.sqrt(var_2)

#bias correction cancels top and bottom:
    cov = (B_v*N_A/Novr)*np.cov(ORet[:,0],ORet[:,1],ddof=1)[0,1]
    corr=cov/sigma_1/sigma_2

    RET={}
    RET['mu_1']=mu_1
    RET['mu_2']=mu_2
    RET['var_1']=var_1
    RET['var_2']=var_2
    RET['sigma_1']=sigma_1
    RET['sigma_2']=sigma_2
    RET['cov']=cov
    RET['corr']=corr

    return RET

def Estimate_MV(Novr,N_A,Ret_Window):

# currently this is set up to use a toeplitz representation of the corelation matrix,
# and toeplitz_solve which is fast enough (for my purposes) to not have to bother 
# caching anything.    
# from what I can tell the condition number isn't very large here so this should be fine.


    ORet=OverlapCalc(Novr,Ret_Window)

    NWindow=np.shape(ORet)[0]
    
#    rho = np.eye(NWindow)
#    for c1 in range(0,NWindow-1):
#        for c2 in range(c1+1,NWindow):
#            rho[c1,c2]=max(0,1-abs(c1-c2)/Novr)
#            rho[c2,c1]=rho[c1,c2]
# replace with toeplitz algebra:
    rho_toeplitz=np.maximum(0.0,1-np.linspace(0,NWindow-1,NWindow)/Novr) 
# looks like the condition number is never too large...
#    rho=spl.toeplitz(rho_toeplitz)
#    (egv,egvals)=np.linalg.eigh(rho)
#    cond_number=np.log10(np.max(egv)/np.min(egv))

#    cholcorr = np.linalg.cholesky( rho )
#    rho_inv = np.linalg.inv(rho)
#    rho_inve = np.sum(rho_inv,axis=0).T
#    rhoinvsum = np.sum(rho_inv)

#    rho_inve=np.linalg.solve(rho,np.ones(len(ORet[:,0])))
#    rhoinvsum = np.sum(rho_inve)
# replace with toeplitz algebra:
    rho_inve=spl.solve_toeplitz(rho_toeplitz,np.ones(len(ORet[:,0])))
    rhoinvsum = np.sum(rho_inve)

    
#    rhosum = np.sum(rho)
#    rhosum=NWindow*Novr-(Novr*Novr-1)/3.0
#    print(rhosum-NWindow*Novr+(Novr*Novr-1)/3.0)
#    Abias = NWindow*(NWindow-1)/(NWindow*NWindow-rhosum)
#    rhosqsum = np.sum(np.matmul(rho, rho) ) 
#    rhosqtrace = np.trace( np.matmul(rho, rho) )

#    rinvOR0=np.linalg.solve(rho,ORet[:,0])
#    rinvOR1=np.linalg.solve(rho,ORet[:,1])
# replace with toeplitz algebra:
    rinvOR0=spl.solve_toeplitz(rho_toeplitz,ORet[:,0])
    rinvOR1=spl.solve_toeplitz(rho_toeplitz,ORet[:,1])
    
#    rhoinveZ1= np.matmul(rho_inve.T, ORet[:,0])
#    rhoinveZ2= np.matmul(rho_inve.T, ORet[:,1] )
#    print(rhoinveZ1-np.sum(rinvOR0))
#    print(rhoinveZ2-np.sum(rinvOR1))
    rhoinveZ1= np.sum(rinvOR0)
    rhoinveZ2= np.sum(rinvOR1)

    mu_1 = (N_A/Novr)*rhoinveZ1/rhoinvsum
    mu_2 = (N_A/Novr)*rhoinveZ2/rhoinvsum
    
#    v1 = np.sqrt( ( np.matmul(ORet[:,0].T, np.matmul(rho_inv, ORet[:,0])) -rhoinveZ1*rhoinveZ1/rhoinvsum )/(NWindow-1) )
#    v2 = np.sqrt( ( np.matmul(ORet[:,1].T , np.matmul(rho_inv , ORet[:,1]))-rhoinveZ2*rhoinveZ2/rhoinvsum )/(NWindow-1) )
#    corr = ( np.matmul(ORet[:,1].T , np.matmul(rho_inv , ORet[:,0])) -rhoinveZ1*rhoinveZ2/rhoinvsum )/(NWindow-1)
#    corr = corr/( v1 * v2 )

    var_1 = (N_A/Novr)*( np.matmul(ORet[:,0].T, rinvOR0) -rhoinveZ1*rhoinveZ1/rhoinvsum )/(NWindow-1)
    var_2 = (N_A/Novr)*( np.matmul(ORet[:,1].T , rinvOR1)-rhoinveZ2*rhoinveZ2/rhoinvsum )/(NWindow-1)

    sigma_1=np.sqrt(var_1)
    sigma_2=np.sqrt(var_2)

#    v1 = np.sqrt( ( np.matmul(ORet[:,0].T, rinvOR0) -rhoinveZ1*rhoinveZ1/rhoinvsum )/(NWindow-1) )
#    v2 = np.sqrt( ( np.matmul(ORet[:,1].T , rinvOR1)-rhoinveZ2*rhoinveZ2/rhoinvsum )/(NWindow-1) )

    cov = (N_A/Novr)*( np.matmul(ORet[:,1].T , rinvOR0) -rhoinveZ1*rhoinveZ2/rhoinvsum )/(NWindow-1)
    corr = cov/( sigma_1 * sigma_2 )
#    print(v1-v1a,v2-v2a,corr-corra)

    RET={}
    RET['mu_1']=mu_1
    RET['mu_2']=mu_2
    RET['var_1']=var_1
    RET['var_2']=var_2
    RET['sigma_1']=sigma_1
    RET['sigma_2']=sigma_2
    RET['cov']=cov
    RET['corr']=corr
    
    return RET



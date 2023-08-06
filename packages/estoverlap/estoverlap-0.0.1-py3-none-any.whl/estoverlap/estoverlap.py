import numpy as np
import pandas as pd

import numpy.random as rd
import scipy.linalg as spl

from estoverlap.overlap_utils.uniform_synchronous import Estimate_SD,Estimate_MV,Estimate_EW

def write_paths(seed,filename,N_paths,N_1,N_A,mu_1,mu_2,sigma_1,sigma_2,corr):
    
    rs = rd.RandomState(rd.MT19937(rd.SeedSequence(seed)))
    Ret = rs.normal(size=(N_paths,N_1,2))
    Ret[:,:,1]= corr * Ret[:,:,0]+np.sqrt(1-corr*corr)*Ret[:,:,1]

    Ret[:,:,0]=mu_1/N_A+sigma_1/np.sqrt(N_A)*Ret[:,:,0]
    Ret[:,:,1]=mu_2/N_A+sigma_2/np.sqrt(N_A)*Ret[:,:,1]
    
    Retp=pd.DataFrame(index=range(0,N_1))
    Retp['date'] = Retp.index
    
    for cc in range(0,N_paths):
        Retp[['Sim_'+str(cc)+'_1','Sim_'+str(cc)+'_2']]=Ret[cc,:,:]
    Retp=Retp.copy()
    
    Retp.to_csv(filename,index=False)
    
    return 



def Path_Analysis(ReturnsFilename,series,N_A,N_1,N_overlaps):

    Ret_raw=pd.read_csv(ReturnsFilename,delimiter=',')

    N_total=len(Ret_raw)
    
    # strip off the columns we don't want:
    Dates=Ret_raw.date
    Ret=Ret_raw[series].to_numpy()
    
    RES_List=[]
    for co in range(0,len(N_overlaps)):
        print(str(co+1)+'/'+str(len(N_overlaps)))
        n = N_overlaps[co]
                
    # this results in different number of results per overlap:
        NumWindows = N_total - N_1 - n
        
        for cw in range(0,NumWindows):
#            print(cw,NumWindows)
            RES={}
    
            N=N_1-n+1
            
            RES['N_1']=N_1
            RES['N']=N
            RES['n']=n
            RES['offset']=cw
            RES['date']=Dates.iloc[cw]
            
            Ret_Window=Ret[cw:cw+N_1,:]
    
            RET = Estimate_SD(1,N_A,Ret_Window)   
            for x in RET:
                RES['SD_'+x]=RET[x]
                                   
            RET = Estimate_EW(n,N_A,Ret_Window)
            for x in RET:
                RES['EW_'+x]=RET[x]
    
            RET = Estimate_MV(n,N_A,Ret_Window)
            for x in RET:
                RES['MV_'+x]=RET[x]
            
            RES_List.append(RES)
    
    RESULTS=pd.DataFrame(RES_List)

    return RESULTS


def Stats_Analysis(ReturnsFilename,N_paths,N_A,N_1,N_overlaps):

    Ret_raw=pd.read_csv(ReturnsFilename,delimiter=',')
        
    RES_List=[]
    for co in range(0,len(N_overlaps)):
        print(str(co+1)+'/'+str(len(N_overlaps)))
        n = N_overlaps[co]
            
        for cp in range(0,N_paths):

            series=['Sim_'+str(cp)+'_1','Sim_'+str(cp)+'_2']
            Ret_Window=Ret_raw[series].to_numpy()

            RES={}
    
            N=N_1-n+1
            
            RES['N_1']=N_1
            RES['N']=N
            RES['n']=n
            RES['path']=cp
            
            RET = Estimate_SD(1,N_A,Ret_Window)   
            for x in RET:
                RES['SD_'+x]=RET[x]
                                   
            RET = Estimate_EW(n,N_A,Ret_Window)
            for x in RET:
                RES['EW_'+x]=RET[x]
    
            RET = Estimate_MV(n,N_A,Ret_Window)
            for x in RET:
                RES['MV_'+x]=RET[x]
            
            RES_List.append(RES)
    
    RESULTS=pd.DataFrame(RES_List)
    

    return RESULTS

#!/usr/bin/env python
"""
Created on Thu Jan 16 14:59:52 2014

@author: Oren Freifeld
Email: freifeld@csail.mit.edu
"""

import numpy as np
from of.utils import ipshell
def create_cont_constraint_mat(H,v1s,v2s,v3s,v4s,nSides,nConstraints,nC,
                               dim_domain,dim_range,tess):    
    """
    L is the matrix that encodes the constraints of the consistent subspace.
    Its null space space is the sought-after consistent subspace
    (unless additional constraints are added; e.g., sub-algerba or bdry 
    conditions).
    """
    if dim_domain != 3:
        raise ValueError
    if dim_range not in [1,3]:
        raise ValueError
    nHomoCoo=dim_domain+1        
#    length_Avee = dim_domain*nHomoCoo
    length_Avee = dim_range*nHomoCoo
    L = np.zeros((nConstraints,nC*length_Avee))    
    # 
    if tess=='II':
        nPtsInSide = 4
    elif tess=='I':
        nPtsInSide = 3    
#    if nSides != nConstraints/(nPtsInSide*dim_domain):
#        raise ValueError(nSides,nConstraints)

    
    if nSides != nConstraints/(nPtsInSide*dim_range):
        print " print  nSides , nConstraints/(nPtsInSide*dim_range):"
        print  nSides , nConstraints/(nPtsInSide*dim_range)
        ipshell('stop')
        raise ValueError( nSides , (nConstraints,nPtsInSide,dim_range))

        
    if nSides != H.shape[0]:
        raise ValueError(nSides,H.shape)

    M = nPtsInSide*dim_range
    if dim_range == 1:
        for i in range(nSides):        
            v1 = v1s[i]
            v2 = v2s[i]
            v3 = v3s[i]
            if tess=='II':
                v4 = v4s[i]        
            h = H[i]
            a,b = h.nonzero()[0]  # idx for the relevant As   
            # s stands for start
            # e stands for end                            
            s1 = a*length_Avee 
            e1 = s1+nHomoCoo  
            s2 = b*length_Avee
            e2 = s2+nHomoCoo  
            
            # Constraint 1:              
            L[i*M,s1:e1]= v1                         
            L[i*M,s2:e2]= -v1                                  
            # Constraint 2:      
            # x component  
            L[i*M+1,s1:e1]= v2                         
            L[i*M+1,s2:e2]= -v2               
            # Constraint 3:                 
            L[i*M+2,s1:e1]= v3                         
            L[i*M+2,s2:e2]= -v3
            if tess=='II':
                # Constraint 4:                 
                L[i*M+3,s1:e1]= v4                         
                L[i*M+3,s2:e2]= -v4    
               
    elif dim_range==3:
        for i in range(nSides):        
            v1 = v1s[i]
            v2 = v2s[i]
            v3 = v3s[i]
            if tess=='II':
                v4 = v4s[i]   
            if np.allclose(v1,v2):
                raise ValueError(v1,v2)
            if np.allclose(v1,v3):
                raise ValueError(v1,v3)
            if np.allclose(v2,v3):
                raise ValueError(v2,v3)
            if tess=='II':
                if np.allclose(v1,v4):
                    raise ValueError(v1,v4)               
                if np.allclose(v2,v4):
                    raise ValueError(v2,v4)            
                if np.allclose(v3,v4):
                    raise ValueError(v3,v4)                
            
            
            h = H[i]
            a,b = h.nonzero()[0]  # idx for the relevant As   
            # s stands for start
            # e stands for end                            
            s1 = a*length_Avee 
            e1 = s1+nHomoCoo  
            s2 = b*length_Avee
            e2 = s2+nHomoCoo  
            
                                                           
            # Constraint 1: 
            row = np.zeros(L.shape[1])
            row[s1:e1]=v1
            row[s2:e2]=-v1            
            # x component  
            L[i*M]=row
            # y component       
            L[i*M+1]=np.roll(row,nHomoCoo)
            # z component       
            L[i*M+2]=np.roll(row,2*nHomoCoo)                        
            
            # Constraint 2: 
            row = np.zeros(L.shape[1])
            row[s1:e1]=v2
            row[s2:e2]=-v2   
            # x component  
            L[i*M+3]=row
            # y component       
            L[i*M+4]=np.roll(row,nHomoCoo)
            # z component       
            L[i*M+5]=np.roll(row,nHomoCoo*2)     
            
            # Constraint 3: 
            row = np.zeros(L.shape[1])
            row[s1:e1]=v3
            row[s2:e2]=-v3             
            # x component  
            L[i*M+6]=row
            # y component       
            L[i*M+7]=np.roll(row,nHomoCoo)
            # z component       
            L[i*M+8]=np.roll(row,2*nHomoCoo)           
#            ipshell('qqq')
#            1/0
            
            if tess=='II':
                # Constraint 4:      
                row = np.zeros(L.shape[1])
                row[s1:e1]=v4
                row[s2:e2]=-v4              
                
                # x component  
                L[i*M+9]=row
                # y component       
                L[i*M+10]=np.roll(row,nHomoCoo)
                # z component       
                L[i*M+11]=np.roll(row,2*nHomoCoo)         
            
            
    else:
        raise ValueError(dim_range)

    
    return L

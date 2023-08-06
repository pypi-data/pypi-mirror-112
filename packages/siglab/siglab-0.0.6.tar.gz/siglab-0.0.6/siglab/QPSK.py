import math
import numpy as np
import matplotlib.pyplot as plt

def qpsk(res,cnt):
   
    m=2
    #reshaping_the_array
    array2d = np.reshape(res,(cnt,m))
    #print(len(array2d))

    a2dfinal = array2d.tolist()
    #print(len(a2dfinal))

    #Creating_a_Dictionary_of_QPSK_values
    b=1
    c=-1
    va00 = complex(c,c)
    va01 = complex(c,b)
    va10 = complex(b,c)
    va11 = complex(b,b)
    #qpskdict = {va00:[[0],[0]],va01:[[0],[1]],va10:[[1],[0]],va11:[[1],[1]]}
    #print(qpskdict)
    #print('\n')

#values_after_qpsk
    cmplx=[]
    for a in range(len(array2d)):
        if a2dfinal[a] ==[0,0]:
         cmplx.append(va00)
        elif a2dfinal[a] ==[0,1]:
            cmplx.append(va01)
        elif a2dfinal[a] ==[1,0]:
            cmplx.append(va10)
        elif a2dfinal[a] ==[1,1]: 
            cmplx.append(va11)             

    #print(len(cmplx))
    #print('\n')
    return cmplx
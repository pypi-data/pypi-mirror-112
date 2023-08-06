import math
import numpy as np
import matplotlib.pyplot as plt

def binary(res):
    #defining_parameter_m
    parameter =4
    m= int(math.log(parameter,2))
    #print("The value of m is: "+str(m)+"\n" )

    #converting_to_1d array
    K = 1
  
    array1d = []
    for idx in range(0, len(res), K):
      
    
        array1d.append(int(res[idx : idx + K]))
  
    #print("Converted number list : " + str(array1d)+"\n") 

    #checking_length_of_array
    len1d = len(array1d)
    if(len1d%2==0):
        finl = len1d
    else:
        array1d = np.append(array1d,[0])
        finl = len(array1d)

    cnt = int(finl/2)

    #print(str(cnt) +"\n")

    return array1d
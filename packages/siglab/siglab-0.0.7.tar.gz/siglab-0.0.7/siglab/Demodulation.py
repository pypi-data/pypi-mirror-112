import math
import numpy as np
from numpy.fft import fft
from numpy import sum,isrealobj,sqrt
from numpy.random import standard_normal
import matplotlib.pyplot as plt
from math import erfc
import numpy as np

b=1
c=-1
va00 = complex(c,c)
va01 = complex(c,b)
va10 = complex(b,c)
va11 = complex(b,b)
qpskdict = {va00:[[0],[0]],va01:[[0],[1]],va10:[[1],[0]],va11:[[1],[1]]}


def demodulation(s,cnt,finl,array1d):
     ber=[]
     EbN0dBs = np.arange(start=-30,stop =15, step = 0.2) 
     #BER_sim = np.zeros(len(EbN0dBs))
     for _,EbN0dB in enumerate(EbN0dBs):
        gamma = 10**(EbN0dB/10) #SNRs to linear scale
        P= sum(abs(s)**2)/len(s) #Actual power in the vector
        N0=P/gamma
  
  #CHANNEL
  #generating AWGN noise
        noise =  sqrt(N0/2)*(standard_normal(s.shape)+1j*standard_normal(s.shape))

        sigpnoise = s+noise #adding noise to signal
    
        #RECEIVER
        #fourier_transform
        #print("performing fft")
        #print('\n')
        NFFT=cnt
        pm = fft(sigpnoise,NFFT)
    
        #print(len(pm))
        #NFFT-point DFT  
        #X=fft(pm,NFFT) #compute DFT using FFT     
        #nVals=np.arange(start = 0,stop = NFFT)/NFFT #Normalized DFT Sample points
    

    #demodulation_of_qpsk
        #print("performing demod")
        #print('\n')
    
        templ = []
        demod = []
        for i in range(len(pm)):
            t1= pm[i]
            t2 = t1-va00
            a1 = abs(t2)
            templ.append(a1)
            t3 = t1 - va01 
            a2 = abs(t3)
            templ.append(a2)
            t4 = t1 - va10
            a3 = abs(t4)
            templ.append(a3)
            t5 = t1 - va11
            a4 = abs(t5)
            templ.append(a4)
            #print((templ))
            arrarnp = np.array(templ)
            sorted = arrarnp.argsort()
            #print(sorted)
            if sorted[0]==0:
                demod.append(va00)
            elif sorted[0]==1:
                demod.append(va01)
            elif sorted[0]==2:
                demod.append(va10)
            elif sorted[0]==3:
                demod.append(va11)
            templ.clear()
  
  
#values_after_qpsk_demod

        array2ddemod =[]
        for a in range(len(demod)):
            if demod[a] == va00:
                array2ddemod.append([0,0])
            elif demod[a] == va01:
                array2ddemod.append([0,1])
            elif demod[a] == va10:
                array2ddemod.append([1,0])
            elif demod[a] == va11: 
                array2ddemod.append([1,1])             


        #print(len(array2ddemod))
        lineardemodarr = np.array(array2ddemod)
        #print(len(lineardemodarr))
        arraysome = np.reshape(lineardemodarr,(1,finl))

        g = np.squeeze(arraysome)
        h = g.tolist()
  
  #Finding the bit error rate
        proper=0
  
        #test=[]
        for d in range(0,finl):
            if array1d[d] == 1 and h[d] == 1:
                proper+=1
      
            elif array1d[d] == 1 and h[d] == 0:
                continue
            elif array1d[d] == 0 and h[d] == 1:
                continue
            else:
                proper+=1
        #print("\n")
        berval = (finl-proper)/finl
  
        ber.append(berval)
    
     #print(ber)
     _, ax = plt.subplots(nrows=1,ncols = 1)
     ax.semilogy(EbN0dBs,ber)
     #xmax = math.ceil(EbN0dBs[len(EbN0dBs)])
     #xmin = math.floor(EbN0dBs[0])
     ax.set_xlim(EbN0dBs[0], EbN0dBs[-2])
     plt.xlabel("SNR in Db")
     plt.ylabel("BER")
     plt.title("Probability of BER for OFDM using QPSK modulation")
     ax.grid(True)
     plt.show()
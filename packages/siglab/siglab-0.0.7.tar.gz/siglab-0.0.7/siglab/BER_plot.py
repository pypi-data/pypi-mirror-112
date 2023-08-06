# import matplotlib.pyplot as plt
# import numpy as np

# EbN0d = np.arange(start=-30,stop =138, step = 1)
# EbN0dBs = EbN0d.tolist()
# def ber_plot(ber):
#     #print(ber)
    
#     _, ax = plt.subplots(nrows=1,ncols = 1)
#     ax.semilogy(EbN0dBs,ber)
#     plt.xlabel("SNR in Db")
#     plt.ylabel("BER")
#     plt.title("Probability of BER for OFDM using QPSK modulation")
#     ax.grid(True)
#     plt.show()
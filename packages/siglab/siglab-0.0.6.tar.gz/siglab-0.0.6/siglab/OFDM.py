import texttobin 

import binary_list
import QPSK 
import Modulation 
import Demodulation 

BER_fin=[]
bin = texttobin.convert()
bin_vals = binary_list.binary(bin)
org_len = (len(bin_vals))
mod_len = int((len(bin_vals)/2))

cmplx_vals = QPSK.qpsk(bin_vals,mod_len)
signal = Modulation.modulation(cmplx_vals)
Demodulation.demodulation(signal,mod_len,org_len,bin_vals)











 













from numpy.fft import ifft

#inverse_fourier_transform
def modulation(cmplx):
    #print('performing ifft')
    #print('\n')
    s = ifft(cmplx)
    #print(s)
    return s
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import scipy.optimize as optimize
import fitsio
from time import time as clock
from SuzPyUtils.norm import medsig
from psf_sim import *
from k2sc.cdpp import cdpp
from tqdm import tqdm

import matplotlib as mpl

mpl.style.use('seaborn-colorblind')

#To make sure we have always the same matplotlib settings
#(the ones in comments are the ipython notebook settings)

mpl.rcParams['figure.figsize']=(8.0,6.0)    #(6.0,4.0)
mpl.rcParams['font.size']=18               #10 
mpl.rcParams['savefig.dpi']= 200             #72 
mpl.rcParams['axes.labelsize'] = 16
mpl.rcParams['axes.labelsize'] = 16
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
colours = mpl.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams["font.family"] = "Times New Roman"


fname = '../EPIC_211309989_mast.fits' # point this path to your favourite K2SC light curve
lc = Table.read(fname)

x, y = lc['x'][150:1550], lc['y'][150:1550] # copy in the xy variations from real data 


ncad = np.size(x)

'''--------------------------------------------------
halo_sawtooth.py - does halo photometry work with 
sawtooth xy variations?
--------------------------------------------------'''

'''------------------------
Generate a toy light curve
------------------------'''

t = np.linspace(0,100,ncad)

amplitude = 1.

periods = np.linspace(0.25,10.,100)

sigs_raw = 1.*np.zeros_like(periods)
sigs_1 = 1.*np.zeros_like(periods)


for jj, period in enumerate(tqdm(periods,desc='periods')):
    # print('Doing period',period)

    # x, y = amplitude*np.sin(2*np.pi*t/period), amplitude*np.cos(2*np.pi*t/period) # smooth
    folded = t % period
    x, y = amplitude*(folded/folded.max()),amplitude*(0.5 + folded/folded.max()) # sharp

    f = 20*np.ones(ncad) + np.sin(t) # make this whatever function you like! 
    f[400:500] *= 0.9 # toy transit


    '''------------------------
    Define a PSF and aperture
    ------------------------'''

    width = 3.
    start = clock()

    nx, ny = 10, 10
    npix = nx*ny
    pixels = np.zeros((nx,ny))

    '''------------------------
    Simulate data
    ------------------------'''

    tpf = np.zeros((nx,ny,ncad))
    sensitivity = 1-0.1*np.random.rand(nx,ny)
    white = 0

    for j in range(ncad):
        tpf[:,:,j] = f[j]*gaussian_psf(pixels,x[j],y[j],width)*sensitivity + np.random.randn(nx,ny)*white

    pixelvectors = np.reshape(tpf,(nx*ny,ncad))

    '''------------------------
    Define objectives
    ------------------------'''


    def obj_1(weights):
        flux = np.dot(weights.T,pixelvectors)
        return diff_1(flux)/np.nanmedian(flux)

    def obj_2(weights):
    #     return np.dot(w.T,sigma_flux,w)
        flux = np.dot(weights.T,pixelvectors)
        return diff_2(flux)/np.nanmedian(flux)

    '''------------------------
    Reconstruct lightcurves
    ------------------------'''

    cons = ({'type': 'eq', 'fun': lambda z: z.sum() - 1.})
    bounds = (npix)*((0,1),)

    w_init = np.random.rand(npix)
    w_init /= np.sum(w_init)
    # w_init = np.ones(180)/180.

    tic = clock()
        
    res1 = optimize.minimize(obj_1, w_init, method='SLSQP', constraints=cons, bounds = bounds,
                            options={'disp': False})
    xbest_1 = res1['x']

    toc = clock()

    # print('Time taken for TV1:',(toc-tic))

    lc_opt_1 = np.dot(xbest_1.T,pixelvectors)

    raw_lc = np.sum(pixelvectors,axis=0)

    raw_lc /= np.nanmedian(raw_lc)
    lc_opt_1 /= np.nanmedian(lc_opt_1)

    ssr = cdpp(t,raw_lc-f/np.nanmedian(f)+1)
    ss1 = cdpp(t,lc_opt_1-f/np.nanmedian(f)+1)

    sigs_raw[jj] = ssr
    sigs_1[jj] = ss1


finish = clock()
print('Done')
print('Time elapsed:',finish-start)

plt.figure(0)
plt.clf()

plt.plot(periods,sigs_raw,'.-',label='Raw')
plt.plot(periods,sigs_1,'.-',label='TV1')
plt.axvline(2*np.pi,color=colours[2],label='x,y frequency')
plt.ylabel('CDPP (ppm)')
plt.xlabel('Period (d)')
plt.yscale('log')
plt.title(r'TV Performance, $x =\sin(2\pi t/P)$')
plt.legend()
plt.savefig('sawtooth_sweep.png')
plt.show()


plt.figure(1)
plt.clf()

plt.plot(t,raw_lc,'.',label='Raw')
plt.plot(t,lc_opt_1,'.',label='TV1')
plt.plot(t,f/np.nanmedian(f),'-',label='True')
plt.ylabel('Time (d)')
plt.xlabel('Flux')
plt.title(r'%.1d Sawtooth: Light curves' % period)
plt.legend()
plt.savefig('sawtooth_%.0f_lc.png' % period)
plt.show()

plt.figure(2)
plt.clf()

plt.plot(t,raw_lc-f/np.nanmedian(f),'.',label='Raw')
plt.plot(t,lc_opt_1-f/np.nanmedian(f),'.',label='TV1')
plt.ylabel('Time (d)')
plt.xlabel('Flux')
plt.title(r'%.1d d Period: Residuals' % period)
plt.legend()
plt.savefig('sawtooth_%.0f_residuals.png' % period)
plt.show()

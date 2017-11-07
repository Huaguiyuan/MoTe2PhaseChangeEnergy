from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy import interpolate
import vaspinput
import sys
import os
rcParams.update({'font.size': 48, 'text.usetex': True})


def getEntropy(folders, T, charge):
    S2H = zeros([len(T),len(charge)])
    STp = zeros([len(T),len(charge)])
    
    basedir = os.getcwd()

    fold = '2H'
    j = 0
    for ch in charge:
        i = 0
        for temp in T:

            fldr = '%s/%s/ch%.2f/T%04.0f'%(basedir,fold,ch,temp)

            os.system("cd %s; cat OUTCAR | grep 'entropy T' | tail -1 | awk '{print $5}' > ts"%fldr)
            val  = genfromtxt(fldr + '/ts')
            S2H[i,j] = val
            #print(val)
            i += 1

        # Important: so far S contains T*S => need to divide by T
        S2H[:,j] = S2H[:,j] / T
        # Also, the value in OUTCAR is negative, so need to negate it here
        S2H[:,j] = - S2H[:,j]
        # Finally, since we have rectangular unit cell with 2 f.u., divide by 2 to get 1 f.u.
        S2H[:,j] = S2H[:,j] / 2
        j += 1

    fold = '1Tp'
    j = 0
    for ch in charge:
        i = 0
        for temp in T:

            fldr = '%s/%s/ch%.2f/T%04.0f'%(basedir,fold,ch,temp)

            os.system("cd %s; cat OUTCAR | grep 'entropy T' | tail -1 | awk '{print $5}' > ts"%fldr)
            val = genfromtxt(fldr + '/ts')
            STp[i,j] = val
            i += 1

        # Important: so far S contains T*S => need to divide by T
        STp[:,j] = STp[:,j] / T
        # Also, the value in OUTCAR is negative, so need to negate it here
        STp[:,j] = - STp[:,j]
        # Finally, since we have rectangular unit cell with 2 f.u., divide by 2 to get 1 f.u.
        STp[:,j] = STp[:,j] / 2
        j += 1

    return S2H, STp

if __name__ == '__main__':
    folders = ['2H', '1Tp']
    ismear = -1 # corresponds to Fermi smearing

    T = array([0,20,40,60,80,100,120,140,160,180,200,300,400,500,600,700,800,900,1000])
    charge = array([-0.05, -0.04, -0.03, -0.02, -0.01, 0.0,
                    0.01,   0.02,  0.03,  0.04,  0.05, 0.06,
                    0.07,   0.08,  0.09,  0.10])
    nfu = 2
    ne = 36
    TtoeV = 8.621738e-5
    smear = T*TtoeV
    nnodes = 8
    TtoeV = 8.621738e-5
    eV_to_meV = 1000

    if ("entropy2H.dat" in os.listdir('.') and "entropyTp.dat" in os.listdir('.')):
        S2H = genfromtxt("entropy2H.dat") # Loaded in eV/K/f.u.
        STp = genfromtxt("entropyTp.dat") # Loaded in eV/K/f.u.
    else:
        S2H, STp = getEntropy(folders,T, charge)
        S2H[isnan(S2H)] = 0.
        STp[isnan(STp)] = 0.
        savetxt("entropy2H.dat", S2H) # Save in eV/K/f.u.
        savetxt("entropyTp.dat", STp) # Save in eV/K/f.u.

    # Interpolation
    runinterpolation = False
    if runinterpolation:
        tck = interpolate.splrep(T, (STp[:,3] - S2H[:,3])*eV_to_meV, s=0)
        Tnew = linspace(0,1000, 1000)
        snew = interpolate.splev(Tnew, tck, der=0)
        
        figure()
        plot(T, (STp[:,3] - S2H[:,3])*eV_to_meV)
        plot(Tnew, snew)
        show()
        
        figure()
        plot(T, (STp[:,3]-S2H[:,3])*eV_to_meV)
        plot(T, (STp[:,5]-S2H[:,5])*eV_to_meV)
        plot(T, (STp[:,13]-S2H[:,13])*eV_to_meV)
        legend(["$\sigma=-0.03$","$\sigma=0$", "$\sigma = 0.08$"])
        xlabel("Temperature (K)")
        ylabel("$\Delta S^\mathrm{el}(T)$")
        title("Electronic entropy difference at different excess charge")
        show()

    TT, CH = meshgrid(charge, T)
        
    fig = figure(figsize=(22,15))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(TT, CH, S2H*eV_to_meV, cmap=cm.viridis, linewidth=0, antialiased=False)
    ax.set_ylim(-50,1050)
    ax.set_xlim(-0.05, 0.10)
    ax.set_zbound(0, 0.03)
    ax.set_xticks([-0.05, 0.0, 0.05, 0.10])
    ax.set_yticks([0,250,500,750,1000])
    ax.set_zticks([0, 0.01, 0.02, 0.03])
    ax.tick_params(axis='x', which='major', pad=5)
    ax.tick_params(axis='y', which='major', pad=10)
    ax.tick_params(axis='z', which='major', pad=25)
    ax.set_ylabel("$T$ (K)",labelpad=50)
    ax.set_xlabel("$\sigma$ ($e$/f.u.)",labelpad=40)
    ax.set_title("2H")
    cbr = fig.colorbar(surf, shrink=0.5, aspect=5,boundaries=linspace(0,0.025,1000))
    cbr.set_label("$S_\mathrm{2H}$ (meV/K/f.u.)",labelpad=20)
    cbr.set_ticks([0., 0.01, 0.02, 0.03])
    cbr.set_clim(0,0.025)
    savefig("sifig2a.png", dpi=300, bbox_inches="tight")

    
    fig = figure(figsize=(22,15))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(TT, CH, STp*eV_to_meV, cmap=cm.viridis, linewidth=0, antialiased=False)
    ax.set_ylim(-50,1050)
    ax.set_xlim(-0.05, 0.10)
    ax.set_zbound(0, 0.03)
    ax.set_xticks([-0.05, 0.0, 0.05, 0.10])
    ax.set_yticks([0,250,500,750,1000])
    ax.set_zticks([0, 0.01, 0.02, 0.03])
    ax.tick_params(axis='x', which='major', pad=5)
    ax.tick_params(axis='y', which='major', pad=10)
    ax.tick_params(axis='z', which='major', pad=25)
    ax.set_ylabel("$T$ (K)",labelpad=50)
    ax.set_xlabel("$\sigma$ ($e$/f.u.)",labelpad=40)
    ax.set_title("1T'")
    cbr = fig.colorbar(surf, shrink=0.5, aspect=5,boundaries=linspace(0,0.025,1000))
    cbr.set_label("$S_\mathrm{1T'}$ (meV/K/f.u.)",labelpad=20)
    cbr.set_ticks([0., 0.01, 0.02, 0.03])
    cbr.set_clim(0,0.025)
    savefig("sifig2b.png", dpi=300, bbox_inches="tight")


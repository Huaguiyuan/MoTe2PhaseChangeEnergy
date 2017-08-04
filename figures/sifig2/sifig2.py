from pylab import *
rcParams.update({'font.size': 48, 'text.usetex': True})

# Constants
mol   = 6.022e23
JtoeV = 1.602e-19
nfu   = 2*2*2                 # number of formula units
vfu2h = 0.3551*0.6149*0.698/2 # volume of 1 f.u. of 2H (in nm^3)

# 2H and 1T' phonopy data
thermal2h = genfromtxt('../../data/thermal_properties/phonon/2H/thermal.dat', skip_header=20,skip_footer=5)
thermal1t = genfromtxt('../../data/thermal_properties/phonon/1Tp/thermal.dat',skip_header=20,skip_footer=5)

# Electronic entropy of 1T' and 2H
selectrons = genfromtxt('../../data/thermal_properties/electron/entropy.dat', skip_header=1)
sel2h = selectrons[:,0]
sel1t = selectrons[:,1]

# Temperatures in K, entropy of 2H, 1T'
T  = thermal2h[:,0]
sh = thermal2h[:,2]
st = thermal1t[:,2]

dSel = sel1t - sel2h # already in meV/K/f.u.

dSph = st - sh      # J/K/mol
dSph /= (mol*JtoeV) # eV/K/unitcell
dSph /= 2*2*2       # eV/K/f.u.
dSph *= 1000        # meV/K/f.u.
dS = dSph + dSel

lws=6
f = figure(figsize=(15,12))
plot(T, dS,lw=lws)
plot(T, dSph,lw=lws)
plot(T, dSel,lw=lws)
legend(['$\Delta S_\mathrm{2H} + \Delta S_\mathrm{el}$',
        '$\Delta S_\mathrm{ph}$',
        '$\Delta S_\mathrm{el}$'],
       loc = 2, fontsize=32)
xlim(0,1050)
ylim(0,0.07)
xlabel('Temperature (K)')
ylabel('$\Delta S$ (meV/K/f.u.)')
savefig('sifig2.png', dpi=300, bbox_inches='tight')

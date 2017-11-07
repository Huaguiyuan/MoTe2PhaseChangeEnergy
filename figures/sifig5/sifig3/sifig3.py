from pylab import *
rcParams.update({'font.size': 48, 'text.usetex': True})

mol   = 6.022e23
JtoeV = 1.602e-19
nfu   = 2*2*2 # number of formula units
vfu2h = 0.3551*0.6149*0.698/2 # volume of 1 f.u. of 2H (in nm^3)

h = genfromtxt('../../data/thermal_properties/phonon/2H/thermal.dat', skip_header=20, skip_footer=5)

T = h[:,0]
ch = h[:,3]  # in J/K/mol
chJcm3 = ch*1e21/(vfu2h*mol*nfu) # 2H heat capacity in J/K/cm3

ch /= JtoeV # eV/K/mol
ch /= mol   # eV/K/unit cell
ch /= nfu   # eV/K/f.u.
ch *= 1000  # meV/K/f.u.

lws = 8
f = figure(figsize=(16,12))
plot(T, ch, 'orange', lw=lws)
xlim(0,1100)
ylim(0, 0.8)
xlabel('Temperature (K)')
ylabel('Specific heat (meV/K/f.u.)')
savefig('sifig3.png',dpi=300,bbox_inches='tight')

print("T=700 K heat capacit of 2H = %g meV/K/f.u."%ch[70])
print("T=700 K heat capacit of 2H = %g J/K/cm3"%chJcm3[70])

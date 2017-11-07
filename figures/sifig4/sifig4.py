from pylab import *
from scipy import interpolate
rcParams.update({'font.size': 48, 'text.usetex': True})

# Load TdS.dat, which is generated from fig4.py
#      TdS.dat: Temps in first column, dS in second column
TdS = genfromtxt('TdS.dat')

# Get index of maximum Temperature value
maxTind = TdS[:,0].argmax()

# Split T and dS into T<0 and T>0 components
Tneg = TdS[:maxTind,0]
dSneg = TdS[:maxTind,1]
Tpos = TdS[maxTind:,0]
dSpos = TdS[maxTind:,1]

# Get latent heat entropy
print("dS(300 K, Q<0) = %.4f"%dSneg[ (Tneg-300)>0][0])
print("dS(300 K, Q>0) = %.4f"%dSpos[ (Tpos-300)>0][-1])

# Remove non-unique values
Tpos, Tposind = unique(Tpos,return_index=True)
Tneg, Tnegind = unique(Tneg,return_index=True)

# Now "smooth" T and dS to remove kinks in dS
Tpos_sm = linspace(Tpos[0],Tpos[-1],100)
tck = interpolate.splrep(Tpos, dSpos[Tposind], s=0)
dSpos_sm = interpolate.splev(Tpos_sm, tck, der=0)

# Smooth for negative temperature values
Tneg_sm = linspace(Tneg[0],Tneg[-1],100)
tck = interpolate.splrep(Tneg, dSneg[Tnegind], s=0)
dSneg_sm = interpolate.splev(Tneg_sm, tck, der=0)

figure()
plot(Tneg_sm, dSneg_sm, lw=8)
plot(Tpos_sm, dSpos_sm, lw=8)
xlim(0,800)
ylim(0,0.06)
xlabel('$T$ (K)')
ylabel("$\Delta S$ (meV/K/f.u.)")
legend(["$Q<0$", "$Q>0$"],fontsize=36)
tick_params(direction='in', width=3, length=6, right='on', top='on')
savefig('sifig4.png', dpi=300, bbox_inches='tight')

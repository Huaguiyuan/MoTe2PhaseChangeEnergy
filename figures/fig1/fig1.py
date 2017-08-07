from pylab import *
rcParams.update({'font.size': 48, 'text.usetex': True})
rcParams['xtick.major.size'] = 6
rcParams['xtick.major.width'] = 3
rcParams['ytick.major.size'] = 6
rcParams['ytick.major.width'] = 3

VQ = genfromtxt('../../data/voltage-charge-diagram/Q_V.dat',skip_header=5)

sigma = VQ[:,0]
v2h   = VQ[:,1]
v1tp  = VQ[:,2]

p2hpos, v2hpos = polyfit(sigma[sigma>=0], v2h[sigma>=0], deg=1)
p2hneg, v2hneg = polyfit(sigma[sigma<0], v2h[sigma<0], deg=1)
vtp, ptp = polyfit(sigma, v1tp, deg=1)

print("Polynomial fitting results")
print("  V_{2H}(Q)  = %8g + %8g x sigma  (sigma >= 0)" %(v2hpos,p2hpos))
print("  V_{2H}(Q)  = %8g + %8g x sigma  (sigma < 0)" %(v2hneg,p2hneg))
print("  V_{1T'}(Q) = %8g + %8g x sigma  (all sigma)" %(vtp,ptp))

def findnearest(array,value):
    return abs(array-value).argmin()

# Transition voltages at 0K
# Vt1 = -1.6
# Vt2 = 4.4

# Transition voltages at 300K
Vt1 = -1.05
Vt2 = 3.23

sigmalower1=sigma[findnearest(v1tp,Vt1)]
sigmalower2=sigma[findnearest(v2h,Vt1)]
sigmaupper1=sigma[findnearest(v2h,Vt2)]
sigmaupper2=sigma[findnearest(v1tp,Vt2)]

intpos = trapz(  v2h[(sigma>=0) & (sigma < sigmaupper1)],
               sigma[(sigma>=0) & (sigma < sigmaupper1)])
intpos+= Vt2*(sigmaupper2-sigmaupper1)

intneg = trapz(  v2h[(sigma<=0) & (sigma > sigmalower2)],
               sigma[(sigma<=0) & (sigma > sigmalower2)])
intneg+= Vt1*(sigmalower2-sigmalower1)

print("T=300K electrostatic energy input:")
print("  \int V d\sigma (postive)  = %f meV/f.u."%(intpos*1000))
print("  \int V d\sigma (negative) = %f meV/f.u."%(intneg*1000))

al = 0.25
fs = 23

f = figure(figsize=(12,10))
plot(sigma, v2h, color='b',linewidth=5)
plot(sigma, v1tp, color='g',linewidth=5)
axhline(4.4,color='k',linestyle='--',linewidth=3)
axhline(-1.6,color='k',linestyle='--',linewidth=3)
axhline(Vt1,color='r',linestyle='--',linewidth=3)
axhline(Vt2,color='r',linestyle='--',linewidth=3)
axhline(0.,color='grey',linewidth=3)
fill_between(sigma, -3, 6, where=((sigma<=sigmalower1)),color='g',alpha=al)
fill_between(sigma, -3, 6, where=((sigma>=sigmalower1) & (sigma <= sigmalower2)),color='r',alpha=al)
fill_between(sigma, -3, 6, where=((sigma>=sigmalower2) & (sigma <= sigmaupper1)),color='b',alpha=al)
fill_between(sigma, -3, 6, where=((sigma>=sigmaupper1) & (sigma <= sigmaupper2)),color='r',alpha=al)
fill_between(sigma, -3, 6, where=((sigma>=sigmaupper2)),color='g',alpha=al)
# text(-0.062, 5.5,"1T'",fontsize=fs)
# text(-0.04,5.5,"Mixed",fontsize=fs)
# text(-0.013, 5.5,"2H",fontsize=fs)
text(-0.015, 4.5,r"$V_t^2(0 \mathrm{K}) = 4.4 \,\mathrm{V}$",fontsize=25) # y= 3.7
text(-0.015,-2.4,r"$V_t^1(0 \mathrm{K}) = -1.6 \,\mathrm{V}$",fontsize=25)
text(-0.015, 3.3,r"$V_t^2(300 \mathrm{K}) = 3.2 \,\mathrm{V}$",fontsize=25,color='r')
text(-0.015,-1.55,r"$V_t^1(300\mathrm{K}) = -1.0 \,\mathrm{V}$",fontsize=25,color='r')
xticks([-0.05,0,0.05,0.1])
legend(["2H", "1T'"],loc=5,fontsize=38)
xlim(-0.076, 0.126)
ylim(-3,6)
xlabel(r'$\sigma$ ($e$/f.u.)')
ylabel(r'$V$ (V)')
savefig('fig1b.png', dpi=300,bbox_inches='tight')

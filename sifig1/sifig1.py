from pylab import *
rcParams.update({'font.size': 48, 'text.usetex': True})

hdos = genfromtxt('2H/total_dos.dat',skip_header=1)
tdos = genfromtxt('1Tp/total_dos.dat',skip_header=1)

hdos[:,1] /= 2*2*2 # divide by number f.u. in a cell
tdos[:,1] /= 2*2*2 # divide by number f.u. in a cell

lws= 6
f = figure(figsize=(15,12))
plot(hdos[:,0],hdos[:,1], 'orange',lw=lws)
plot(tdos[:,0],tdos[:,1], 'g',lw=lws)
legend(['2H', "1T'"],loc=2,fontsize=38)
xlabel(r'$\omega$ (THz)')
ylabel(r'PDOS($\omega$) (states/THz/f.u.)')
xlim(0,9)
ylim(0,4)
savefig('sifig1.png',dpi=300,bbox_inches='tight')

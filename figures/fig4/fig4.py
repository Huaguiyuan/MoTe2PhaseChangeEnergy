from pylab import *
import scipy.constants as sc
rcParams.update({'font.size': 48, 'text.usetex': True})

global vol2H, vol1Tp, eV, mol

vol2H  = 0.3551*0.6149*0.698/2 # volume of one formula unit of 2H (in nm^3)
vol1Tp = 0.3551*0.6149*0.698/2 # volume of one formula unit of 2H (in nm^3)
eV = sc.physical_constants["electron volt"][0]
mol = sc.N_A

def getTotalEntropy(thermal2h, thermal1tp, elentropy):
    """
    Return values:
       T:  Nx1 array containing temperatures (in K)
       entropies: Nx2 array containing S_{2H}, S_{1T'} in (meV/K/f.u.)
    Note:
       S_{2H/1T'} = total entropy (S_{ph} + S_{el}) for both 2H, 1T'
    """

    nfu = 2*2*2 # Number of formula units in a supercell

    # Read files
    thermal_2h    = genfromtxt(thermal2h,  skip_header=20, skip_footer=5)
    thermal_1tp   = genfromtxt(thermal1tp, skip_header=20, skip_footer=5)
    el_entropy    = genfromtxt(elentropy,  skip_header=1)

    elentropy_2h  = el_entropy[:,0]
    elentropy_1tp = el_entropy[:,1]

    T = thermal_2h[:,0]

    # Run checks on data sizes
    if (size(thermal_1tp[:,0]) != size(T)):
        print("Error: 2H thermal data size does not match 1T' thermal data size")
        print("size(T)=%g size(thermal_1tp[:,0])=%g"%(size(T), size(thermal_1tp[:,0])))
        exit()
    elif (size(elentropy_2h) != size(T)):
        print("Error: 2H thermal data size does not match 2H electronic entropy data size")
    elif (size(elentropy_1tp) != size(T)):
        print("Error: 2H thermal data size does not match 1T' electronic entropy data size")

    # Fill entropies array with Phonon data (add electron data later)
    entropies = zeros([len(T),2])
    entropies[:,0] = thermal_2h[:,2]
    entropies[:,1] = thermal_1tp[:,2]

    # Unit conversion: thermal_2h and thermal_1tp entropies in   J/K/mol
    entropies[:,:] /= eV       # eV/K/mol
    entropies[:,:] /= mol      # eV/K/supercell
    entropies[:,:] /= nfu      # eV/K/f.u.
    entropies[:,:] *= 1000.     # meV/K/f.u.

    # Add in electronic entropy, which was already saved in meV/K/f.u.
    entropies[:,0] += elentropy_2h
    entropies[:,1] += elentropy_1tp

    return T, entropies


def integrate_dS(T,dS):
    """
    Return values:
        integral: array of $$ -\int_0^T \Delta S(T') dT'$$  in (eV/K/f.u.)
    Note:
        Each index in the array contains the value of the integral up to temperature T.
    """
    delS = dS/1000 # Convert to eV/K/f.u.

    integral = zeros(len(dS))

    for i in range(len(dS)):
        integral[i] = trapz(delS[:i], T[:i])

    return -integral


def integrate_dQ():
    """
    Return values:
        integral: array of $$\int \Delta Q dV$$
    """
    # Define voltage values
    V = linspace(-1.6,4.3889,10000)

    # Compute \Delta Q based on equation for V-Q diagram in fig1:
    sig2h =  sig2h = zeros(len(V))
    sig2h[V>0] = (V[V>0]-0.59)/38.8507
    sig2h[V<0] = (V[V<0]+0.36)/32.8307
    sigTp = (V - 0.4) / 36.8776
    dQ  = sigTp - sig2h

    # Compute integral \int \Delta Q dV
    integral = zeros(len(V))

    for i in range(len(V)):
        integral[i] = trapz(dQ[:i], V[:i], dx=(V[1]-V[0]))

    return V, dQ, integral

def computeTofV(intdS, intdQ, T, V):
    """
    Return values:
        TofV:
    """

    def find_nearest(array,value):
        return abs(array-value).argmin()

    # Create TofV for temp-voltage charge diagram
    TofV = zeros(len(V))
    for i in range(len(TofV)):
        j = find_nearest(intdS,intdQ[i])
        TofV[i] = T[j]

    print("V=0 transition temperature estimate %g K" %max(TofV))

    return TofV

def smoothTofV(T,V):
    """
    Return values:
       Treturn: array of temperatures as function of V
       Vreturn: array of voltage values
    Description:
       TofV has a step-like character, and this returns a 'smoothed' version of it.
    """
    # Temporary arrays, variables for storage
    Vnew = []
    Tnew = []
    count = 0
    currT = T[0]

    for i in range(len(T)):
        if abs(T[i]-currT) > 1e-3:
            Tnew.append(currT + (T[i]-currT)/2 )
            Vnew.append(V[i])
            currT = T[i]
            count = 0
        else:
            count += 1

    # Convert to numpy arrays
    Tnew = array(Tnew)
    Vnew = array(Vnew)

    # Now fix the V=0 point by adding in a value
    V0m1 = Vnew[Vnew<0][-1]
    V0m2 = Vnew[Vnew<0][-2]
    T0m1 = Tnew[Vnew<0][-1]
    T0m2 = Tnew[Vnew<0][-2]
    T0 =  T0m1 + abs(V0m1)*(T0m1-T0m2)/(V0m1-V0m2)
    print("V=0 transition temperature %g K" %T0)

    # Create final arrays to return
    Treturn = concatenate([array([0]), Tnew[Vnew<0] , array([T0]), Tnew[Vnew>0], array([0]) ])
    Vreturn = concatenate([array([V[0]]), Vnew[Vnew<0] , array([0.]), Vnew[Vnew>0], array([Vnew[-1]]) ])

    return Treturn, Vreturn

def print_Vt_T300K(Tnew, Vnew):
    """
    Computes the T=300 K transition voltage from the smoothed T-V diagram
    Does not return a value; just prints the values to the screen
    """
    Vt1 = Vnew[Vnew<0][Tnew[Vnew<0] <= 300][-1]
    Vt2 = Vnew[Vnew>0][Tnew[Vnew>0] <= 300][0]
    print("Transition Voltages:\n\tVt1(295K) = %8g\n\tVt2(295K) = %8g" %(Vt1,Vt2))


if __name__ == '__main__':
    plotSupFigs = False  # Option to plot supporting figures
    plotFigure4 = True   # Option to plot Figure 4
    
    thermal2h = '../../data/thermal_properties/phonon/2H/thermal.dat'
    thermaltp = '../../data/thermal_properties/phonon/1Tp/thermal.dat'
    elentropy = '../../data/thermal_properties/electron/entropy.dat'

    T, S = getTotalEntropy(thermal2h,thermaltp,elentropy)
    dS = S[:,1]-S[:,0]  # meV/K/f.u.

    T = linspace(0,1000,len(dS))
    intdS = integrate_dS(T,dS) # eV/f.u.

    V, dQ, intdQ = integrate_dQ()

    TofV = computeTofV(intdS, intdQ, T, V)
    Tnew, Vnew = smoothTofV(TofV,V)

    print_Vt_T300K(Tnew,Vnew)
    
    # Generate fill between data for green portion of graph
    V0=-1.6
    Vf=4.22538
    Vbefore = linspace(-4,V0,len(Vnew))
    Vafter  = linspace(Vf, 6,len(Vnew))
    bottom  = concatenate([Vbefore,Tnew, Vafter])
    top     = 1000*ones(len(bottom))
    x       = concatenate([Vbefore,Vnew,Vafter])

    # Create figure of T-V phase diagram
    if plotFigure4:
        lws=8
        f = figure()
        plot(Vnew,Tnew,linewidth=8)
        fill(Vnew,Tnew,color='b',alpha=0.25)
        fill_between(x,bottom,top,color='g', alpha=0.25)
        ylim(0,800)
        xlim(-3,5)
        xlabel('Voltage (V)')
        ylabel('Temperature (K)')
        text(1.6,340,'2H',fontsize=40)
        text(3.4,480,"1T'",fontsize=40)
        savefig('fig4.png',dpi=300,bbox_inches='tight')

    if plotSupFigs:
        figure()
        plot(T, intdS,lw=lws)
        xlim(0,1050)
        ylim(-0.05,0)
        xlabel('$T$ (K)')
        ylabel("$-\int \Delta S(T') dT'$ (eV/f.u.)")
        savefig('pics/intdS.png',dpi=200,bbox_inches='tight')

        figure()
        plot(V, dQ,lw=lws)
        axhline(0, color='grey', lw=1)
        xlabel('$V$ (V)')
        ylabel("$\Delta \sigma(V)$ (e/f.u.)")
        savefig('pics/dQ.png',dpi=200,bbox_inches='tight')

        figure();
        plot(V, intdQ);
        xlabel('$V$ (V)');
        ylabel("$\int \Delta \sigma(V') dV'$ (eV/f.u.)");
        savefig('pics/intdQ.png',dpi=200,bbox_inches='tight')
        
        f = figure()
        plot(V,TofV,linewidth=5)
        ylim(0,800)
        xlim(-3,5)
        xlabel('Voltage (V)')
        ylabel('Temperature (K)')
        savefig('pics/TofV.png',dpi=300,bbox_inches='tight')

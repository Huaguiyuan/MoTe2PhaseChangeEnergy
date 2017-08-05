eV = 1.602e-19
atto = 1e18 #(actually inverse atto)

# Volumes of 2H, 1T' in [nm3]
V2H  = 0.3551*0.6149*0.698/2
V1Tp = 0.3452*0.6368*0.698/2

V = 255.         # Define # pixels for 1 Volt
pt1sigma = 1187. # Define num pixels for 0.1 sigma
mol = 6.022e23

def electrostatic_forward():
    # old (T = 0K)
    # energy1  = (144./V) * 0.1*(1165./pt1sigma)
    # energy2  = 0.5* (1165./pt1sigma) * 0.1 *(972./V)
    # energy3  = 0.1*(135./pt1sigma) * 1120./V
    # energy = (energy1 + energy2 + energy3)*1000

    # New (T = 300K)
    energy = 192.574167

    print( "Electrostatic Energy input (forward bias, T=0K)")
    print( "    Vdq = %f [meV/f.u.]" %energy)

    # energy1 *= (eV*atto/V2H)
    # energy2 *= (eV*atto/V2H)
    # energy3 *= (eV*atto/V1Tp)
    # energy = energy1 + energy2 + energy3

    energy *= (eV*atto/V2H/1000)
    print( "        = %f [aJ/nm3]" %energy)
    print('')


def electrostatic_reverse():
    # old (T = 0K)
    # energy1 = (92/V) * (0.1*440/pt1sigma)
    # energy2 = 0.5* (0.1*440./pt1sigma) * (312./V)
    # energy3 = ((92.+312.)/V) * (0.1*206./pt1sigma)
    # energy = (energy1 + energy2 + energy3)*1000

    # New (T = 300K)
    energy = 38.338612 
    print( "Electrostatic Energy input (reverse bias, T=0K)")
    print( "    Vdq = %f [meV/f.u.]" %energy)
    # energy1 *= (eV*atto/V2H)
    # energy2 *= (eV*atto/V2H)
    # energy3 *= (eV*atto/V1Tp)
    # energy = energy1 + energy2 + energy3

    energy *= (eV*atto/V2H/1000)
    print( "        = %f [aJ/nm3]\n" %energy)

def latent_heat_T300():
    #-------------------------------------------------------------------
    #Thermal energy at room temperature
    #    (use average of 1T', 2H volume)
    #    (use T=0 to T=860K transition temperature)
    #-------------------------------------------------------------------
    # Thermal Energy for T=300 K

    Vol = (V2H + V1Tp) / 2.
    T = 300.
    dSph = 0.033               # meV/f.u.
    dSel = 0.0000055251        # eV/f.u.
    thermE_ph = T*dSph / 1000  # eV/ f.u.
    thermE_el = T*dSel
    thermE_tot = thermE_ph + thermE_el

    print( "Latent heat (T=300K)")
    print( "    TdS_ph = %f [meV/f.u.]" %(thermE_ph*1000))
    print( "           = %f [aJ/nm3]"   %(thermE_ph/Vol * eV * atto))
    print( "    TdS_el = %f [meV/f.u.]" %(thermE_el*1000))
    print( "           = %f [aJ/nm3]"   %(thermE_el/Vol * eV * atto))
    print( "    T(dS_ph + dS_el) = %f [meV/f.u.]" %((thermE_ph + thermE_el)*1000))
    print( "                     = %f [aJ/nm3]"   %((thermE_ph + thermE_el)/Vol * eV * atto))
    print()

def MoTe2_pure_thermal():
    #-------------------------------------------------------------------
    #Thermal energy for purely thermal transition T=300 to T=860K
    #    (use 2H volume for Cp)
    #-------------------------------------------------------------------
    Vol = (V2H + V1Tp) / 2.
    T = 860.
    dSph = 0.033                   # meV/f.u. 
    dSel = 0.000014705             #  eV/f.u.
    thermalE_ph = T*dSph/1000      #  eV/f.u.
    thermalE_el = T*dSel           #  eV/f.u.
    thermalE_tot = thermalE_ph + thermalE_el

    print( "Thermal energy input, T=300 to T=860K")
    print( "    TdS_ph = %f [meV/f.u.]" %(thermalE_ph*1000))
    print( "           = %f [aJ/nm3]\n" %(thermalE_ph/Vol * eV *atto))
    print( "    TdS_el = %f [meV/f.u.]" %(thermalE_el*1000))
    print( "           = %f [aJ/nm3]\n" %(thermalE_el/Vol * eV *atto))
    print( "    T(dS_ph + dS_el) = %f [meV/f.u.]" %( (thermalE_ph + thermalE_el)*1000 ))
    print( "                     = %f [aJ/nm3]"   %( (thermalE_ph + thermalE_el)/Vol * eV * atto ))
    print( )
    Cp = 0.00079  # Heat capacity meV/f.u./K  for MoTe2
    dT = (T-300)      # assume heating from T=300 to T=860 K


    print( "    (Side note: Cp for MoTe2 = %f [J/cm^3])"% (Cp/Vol *eV *atto *1e3))    
    Energy = Cp*dT + thermalE_tot
    print( "    Cp dT = %f [meV/f.u.]" %(Cp*dT*1000))
    print( "          = %f [aJ/nm3]\n" %(Cp*dT/Vol * eV *atto))
    print( "    Cp dT + TdS = %f [meV/f.u.]" %(Energy*1000))
    print( "                = %f [aJ/nm3]"   %(Energy/Vol * eV *atto))
    print()

def VO2_thermal():
    #-------------------------------------------------------------------
    #Thermal energy for purely thermal transition T=300 to T=340K 
    #    (VO2 has Cp = 15 cal / mol K,  L = 1020 cal / mol)
    #-------------------------------------------------------------------
    Cp = 15             # cal/mol K
    dT = 340.-300.      # K
    L = 1020            # cal/ mol
    V_vo2 = 29.4/1000   # nm3
    print( "VO2 thermal energy ")
    print( "    Cp    = %g [J/cm3]" %(Cp*4.184*1e21/(mol*V_vo2)))
    print( "    Cp*dT = %g [aJ/nm3]"%((Cp*dT)*4.184*1e18/(mol*V_vo2)))
    print( "    L     = %g [aJ/nm3]"%((L)*4.184*1e18/(mol*V_vo2)))
    print( "    Cp*dT + L = %g [meV/f.u.]" %((Cp*dT + L)*4.184/(mol*eV)*1000))
    print( "              = %g [aJ /nm3]"  %((Cp*dT + L)*4.184*1e18/(mol*V_vo2)))


def MoTe2_LatentHeat_Experimental():
    dH1 = 333  # cal/mol
    dH2 = 360  # cal/mol
    caltoJ = 4.184

    dH1 *= caltoJ  # J/mol
    dH1 /= mol     # J/f.u.
    dH1 /= V2H     # J/nm3
    dH1 *= 1e18    # aJ/nm3

    dH2 *= caltoJ  # J/mol
    dH2 /= mol     # J/f.u.
    dH2 /= V2H     # J/nm3
    dH2 *= 1e18    # aJ/nm3

    print("\nExperimental Latent Heat of MoTe2:")
    print("\tLatent Heat 1 (333 cal/mol) = %g aJ/nm3"%dH1)
    print("\tLatent Heat 2 (360 cal/mol) = %g aJ/nm3\n"%dH2)
    
    
if __name__=='__main__':

    electrostatic_forward()
    electrostatic_reverse()
    latent_heat_T300()
    MoTe2_LatentHeat_Experimental()
    MoTe2_pure_thermal()
    VO2_thermal()


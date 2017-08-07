import pylab

# Global constants
V2H  = 0.3551*0.6149*0.698/2 # Volume of 2H  in [nm3]
V1Tp = 0.3452*0.6368*0.698/2 # Volume of 1T' in [nm3]
eV   = 1.602e-19
atto = 1e18 #(actually inverse atto)
mol  = 6.022e23

def electrostatic_forward_T0():
    energy = 288.646619 # meV/K/f.u., computed using fig1
    print( "Electrostatic Energy input (forward bias, T=0K)")
    print( "    Vdq = %f [meV/f.u.]" %energy)
    energy *= (eV*atto/V2H/1000)
    print( "        = %f [aJ/nm3]\n" %energy)

def electrostatic_reverse_T0():
    energy = 62.211718 # meV/K/f.u., computed using fig1
    print( "Electrostatic Energy input (reverse bias, T=0K)")
    print( "    Vdq = %f [meV/f.u.]" %energy)
    energy *= (eV*atto/V2H/1000)
    print( "        = %f [aJ/nm3]\n" %energy)

def electrostatic_forward_T300():
    energy = 155.285 # meV/K/f.u., computed using fig1
    print( "Electrostatic Energy input (forward bias, T=300K)")
    print( "    Vdq = %f [meV/f.u.]" %energy)
    energy *= (eV*atto/V2H/1000)
    print( "        = %f [aJ/nm3]\n" %energy)

def electrostatic_reverse_T300():
    energy = 33.464 # meV/K/f.u., computed using fig1
    print( "Electrostatic Energy input (reverse bias, T=300K)")
    print( "    Vdq = %f [meV/f.u.]" %energy)
    energy *= (eV*atto/V2H/1000)
    print( "        = %f [aJ/nm3]\n" %energy)

def latent_heat_T300():
    #-------------------------------------------------------------------
    #Thermal energy at room temperature
    #    (use average of 1T', 2H volumes)
    #    dS is computed from SI figure 2
    #-------------------------------------------------------------------
    # Thermal Energy for T=300 K

    Vol = (V2H + V1Tp) / 2.
    T = 300.
    dSph = 0.043415         # meV/f.u.
    dSel = 0.00557          # meV/f.u.    
    thermE_ph = T*dSph/1000 #  eV/f.u.
    thermE_el = T*dSel/1000 #  eV/f.u.
    thermE_tot = thermE_ph + thermE_el
    
    print( "Latent heat (T=300K)")
    print( "    TdS_ph = %8f [meV/f.u.]" %(thermE_ph*1000))
    print( "           = %8f [aJ/nm3]"   %(thermE_ph/Vol * eV * atto))
    print( "    TdS_el = %8f [meV/f.u.]" %(thermE_el*1000))
    print( "           = %8f [aJ/nm3]"   %(thermE_el/Vol * eV * atto))
    print( "    T(dS_ph + dS_el) = %8f [meV/f.u.]" %(thermE_tot*1000))
    print( "                     = %8f [aJ/nm3]\n"   %(thermE_tot/Vol * eV * atto))

def MoTe2_pure_thermal():
    #-------------------------------------------------------------------
    #Thermal energy for purely thermal transition T=300 to T=690K
    #    (use 2H volume for Cp)
    #-------------------------------------------------------------------
    Vol = (V2H + V1Tp) / 2.
    T   = 690.
    dSph = 0.04605                           # meV/K/f.u. 
    dSel = 0.01176                           # meV/K/f.u.
    thermalE_ph = T*dSph/1000                #  eV/f.u.
    thermalE_el = T*dSel/1000                #  eV/f.u.
    thermalE_tot = thermalE_ph + thermalE_el #  eV/f.u.

    print( "Thermal energy input, T=300 to T=690K")
    print( "    TdS_ph = %8f [meV/f.u.]" %(thermalE_ph*1000))
    print( "           = %8f [aJ/nm3]\n" %(thermalE_ph/Vol * eV *atto))
    print( "    TdS_el = %8f [meV/f.u.]" %(thermalE_el*1000))
    print( "           = %8f [aJ/nm3]\n" %(thermalE_el/Vol * eV *atto))
    print( "    T(dS_ph + dS_el) = %8f [meV/f.u.]" %( (thermalE_ph + thermalE_el)*1000 ))
    print( "                     = %8f [aJ/nm3]\n" %( (thermalE_ph + thermalE_el)/Vol * eV * atto ))

    # Note: Cp is taken from SI Figure 3 at 700K
    Cp = 0.766889/1000  # Heat capacity eV/f.u./K for MoTe2 at T=700 K
    dT = (T-300)        # assume heating from T=300 to T = 690

    print( "\n    Cp for MoTe2 = %8f [J/cm^3]\n"% (Cp/Vol *eV *atto *1e3))    
    Energy = Cp*dT + thermalE_tot
    print( "    Cp dT = %8f [meV/f.u.]" %(Cp*dT*1000))
    print( "          = %8f [aJ/nm3]\n" %(Cp*dT/Vol * eV *atto))
    print( "    Cp dT + TdS = %8f [meV/f.u.]" %(Energy*1000))
    print( "                = %8f [aJ/nm3]\n" %(Energy/Vol * eV *atto))

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

def VO2_thermal():
    #-------------------------------------------------------------------
    #Thermal energy for purely thermal transition T=300 to T=340K 
    #    (VO2 has Cp = 15 cal / mol K,  L = 1020 cal / mol)
    #-------------------------------------------------------------------
    Cp = 15             # cal/mol K
    dT = 340.-300.      # K
    L = 1020            # cal/ mol
    V_vo2 = 29.4/1000   # nm3 - taken from Qiu, H. et al. New J. Phys. 17 (2015) 113016
    print( "VO2 thermal energy ")
    print( "    Cp    = %g [J/cm3]" %(Cp*4.184*1e21/(mol*V_vo2)))
    print( "    Cp*dT = %g [aJ/nm3]"%((Cp*dT)*4.184*1e18/(mol*V_vo2)))
    print( "    L     = %g [aJ/nm3]"%((L)*4.184*1e18/(mol*V_vo2)))
    print( "    Cp*dT + L = %g [meV/f.u.]" %((Cp*dT + L)*4.184/(mol*eV)*1000))
    print( "              = %g [aJ /nm3]"  %((Cp*dT + L)*4.184*1e18/(mol*V_vo2)))
    
def mote2banner():
    string = "======================================================================\n"
    string += "   MoTe2 \n"
    string += "======================================================================\n"
    print(string)

def vo2banner():
    string = "======================================================================\n"
    string += "   VO2 \n"
    string += "======================================================================\n"
    print(string)
    
if __name__=='__main__':

    mote2banner()
    electrostatic_forward_T0()
    electrostatic_reverse_T0()
    electrostatic_forward_T300()
    electrostatic_reverse_T300()
    latent_heat_T300()
    MoTe2_pure_thermal()
    MoTe2_LatentHeat_Experimental()
    vo2banner()
    VO2_thermal()

    

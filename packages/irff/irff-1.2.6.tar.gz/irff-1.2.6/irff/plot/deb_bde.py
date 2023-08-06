from ase.io.trajectory import TrajectoryWriter,Trajectory
from irff.AtomDance import AtomDance
from ase.calculators.singlepoint import SinglePointCalculator
from ase.io import read,write
from ase import units
from ase.visualize import view
from irff.irff_np import IRFF_NP
# from irff.tools import deb_energy
import matplotlib.pyplot as plt
from irff.AtomDance import AtomDance
import numpy as np


def plot(e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,Ehb,show=False):
    plt.figure(figsize=(15,12))    
    plt.subplot(3,3,1)   
    plt.plot(Eb,alpha=0.8,linestyle='-',color='b',label='Ebond')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,2)   
    plt.plot(Eo,alpha=0.8,linestyle='-',color='b',label='Eover')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,3)   
    plt.plot(Eu,alpha=0.8,linestyle='-',color='b',label='Eunder')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,4)   
    plt.plot(Ea,alpha=0.8,linestyle='-',color='b',label='Eang')
    plt.legend(loc='best',edgecolor='yellowgreen')
    
    plt.subplot(3,3,5)   
    plt.plot(El,alpha=0.8,linestyle='-',color='b',label='Elone')
    plt.legend(loc='best',edgecolor='yellowgreen')

    # plt.subplot(4,3,5)   
    # plt.plot(Et,alpha=0.8,linestyle='-',color='b',label='Etcon')
    # plt.legend(loc='best',edgecolor='yellowgreen')

    # plt.subplot(4,3,6)   
    # plt.plot(Ep,alpha=0.8,linestyle='-',color='b',label='Epen')
    # plt.legend(loc='best',edgecolor='yellowgreen')

    
    plt.subplot(3,3,6)   
    plt.plot(Et,alpha=0.8,linestyle='-',color='b',label='Etor')
    plt.legend(loc='best',edgecolor='yellowgreen')
    
    # plt.subplot(4,3,9)  
    # plt.plot(Ef,alpha=0.8,linestyle='-',color='b',label='Efcon')
    # plt.legend(loc='best',edgecolor='yellowgreen')
    
    Ebv = np.array(Ev) + np.array(Eb) + np.array(Eo) + np.array(Eu)
    plt.subplot(3,3,7)   
    plt.plot(Ehb,alpha=0.8,linestyle='-',color='b',label='Ehb')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,8)   
    plt.plot(Ev,alpha=0.8,linestyle='-',color='b',label='Evdw')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,9)   
    plt.plot(e,alpha=0.8,linestyle='-',color='b',label='Total Energy')
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('deb_energies.pdf')
    if show: plt.show()
    plt.close()


def deb_vdw(images,i=0,j=1,show=False):
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 nn=True)
    ir.calculate_Delta(images[0])

    Eb,Ea,e = [],[],[]
    Ehb,Eo,Ev,Eu,El = [],[],[],[],[]
    Etor,Ef,Ep,Et = [],[],[],[]

    for i_,atoms in enumerate(images):       
        ir.calculate(images[i_])
        # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )
        Eb.append(ir.Ebond)
        Ea.append(ir.Eang)
        Eo.append(ir.Eover)
        Ev.append(ir.Evdw)
        Eu.append(ir.Eunder)
        El.append(ir.Elone)
        Ep.append(ir.Epen)
        Et.append(ir.Etcon)
        Ef.append(ir.Efcon)
        Etor.append(ir.Etor)
        Ehb.append(ir.Ehb)
        e.append(ir.E)
        
    emin_ = np.min(Eb)
    eb    =  np.array(Eb) - emin_# )/emin_
    vmin_ =  np.min(Ev)
    ev    =  np.array(EV) - vmin_# )/emin_

    plt.figure(figsize=figsize)     
    # plt.plot(bopsi,alpha=0.8,linewidth=2,linestyle=':',color='k',label=r'$BO_p^{\sigma}$')
    # plt.plot(boppi,alpha=0.8,linewidth=2,linestyle='-.',color='k',label=r'$BO_p^{\pi}$')
    # plt.plot(boppp,alpha=0.8,linewidth=2,linestyle='--',color='k',label=r'$BO_p^{\pi\pi}$')
    # plt.plot(bo0,alpha=0.8,linewidth=2,linestyle='-',color='g',label=r'$BO^{t=0}$')
    
    plt.plot(ev,alpha=0.8,linewidth=2,linestyle='-',color='y',label=r'$E_{vdw}$')
    plt.plot(eb,alpha=0.8,linewidth=2,linestyle='-',color='r',label=r'$E_{bond}$')

    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('deb_bo.pdf')
    if show: plt.show()
    plt.close()
    return eb,ev


def deb_energy(images,debframe=[],i=6,j=8,show=False):
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 nn=True)
    ir.calculate_Delta(images[0])

    Eb,Ea,e = [],[],[]
    Ehb,Eo,Ev,Eu,El = [],[],[],[],[]
    Etor,Ef,Ep,Et = [],[],[],[]

    for i_,atoms in enumerate(images):       
        ir.calculate(images[i_])
        # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )
        Eb.append(ir.Ebond)
        Ea.append(ir.Eang)
        Eo.append(ir.Eover)
        Ev.append(ir.Evdw)
        Eu.append(ir.Eunder)
        El.append(ir.Elone)
        Ep.append(ir.Epen)
        Et.append(ir.Etcon)
        Ef.append(ir.Efcon)
        Etor.append(ir.Etor)
        Ehb.append(ir.Ehb)
        e.append(ir.E)
        
    plot(e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,Ehb,show=show)
    return e


def deb_bo(images,i=0,j=1,figsize=(16,10),print_=False,show=False):
    r,bopsi,boppi,boppp,bo0,bo1,eb,esi = [],[],[],[],[],[],[],[]
    
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 nn=True)
    ir.calculate_Delta(images[0])
    
    for i_,atoms in enumerate(images):       
        ir.calculate(atoms)
        
        bopsi.append(ir.eterm1[i][j])
        boppi.append(ir.eterm2[i][j])
        boppp.append(ir.eterm3[i][j])
        bo0.append(ir.bop[i][j])      
        bo1.append(ir.bo0[i][j])  
        eb.append(ir.ebond[i][j])   
        esi.append(ir.esi[i][j])
        r.append(ir.r[i][j]) 
        if print_:
           print('{:3d}  r: {:6.4f} bo: {:6.4f} Delta: {:6.4f} {:6.4f}'.format(i_,
                     ir.r[i][j],ir.bo0[i][j],ir.Delta[i],ir.Delta[j])) # self.thet0-self.theta
    emin_ = np.min(eb)
    eb = (emin_ - np.array(eb) )/emin_

    ems = np.min(esi)
    emx = np.max(esi)
    esi = (np.array(esi)-ems)/emx

    plt.figure(figsize=figsize)     
    plt.plot(r,bopsi,alpha=0.8,linewidth=2,linestyle=':',color='k',label=r'$BO_p^{\sigma}$')
    plt.plot(r,boppi,alpha=0.8,linewidth=2,linestyle='-.',color='k',label=r'$BO_p^{\pi}$')
    plt.plot(r,boppp,alpha=0.8,linewidth=2,linestyle='--',color='k',label=r'$BO_p^{\pi\pi}$')
    plt.plot(r,bo0,alpha=0.8,linewidth=2,linestyle='-',color='g',label=r'$BO^{t=0}$')
    plt.plot(r,bo1,alpha=0.8,linewidth=2,linestyle='-',color='y',label=r'$BO^{t=1}$')
    plt.plot(r,eb,alpha=0.8,linewidth=2,linestyle='-',color='r',label=r'$E_{bond}$ ($-E_{bond}/%4.2f$)' %-emin_)
    plt.plot(r,esi,alpha=0.8,linewidth=2,linestyle='-',color='indigo',label=r'$E_{esi}$ ($E_{si}/%4.2f$)' %emx)
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('deb_bo.pdf')
    if show: plt.show()
    plt.close()
    return r,eb


def deb_eang(images,ang=[0,1,2],figsize=(8,6),show=False,print_=False):
    i,j,k = ang
    ang_  = [k,j,i]
    a     = 0
    found = False
    eang,ecoa,epen = [],[],[]
    
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 nn=True)
    ir.calculate_Delta(images[0])
     
    for na,angle in enumerate(ir.angs):  
        i_,j_,k_ = angle
        if (i_==i and j_==j and k_==k) or (i_==k and j_==j and k_==i):
           a = na
           found = True
           
    if not found:
       print('Error: no angle found for',ang,angle)
    
    for i_,atoms in enumerate(images):       
        ir.calculate(atoms)

        eang.append(ir.Eang)    
        ecoa.append(ir.Etcon)
        epen.append(ir.Epen)
        if print_:
           # for a,angle in enumerate(ir.angs):  
           #i_,j_,k_ = angle
           print('{:3d}  {:6.4f}  {:6.4f} Dpi: {:6.4f} pbo: {:6.4f} N: {:6.4f} SBO3: {:6.4f}'.format(i_,
                     ir.thet0[a],ir.theta[a],ir.sbo[a],ir.pbo[a],
                     ir.nlp[j],ir.SBO3[a])) # self.thet0-self.theta
         
    plt.figure(figsize=figsize)     
    plt.plot(eang,alpha=0.8,linewidth=2,linestyle='-',color='r',label=r'$E_{ang}$')# ($-E_{ang}/{:4.2f}$)'.format(ang_m))
    # plt.plot(ecoa,alpha=0.8,linewidth=2,linestyle='-',color='indigo',label=r'$E_{coa}$') # ($E_{coa}/%4.2f$)' %emx)
    # plt.plot(epen,alpha=0.8,linewidth=2,linestyle='-',color='b',label=r'$E_{pen}$') # ($E_{pen}/%4.2f$)' %eox)
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('deb_ang.pdf')
    if show: plt.show()
    plt.close()


def get_theta(atoms,figsize=(8,6)):
    ir = IRFF_NP(atoms=atoms,
                 libfile='ffield.json',
                 nn=True)
    ir.calculate(atoms)
     
    for a,angle in enumerate(ir.angs):  
        i,j,k = angle
        print('{:3d} {:3d} {:3d} {:3d}  {:6.4f}  {:6.4f} Dpi: {:6.4f} SBO: {:6.4f} pbo: {:6.4f} SBO3: {:6.4f}'.format(a,
                     i,j,k,
                     ir.thet0[a],ir.theta[a],ir.sbo[a],ir.SBO[a],ir.pbo[a],
                     ir.SBO3[a])) # self.thet0-self.theta


def deb_eover(images,i=0,j=1,figsize=(16,10),show=False,print_=True):
    bopsi,boppi,boppp,bo0,bo1,eb = [],[],[],[],[],[]
    eo,eu,el,esi,r = [],[],[],[],[]
    eo_,eu_,eb_ = [],[],[]
    
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 nn=True)
    ir.calculate_Delta(images[0])
    
    for i_,atoms in enumerate(images):       
        ir.calculate(atoms)      
        bo0.append(ir.bop[i][j])      
        bo1.append(ir.bo0[i][j])  
        eb.append(ir.ebond[i][j])    
        eo.append(ir.Eover)      
        eu.append(ir.Eunder)
        r.append(ir.r[i][j])
        
        if print_:
           print('r: {:6.4f} bo: {:6.4f} eu: {:6.4f} ev: {:6.4f} eb: {:6.4f}'.format(ir.r[i][j],
                 ir.bo0[i][j],ir.Eunder,ir.Eover,ir.ebond[i][j]))
    
    ebx  = np.max(np.abs(eb))
    eb   = np.array(eb)/ebx+1.0
    
    eox  = np.max(np.abs(eo))
    if eox<0.0001:
       eox = 1.0
    eo   = np.array(eo)/eox + 1.0
    
    eux  = np.max(np.abs(eu))
    eu   = np.array(eu)/eux + 1.0
    
    plt.figure(figsize=figsize)     
    # plt.plot(r,bo0,alpha=0.8,linewidth=2,linestyle='-',color='g',label=r'$BO^{t=0}$')
    # plt.plot(r,bo1,alpha=0.8,linewidth=2,linestyle='-',color='y',label=r'$BO^{t=1}$')
    plt.plot(r,eb,alpha=0.8,linewidth=2,linestyle='-',color='r',label=r'$E_{bond}$')
    plt.plot(r,eo,alpha=0.8,linewidth=2,linestyle='-',color='indigo',label=r'$E_{over}$ ($E_{over}/%4.2f$)' %eox)
    plt.plot(r,eu,alpha=0.8,linewidth=2,linestyle='-',color='b',label=r'$E_{under}$ ($E_{under}/%4.2f$)' %eux)
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('deb_bo.pdf')
    if show: plt.show()
    plt.close()

## compare the total energy with DFT energy

# images = Trajectory('md.traj')
# E = []
# for atoms in images:
#     E.append(atoms.get_potential_energy())

# e = deb_energy(images)

# plt.figure()
# e_ = np.array(e) - np.min(e)
# E_ = np.array(E) - np.min(E)
# plt.plot(e_,alpha=0.8,linestyle='-',color='b',label='Total Energy')
# plt.plot(E_,alpha=0.8,linestyle='-',color='r',label='DFT Energy')
# plt.legend(loc='best',edgecolor='yellowgreen')
# plt.show()


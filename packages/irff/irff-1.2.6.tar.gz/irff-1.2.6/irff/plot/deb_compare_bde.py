#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
get_ipython().run_line_magic('matplotlib', 'inline')


# In[77]:


def plot(Eb1,Eb2,Eu1,Eu2,Eo1,Eo2,El1,El2,Ea1,Ea2,Et1,Et2,Ep1,Ep2,Etor1,Etor2,Ef1,Ef2,Ev1,Ev2,e1,e2):
    plt.figure(figsize=(15,15))    
    plt.subplot(3,3,1)   
    plt.plot(Eb1,alpha=0.8,linestyle='-',color='r',label='Ebond-1')
    plt.plot(Eb2,alpha=0.8,linestyle='-',color='b',label='Ebond-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,2)   
    plt.plot(Eo1,alpha=0.8,linestyle='-',color='r',label='Eover-1')
    plt.plot(Eo2,alpha=0.8,linestyle='-',color='b',label='Eover-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,3)   
    plt.plot(Eu1,alpha=0.8,linestyle='-',color='r',label='Eunder-1')
    plt.plot(Eu2,alpha=0.8,linestyle='-',color='b',label='Eunder-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,4)   
    plt.plot(Ea1,alpha=0.8,linestyle='-',color='r',label='Eang-1')
    plt.plot(Ea2,alpha=0.8,linestyle='-',color='b',label='Eang-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,5)   
    plt.plot(Et1,alpha=0.8,linestyle='-',color='r',label='Etcon-1')
    plt.plot(Et2,alpha=0.8,linestyle='-',color='b',label='Etcon-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,6)   
    plt.plot(Ep1,alpha=0.8,linestyle='-',color='r',label='Epen-1')
    plt.plot(Ep2,alpha=0.8,linestyle='-',color='b',label='Epen-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,7)   
    plt.plot(El1,alpha=0.8,linestyle='-',color='r',label='Elone-1')
    plt.plot(El2,alpha=0.8,linestyle='-',color='b',label='Elone-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,8)   
    plt.plot(Ev1,alpha=0.8,linestyle='-',color='r',label='Evdw-1')
    plt.plot(Ev2,alpha=0.8,linestyle='-',color='b',label='Evdw-2')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(3,3,9)   
    plt.plot(e1,alpha=0.8,linestyle='-',color='r',label='Total Energy-1')
    plt.plot(e2,alpha=0.8,linestyle='-',color='b',label='Total Energy-2')
    plt.legend(loc='best',edgecolor='yellowgreen')
    # plt.savefig('deb_energies.pdf')
    plt.show()

def deb_energy(images1,images2,debframe=[],i=0,j=1):
    ir1 = IRFF_NP(atoms=images1[0],
                 libfile='ffield.json',
                 nn=True)
    ir1.calculate_Delta(images1[0])

    ir2 = IRFF_NP(atoms=images2[0],
                 libfile='ffield.json',
                 nn=True)
    ir2.calculate_Delta(images2[0])

    Eb1,Eb2,Ea1,Ea2,e1,e2 = [],[],[],[],[],[]
    Eo1,Eo2,Ev1,Ev2 = [],[],[],[]
    Eu1,Eu2,El1,El2 = [],[],[],[]
    Ep1,Ep2,Et1,Et2 = [],[],[],[]
    Etor1,Etor2,Ef1,Ef2 = [],[],[],[]
    eo = []

    for i_,atoms in enumerate(images1):       
        ir1.calculate(images1[i_])
        ir2.calculate(images2[i_])
        # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )
        # Eb1.append(ir1.Ebond)
        # Eb2.append(ir2.Ebond)
        Eb1.append(ir1.ebond[i][j])
        Eb2.append(ir2.ebond[i][j])
        Ea1.append(ir1.Eang)
        Ea2.append(ir2.Eang)
        Eo1.append(ir1.Eover)
        Eo2.append(ir2.Eover)
        Ev1.append(ir1.Evdw)
        Ev2.append(ir2.Evdw)
        Eu1.append(ir1.Eunder)
        Eu2.append(ir2.Eunder)
        El1.append(ir1.Elone)
        El2.append(ir2.Elone)
        Ep1.append(ir1.Epen)
        Ep2.append(ir2.Epen)
        Et1.append(ir1.Etcon)
        Et2.append(ir2.Etcon)
        Ef1.append(ir1.Efcon)
        Ef2.append(ir2.Efcon)
        Etor1.append(ir1.Etor)
        Etor2.append(ir2.Etor)
        e1.append(ir1.E)
        e2.append(ir2.E)
        
        # print(ir1.r[i][j],ir1.ebond[i][j],ir2.r[i][j],ir2.ebond[i][j])
        
        if i_ in debframe:
           eo.append(ir1.eover)
        
        if i_ in debframe:
           for ia,a in enumerate(ir2.eang):
               # ia = 17
               print('{:3d} {:3d} {:3d} {:3d}  {:6.4f}  {:6.4f}  {:6.4f}'.format(ia,
                     ir2.angi[ia],ir2.angj[ia],ir2.angk[ia],ir2.etcon[ia],ir2.eang[ia],ir2.epen[ia]),
                     # '{:6.4f} {:6.4f} {:6.4f}'.format(ir2.f_7[ia],ir2.f_8[ia],ir2.expang[ia]),
                     # '{:6.4f} {:6.4f} {:6.4f} {:6.4f} {:6.4f}'.format(ir2.texp0[ia],ir2.texp1[ia],ir2.texp2[ia],
                     #                                                  ir2.texp3[ia],ir2.texp4[ia]),
                     )
#         if i_ in debframe:
#            for ia,a in enumerate(ir2.etor):
#                # ia = 17
#                print('{:3d} {:3d} {:3d} {:3d} {:3d}  {:6.4f} '.format(ia,
#                      ir2.tori[ia],ir2.torj[ia],ir2.tork[ia],ir2.torl[ia],ir2.etor[ia],
#                      #'{:6.4f} {:6.4f} {:6.4f}'.format(ir2.f_7[ia],ir2.f_8[ia],ir2.expang[ia]),　
#                      ))
#     for i in range(ir1.natom):
#         print(i,eo[0][i],eo[1][i])
    e1 = np.array(e1) - np.min(e1)
    e2 = np.array(e2) - np.min(e2)
    plot(Eb1,Eb2,Eu1,Eu2,Eo1,Eo2,El1,El2,Ea1,Ea2,Et1,Et2,Ep1,Ep2,Etor1,Etor2,Ef1,Ef2,Ev1,Ev2,e1,e2)


# In[61]:


i      = 6         # atom id
j      = 8         # atom id
st     = 1.1
ed     = 2.0

atoms  = read('hmx1-0.gen',index=0)
ad     = AtomDance(atoms=atoms,FirstAtom=9)
# images = ad.bond_momenta_bigest(atoms)
images1 = ad.stretch([i,j],nbin=30,rst=st,red=ed,scale=1.26,traj='md1.traj')
ad.close()
# view(images)


atoms  = read('hmx2-0.gen',index=0)
ad     = AtomDance(atoms=atoms,FirstAtom=9)
# images = ad.bond_momenta_bigest(atoms)
images2 = ad.stretch([i,j],nbin=30,rst=st,red=ed,scale=1.26,traj='md2.traj')
ad.close()


# The $ dE_{ang} $  is too big, we found it has a big 'val2' parameter.

# In[85]:


deb_energy(images1,images2,debframe=[13,14],i=6,j=8)


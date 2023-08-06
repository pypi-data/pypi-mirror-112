#!/usr/bin/env python
# coding: utf-8
from ase.io.trajectory import TrajectoryWriter,Trajectory
from irff.AtomDance import AtomDance
from ase.calculators.singlepoint import SinglePointCalculator
from ase.io import read,write
from ase import units
from ase.visualize import view
from irff.irff_np import IRFF_NP
import matplotlib.pyplot as plt
from irff.AtomDance import AtomDance
import numpy as np



def plot(e=None,e1=None,label='Bond Energy',label1='none',fig='bond_energy.pdf'):
    plt.figure()
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.plot(e,alpha=0.8,linestyle='-',color='r',label=label)
    if not e1 is None:
       plt.plot(e1,alpha=0.8,linestyle='-',color='b',label=label1)

    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig(fig,transparent=True) 
    plt.close() 


i = 6         # atom id
j = 8         # atom id


atoms  = read('hmx1-0.gen',index=0)
ad     = AtomDance(atoms=atoms,FirstAtom=9)
# images = ad.bond_momenta_bigest(atoms)
images1 = ad.stretch([i,j],nbin=30,rst=1.15,red=1.36,scale=1.26,traj='md1.traj')
ad.close()
# view(images)


atoms  = read('hmx2-0.gen',index=0)
ad     = AtomDance(atoms=atoms,FirstAtom=9)
# images = ad.bond_momenta_bigest(atoms)
images2 = ad.stretch([i,j],nbin=30,rst=1.15,red=1.36,scale=1.26,traj='md2.traj')
ad.close()

ir1 = IRFF_NP(atoms=images1[0],
             libfile='ffield.json',
             nn=True)
ir1.calculate_Delta(images1[0])

ir2 = IRFF_NP(atoms=images2[0],
             libfile='ffield.json',
             nn=True)
ir2.calculate_Delta(images2[0])


E1,E2,Ea1,Ea2,e = [],[],[],[],[]
Eo1,Eo2,Ev1,Ev2 = [],[],[],[]
Eu1,Eu2,El1,El2 = [],[],[],[]
Ep1,Ep2,Et1,Et2 = [],[],[],[]
Etor1,Etor2,Ef1,Ef2 = [],[],[],[]

for i_,atoms in enumerate(images1):       
    ir1.calculate(images1[i_])
    ir2.calculate(images2[i_])
    # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )
    E1.append(ir1.Ebond)
    E2.append(ir2.Ebond)
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
    e.append(ir1.ebond[i][j])
    
    # if i_==0: 
    #    for ia,a in enumerate(ir1.eang):
    #        # ia = 17
    #        print('{:3d} {:3d} {:3d} {:3d}  {:6.4f}  {:6.4f} '.format(ia,
    #              ir1.angi[ia],ir1.angj[ia],ir1.angk[ia],ir1.etcon[ia],ir1.eang[ia],
    #              #'{:6.4f} {:6.4f} {:6.4f}'.format(ir1.f_7[ia],ir1.f_8[ia],ir1.expang[ia]),　
    #              ))
    if i_==0:
       for ia,a in enumerate(ir2.eang):
           # ia = 17
           print('{:3d} {:3d} {:3d} {:3d}  {:6.4f}  {:6.4f} '.format(ia,
                 ir2.angi[ia],ir2.angj[ia],ir2.angk[ia],ir2.etcon[ia],ir2.eang[ia],
                 #'{:6.4f} {:6.4f} {:6.4f}'.format(ir2.f_7[ia],ir2.f_8[ia],ir2.expang[ia]),　
                 ))
    if i_ in [28,29]:
       for ia,a in enumerate(ir2.etor):
           # ia = 17
           print('{:3d} {:3d} {:3d} {:3d} {:3d}  {:6.4f} '.format(ia,
                 ir2.tori[ia],ir2.torj[ia],ir2.tork[ia],ir2.torl[ia],ir2.etor[ia],
                 #'{:6.4f} {:6.4f} {:6.4f}'.format(ir2.f_7[ia],ir2.f_8[ia],ir2.expang[ia]),　
                 ))

    print('%d Energies: ' %i_,
          '%12.4f ' %ir1.E,'%12.4f ' %ir2.E,
          'Ebd: %6.4f' %ir1.Ebond, ' %6.4f' %ir2.Ebond,
          'ebond: %6.4f' %ir1.ebond[i][j], ' %6.4f' %ir2.ebond[i][j],
          # 'ebond: %6.4f' %ir1.ebond[i][9], ' %6.4f' %ir2.ebond[i][9],
          # 'Eov: %6.4f' %ir1.Eover, ' %6.4f' %ir2.Eover,
          'Eang: %6.4f' %ir1.Eang, ' %6.4f' %ir2.Eang,
          'Etcon: %6.4f' %ir1.Etcon, ' %6.4f' %ir2.Etcon,
          # 'Eun: %6.4f' %ir1.Eunder,' %6.4f' %ir2.Eunder,
          'Etor: %6.4f' %ir1.Etor, ' %6.4f' %ir2.Etor,
          # 'Ele: %6.4f' %ir1.Elone, ' %6.4f' %ir2.Elone,
          # 'Evdw: %6.4f' %ir1.Evdw, ' %6.4f' %ir2.Evdw,
          # 'Ehb: %6.4f' %ir1.Ehb,   ' %6.4f' %ir2.Ehb,
          )
#      E = self.Ebond + self.Elone + self.Eover + self.Eunder + \
#               self.Eang + self.Epen + self.Etcon + \
#               self.Etor + self.Efcon + self.Evdw + self.Ecoul + \
#               self.Ehb + self.Eself + self.zpe

Ebv1 = np.array(E1) + np.array(Eo1) + np.array(Ev1)
Ebv2 = np.array(E2) + np.array(Eo2) + np.array(Ev2)
plot(e=Etor1,e1=Etor2,label='structure-1',label1='structure-2',fig='Etor.pdf')
plot(e=Ef1,e1=Ef2,label='structure-1',label1='structure-2',fig='Efcon.pdf')
plot(e=Et1,e1=Et2,label='structure-1',label1='structure-2',fig='Etcon.pdf')
plot(e=Ep1,e1=Ep2,label='structure-1',label1='structure-2',fig='Epen.pdf')
plot(e=El1,e1=El2,label='structure-1',label1='structure-2',fig='Elone.pdf')
plot(e=Eu1,e1=Eu2,label='structure-1',label1='structure-2',fig='Eunder.pdf')
plot(e=Ebv1,e1=Ebv2,label='structure-1',label1='structure-2',fig='Ebvdw.pdf')
plot(e=Ev1,e1=Ev2,label='structure-1',label1='structure-2',fig='Evdw.pdf')
plot(e=Eo1,e1=Eo2,label='structure-1',label1='structure-2',fig='Eover.pdf')
plot(e=Ea1,e1=Ea2,label='structure-1',label1='structure-2',fig='Eang.pdf')
plot(e=E1,e1=E2,label='structure-1',label1='structure-2',fig='Ebond.pdf')
# plot(e=e,label='Bond Energy',fig='Ebond.pdf')




#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
from os import system, getcwd, chdir,listdir
from os.path import isfile # exists
from irff.irff_np import IRFF_NP
from irff.AtomDance import AtomDance
from irff.plot.deb_bde import deb_bo
import argh
import argparse
import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from ase.io.trajectory import Trajectory
from ase.io import read
import json as js



def taper(r,vdwcut=10.0):
    tp = 1.0+np.divide(-35.0,np.power(vdwcut,4.0))*np.power(r,4.0)+ \
         np.divide(84.0,np.power(vdwcut,5.0))*np.power(r,5.0)+ \
         np.divide(-70.0,np.power(vdwcut,6.0))*np.power(r,6.0)+ \
         np.divide(20.0,np.power(vdwcut,7.0))*np.power(r,7.0)
    return tp


def vdw(r,Devdw=0.01,gamma=1.0,gammaw=1.0,vdw1=1.0,rvdw=2.0,alfa=12.0):
    gm3  = np.power(1.0/gamma,3.0)
    r3   = np.power(r,3.0)
    
    rr   = np.power(r,vdw1) + np.power(1.0/gammaw,vdw1)
    f13  = np.power(rr,1.0/vdw1)

    tpv  = taper(r)

    expvdw1 = np.exp(0.5*alfa*(1.0-np.divide(f13,2.0*rvdw)))
    expvdw2 = np.square(expvdw1)
    evdw    = tpv*Devdw*(expvdw2-2.0*expvdw1)
    return evdw

# with open('ffield-FromPaperSort.json','r') as lf:
#      j = js.load(lf)
#      p = j['p']
with open('ffield.json','r') as lf:
     j = js.load(lf)
     p = j['p']

bd = 'H-H'
b  = bd.split('-') 
atomi,atomj = b
gammaw      = np.sqrt(p['gammaw_'+atomi]*p['gammaw_'+atomj])
gamma       = np.sqrt(p['gamma_'+atomi]*p['gamma_'+atomj])
alfa        = p['alfa_'+bd]
#alfa       = np.sqrt(p['alfa_'+atomi]*p['alfa_'+atomj])
vdw1        = p['vdw1']
rvdw        = p['rvdw_'+bd]
# rvdw      = np.sqrt(p['rvdw_'+atomi]*p['rvdw_'+atomj])
Devdw       = p['Devdw_'+bd]
# Devdw     = np.sqrt(p['Devdw_'+atomi]*p['Devdw_'+atomj])

print ('Devdw: {:6.4f} '.format(Devdw))
print ('Gamma: {:6.4f} '.format(gamma))
print ('Gammaw: {:6.4f} '.format(gammaw))
print ('alfa: {:6.4f} '.format(alfa))
print ('vdw1: {:6.4f} '.format(vdw1))
print ('rvdw: {:6.4f} '.format(rvdw))

#rint(Devdw*vdw1)
# print(rvdw*vdw1)

r   = np.linspace(1.8,4.0,50)
ev  = vdw(r,Devdw=Devdw,gamma=gamma,gammaw=gammaw,vdw1=vdw1,rvdw=rvdw)
# print(ev)

plt.figure()     
plt.plot(r,ev,alpha=0.8,linewidth=2,linestyle='-',color='r',
         label=r'$E_{vdw}$')
plt.legend(loc='best',edgecolor='yellowgreen')
plt.savefig('vdw_energy_{:s}.pdf'.format(bd))
# if show: plt.show()
plt.close()

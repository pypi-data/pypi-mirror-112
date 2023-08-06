#!/usr/bin/env python
# coding: utf-8
from ase.visualize import view
from ase.io import read
from ase.io.trajectory import TrajectoryWriter,Trajectory
from irff.AtomDance import AtomDance
# get_ipython().run_line_magic('matplotlib', 'inline')


atoms  = read('md.traj',index=-1)
ad     = AtomDance(atoms=atoms,rmax=1.33)
# images = ad.bond_momenta_bigest(atoms)
images = ad.stretch([9,10],nbin=50,rst=1.35,red=1.0,scale=1.26,ToBeMoved=[10],traj='md.traj')
ad.close()
# view(images)




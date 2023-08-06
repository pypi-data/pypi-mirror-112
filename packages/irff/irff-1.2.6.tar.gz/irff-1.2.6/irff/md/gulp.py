from __future__ import print_function
from os import system
import numpy as np
from ase import Atoms
from ase.io import read # ,write
from ase.io.trajectory import TrajectoryWriter
from ase.calculators.singlepoint import SinglePointCalculator
import matplotlib.pyplot as plt
from ..molecule import press_mol


def write_gulp_in(A,runword='gradient qiterative nosymmetry conv verb debu',
                  T=298.0,
                  time_step=0.1,
                  tot_step=10.0,
                  maxcyc=2000,
                  lib='reax'):
    ''' runword = keyword in gulp input
        can be 'md conv' 'md conp' 'opti conp'
        qite = iterative solve charges, norx = no charges '''
    finp = open('inp-gulp','w')
    rw = runword.split()
    print(runword,file=finp)
    print('#',file=finp)
    print('#',file=finp)
    if rw[0]=='opti':
       print('maxcyc %d' %maxcyc,file=finp)
    elif rw[0]=='md':
       if rw[1]=='conv':
          print('ensemble nvt',file=finp)
          print('tau_thermostat     0.05 ps',file=finp)
       elif rw[1]=='conp':
          print('integrator leapfrog verlet',file=finp)
          print('ensemble           npt',file=finp)
          print('pressure           0.00 GPa',file=finp)
          print('tau_barostat       0.1 ps',file=finp)
          print('tau_thermostat     0.1 ps',file=finp)

       print('temperature        %f K' %T,file=finp)
       print('timestep           %f fs' %time_step,file=finp)
       print('production         %f ps' %float(tot_step*time_step/1000.0),file=finp)
       print('equilibration      0.0 ps' ,file=finp)
       print('write              1',file=finp)
       print('sample             1',file=finp)

    print('#',file=finp)
    print('title',file=finp)
    print('GULP calculation',file=finp)
    print('end',file=finp)
    print('#',file=finp)
    if lib=='brenner':
       print('%s' %lib,file=finp)
    else:
       print('library %s' %lib,file=finp)

    print('output movie xyz his.xyz',file=finp)
    print('dump 100 restart.grs',file=finp)
    print('#',file=finp)
    
    print('vectors',file=finp)
    cell = A.get_cell()
    for a in cell:
        print(a[0],a[1],a[2],file=finp)
    print('\n',file=finp)

    print('cartesian',file=finp)
    pos = A.get_positions()
    symb= A.get_chemical_symbols()
    for sp,x in zip(symb,pos):
        print(sp,'core',x[0],x[1],x[2],0.0,1.0,0.0,1,1,1,file=finp)
    finp.close()


def get_reaxff_q(natom,fo='out'):
    q = []
    fout = open(fo,'r')
    lines = fout.readlines()
    fout.close()

    for i,line in enumerate(lines):
        if line.find('Final charges from ReaxFF :')>=0:
           charge_line = i
        elif line.find('E(coulomb)')>=0:
           ecoul = float(line.split()[2])
        elif line.find('E(self)')>=0:
           eself = float(line.split()[2])
        elif line.find('E(vdw)')>=0:
           evdw = float(line.split()[2])

    for i in range(natom):
        line = lines[i+5+charge_line]
        l = line.split()
        q.append(float(l[2]))
    return q,ecoul,eself,evdw


def get_reax_energy(fo='out'):
    fout = open(fo,'r')
    for line in fout.readlines():
        if line.find('E(bond)')>=0:
           ebond = float(line.split()[2])
        elif line.find('E(lonepair)')>=0:
           elp   = float(line.split()[2])
        elif line.find('E(over)')>=0:
           eover = float(line.split()[2])
        elif line.find('E(under)')>=0:
           eunder = float(line.split()[2])
        elif line.find('E(val)')>=0:
           eang   = float(line.split()[2])
        elif line.find('E(coa)')>=0:
           tconj   = float(line.split()[2])
        elif line.find('E(pen)')>=0:
           epen  = float(line.split()[2])
        elif line.find('E(tors)')>=0:
           etor  = float(line.split()[2])
        elif line.find('E(conj)')>=0:
           fconj  = float(line.split()[2])
        elif line.find('E(vdw)')>=0:
           evdw   = float(line.split()[2])
        elif line.find('E(hb)')>=0:
           ehb   = float(line.split()[2])
        elif line.find('E(coulomb)')>=0:
           ecl   = float(line.split()[2])
        elif line.find('E(self)')>=0:
           esl   = float(line.split()[2])
        elif line.find('ReaxFF force field')>=0:
           e   = float(line.split()[4])
    fout.close()
    return e,ebond,elp,eover,eunder,eang,epen,tconj,etor,fconj,evdw,ehb,ecl,esl


def change_keyword(lib='reaxff_rdx'):
    system('cp inp-gulp inp-gulp.sample')
    fin  = open('inp-gulp','w')
    fgin = open('inp-gulp.sample', 'r')
    for line in fgin.readlines():                # prepare input file
       if len(line.split())>=1:
          if line.split()[0] == 'library':
             print >>fin, 'library %s' %lib 
             print >>fin, 'maxcyc 1000' 
          else:
             print >>fin, '%s' %line[:-1] # delete /n

    fgin.close()
    fin.close()


def get_md_results(out='gulp.out'):
    ''' get the result from the  gulp MD simulation '''
    flog = open(out,'r')
    E,Epot,T,P = [],[],[],[]

    for line in flog.readlines():
        l = line.split()
        if line.find('Potential energy  (eV) =')>=0:
           Epot.append(float(l[4]))
        elif line.find('Temperature       (K)  =')>=0:
           T.append(float(l[3]))
        elif line.find('Total energy      (eV) =')>=0:
           E.append(float(l[4]))
        elif line.find('Pressure         (GPa) =')>=0:
           P.append(float(l[3]))
    flog.close()
    return E,Epot,T,P


def plot_md(E,Epot,T,P,show=True):
    plt.figure(figsize=(12,12))  

    plt.subplot(2,2,1)  
    plt.ylabel(r'$Total Energy (Unit: eV)$')
    plt.xlabel(r'$Iterations$')
    plt.plot(E,label=r'$Total Energy$', color='blue', linewidth=2)
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(2,2,2)  
    plt.ylabel(r'$Potential Energy (Unit: eV)$')
    plt.xlabel(r'$Iterations$')
    plt.plot(Epot,label=r'$Potential Energy$', color='blue', linewidth=2)
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(2,2,3)  
    plt.ylabel(r'$Temperature (Unit: K)$')
    plt.xlabel(r'$Iterations$')
    plt.plot(T,label=r'$Temperature$', color='blue', linewidth=2)
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(2,2,4)  
    plt.ylabel(r'$Pressure (Unit: GPa)$')
    plt.xlabel(r'$Iterations$')
    plt.plot(P,label=r'$Pressure$', color='blue', linewidth=2)
    plt.legend(loc='best',edgecolor='yellowgreen')

    if show:
       plt.show()
    else:
       plt.savefig('MD_results.svg') 
    plt.close()


def plot_optimize(log='gulp.out'):
    ''' plot the energies or other from gulp log file'''
    flog = open(log,'r')
    cyc,e = [],[]

    for line in flog.readlines():
        l = line.split()
        if line.find('Cycle:')>=0 and line.find('Energy:')>=0:
           cyc.append(float(l[1]))
           e.append(float(l[3]))

    flog.close()
    plt.figure()
    plt.ylabel(r'$Energy (Unit: eV)$')
    plt.xlabel(r'$Iterations$')
    # plt.xlim(6,500)
    # plt.ylim(-625,-600)
    plt.plot(cyc,e,label=r'$energy .VS. iterations$', color='blue', linewidth=2)
    plt.savefig('energy_vs_iteration.png') 
    plt.close()


def get_lattice(inp='inp-gulp'):
    finp = open(inp,'r')
    il = 0
    cell = []
    readlatv = False
    readlat  = False
    for line in finp.readlines():
        l = line.split()
        if line.find('vectors')>=0:
           readlatv = True

        if readlatv and il < 4:
           if il!=0:
              cell.append( [float(l[0]),float(l[1]),float(l[2])])
           il += 1
    finp.close()
    return np.array(cell)


def reaxyz(fxyz):
    # cell = get_lattice()
    f = open(fxyz,'r')
    lines = f.readlines()
    f.close()
    
    natom  = int(lines[0])
    nframe = int(len(lines)/(natom+2))
    
    positions = np.zeros([nframe,natom,3])
    atom_name = []
    energies  = []
    for nf in range(nframe):
        le = lines[nf*(natom+2)+1].split()
        if le[2]!='NaN':
           energies.append(float(le[2]))
           for na in range(natom):
               ln = nf*(natom+2)+2+na
               l  = lines[ln].split()
               
               if nf==0:
                  atom_name.append(l[0])
              
               positions[nf][na][0] = float(l[1])
               positions[nf][na][1] = float(l[2])
               positions[nf][na][2] = float(l[3])
    return atom_name,positions,energies


def xyztotraj(fxyz,checkMol=False,mode='w',scale=True):
    atom_name,positions,e = reaxyz(fxyz)
    cell = get_lattice()
    u    = np.linalg.inv(cell)
    his  = TrajectoryWriter('gulp.traj',mode=mode)

    for i,e_ in enumerate(e):
        if scale:
           pos_ = np.dot(positions[i],u)
           posf = np.mod(pos_,1.0)          # aplling simple pbc conditions
           pos  = np.dot(posf,cell)
        else:
           pos  = positions[i]
        A = Atoms(atom_name,pos,cell=cell,pbc=[True,True,True])
        
        if checkMol:
           A = press_mol(A)

        calc = SinglePointCalculator(A,energy=e[i])
        A.set_calculator(calc)
        his.write(atoms=A)
        del A
    his.close()


def opt(T=350,gen='siesta.traj',mode='w'):
    A = read(gen,index=-1)
    A = press_mol(A)
    write_gulp_in(A,runword='opti conv qiterative',
                  T=T,
                  lib='reax')
    print('\n-  running gulp opt ...')
    system('gulp<inp-gulp>gulp.out')
    xyztotraj('his.xyz',mode='w')



def optl(T=350,gen='poscar.gen',mc=500):
    A = read(gen)
    # A = press_mol(A)
    write_gulp_in(A,runword='opti conp qiterative stre atomic_stress',
                  T=T,maxcyc=mc,
                  lib='reax')
    print('\n-  running gulp optimize ...')
    system('/home/feng/gulp/gulp-5.0/Src/gulp<inp-gulp>gulp.out')
    xyztotraj('his.xyz',mode='w',scale=False)


def npt(T=350,time_step=0.1,tot_step=10.0):
    A = read('packed.gen')
    write_gulp_in(A,runword='md conp qiterative',
                  T=T,
                  time_step=time_step,
                  tot_step=tot_step,
                  lib='reax')
    system('gulp<inp-gulp>gulp.out')
    xyztotraj('his.xyz')


def nvt(atoms=None,gen='poscar.gen',T=350,time_step=0.1,tot_step=100,index=-1,mode='w',lib='reax'):
    if atoms is None:
       atoms = read(gen,index=index)
    write_gulp_in(atoms,runword='md qiterative conv',
                  T=T,
                  time_step=time_step,
                  tot_step=tot_step,
                  lib=lib)
    # print('\n-  running gulp nvt ...')
    system('gulp<inp-gulp>gulp.out')
    xyztotraj('his.xyz',mode=mode)


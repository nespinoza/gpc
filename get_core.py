# -*- coding: utf-8 -*-
import numpy as np
import subprocess
import os

def spaced(input,space):
    fixed = False
    i = 0
    input = space+input
    while(not fixed):
        if(input[i:i+1] == '\n'):
           input = input[0:i+1]+space+input[i+1:]
           i = i + len(space)
        i = i + 1
        if(i == len(input)-1):
          fixed = True
    return input

def get_models(core_masses,distances):
    cwd = os.getcwd()
    os.mkdir('models')
    os.chdir('models')
    for distance in distances:
        for core_mass in core_masses:
            if distance == 'point02AU' and core_mass == '00b':
                core_mass = '00c'
            p = subprocess.Popen('wget http://www.ucolick.org/~jfortney/models/tbl_Evpcore_'+\
                            core_mass+'_'+distance+'.dat',stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell = True)
            p.wait()
            if(p.returncode != 0 and p.returncode != None):
                print '\t >> Download failed. The error was:\n'
                out, err = p.communicate()
                print spaced(err,"\t \t")
                print '\t >> Check your internet connection and/or J. Fortney webpage. If the '
                print '\t    problem persists, contact the author of this code.'
    os.chdir(cwd)

def read_data(fname):
    f = open(fname,'r')
    first_time = True
    while True:
        line = f.readline()
        if line == '':
            break
        elif line[0] == 't':
            t = np.double(line.split('=')[-1])
            f.readline()
            f.readline()
            f.readline()
            while True:
                line = f.readline()
                if line[0] == '-':
                    break
                else:
                    me,mj,rj,g,tint,L =line.split()
                    if first_time:
                        out_array = np.array([t,np.double(me),np.double(mj),np.double(rj)])
                        first_time = False
                    else:
                        out_array = np.vstack((out_array,np.array([t,np.double(me),np.double(mj),np.double(rj)])))

    f.close()
    return out_array

def read_input(fname):
    def read_value(l):
        vals = l.split('=')[-1]
        v,v_err = vals.split('+-')
        return np.double(v),np.double(v_err)
    f = open(fname,'r')
    output_array = 12*[[]]
    while True:
        line = f.readline()
        if line == '':
           break
        else:
           if line[0] == '|':
               if 'Name' in line:
                   output_array[11] = ''.join(((line.split('=')[-1]).split('\n')[0]).split())
               elif 'System Age' in line:
                   output_array[0],output_array[1] = read_value(line)
               elif 'Luminosity' in line:
                   output_array[2],output_array[3] = read_value(line)
               elif 'Planet Mass' in line:
                   output_array[4],output_array[5] = read_value(line)
               elif 'Planet Radius' in line:
                   output_array[6],output_array[7] = read_value(line)
               elif 'Planet-Star' in line:
                   output_array[8],output_array[9] = read_value(line)
               elif 'Number of simulations' in line:
                   output_array[10] = np.int(line.split('=')[-1])
               else:
                   print '\t WARNING: Input value:'
                   print '\t '+line
                   print '\t not used/understood!'
    return output_array

def save_results(pname,vals):
    if not os.path.exists('results'):
        os.mkdir('results')
    fname = 'results/'+pname+'_mc_simulations.dat'
    fout = open(fname,'w')
    for i in range(len(vals)):
        fout.write(str(vals[i])+'\n')
    fout.close()

print '\n'
print '\t #########################################  '
print '\t ##   Giant Planet Cores (GPCs) v.1.0.  ##  '
print '\t #########################################  '
print '\t' 
print '\t  Author: Nestor Espinoza (nsespino@uc.cl)  '
print '\t'
print '\t   Models obtained from Fortney, Marley     '
print '\t    and Barnes (2007; ApJ, 659, 1661)       '
print '\t  '
print '\t  DISCLAIMER: If you make use of this code  ' 
print '\t  please cite the above referenced work and '
print '\t  acknowledge the work put on this code.    '
print '\n'

# Define core masses to extract (in Mearth) along with distances (in AU):
core_masses = ['00b','10a','25a','50a','100a']#['10a','25a','50a','100a']#['00b','10a','25a','50a','100a']
core_masses_numbers = [0.,10.,25.,50.,100.]#[10.,25.,50.,100.]#[0.,10.,25.,50.,100.]
distances = ['point02AU','point045AU','point1AU','1AU','9point5AU']
distances_numbers = [0.02,0.045,0.1,1.0,9.5]

# Start the code:
print '\t >> 1. Checking models...'
if not os.path.exists('models'):
    print '\t    Models not found. Downloading them from J. Fortney webpage...'
    get_models(core_masses,distances)
    print '\t    Done!\n'
else:
    print '\t    Model folder found!\n'
print '\t >> 2. Extracting data...'

# Extract data. The final full_data array has 6 dimensions,
# which are full_data = (t,Me,Mj,Rj,distance,core_mass), with
# the following definitions:
#
# t:                Time in Gyr of the system.
#
# Me:               Mass of the planet in Earth units.
#
# Mj:               Mass of the planet in Jupiter units.
#
# Rj:               Radius of the planet in Jupiter units.
#
# distance:         Distance of the system from the parent star
#                   in AU.
#
# core_mass:        Core-mass of the planet in earth units.
#
#
# Keep in mind that the parent star is assumed to be solar. Also, 
# the composition of the core is 50% rock/50% ice.

first_time = True
for i in range(len(distances)):
    distance = distances[i]
    for j in range(len(core_masses)):
        core_mass = core_masses[j]
        if distance == 'point02AU' and core_mass == '00b':
            core_mass = '00c'

        data = read_data('models/tbl_Evpcore_'+core_mass+'_'+distance+'.dat')    
        if first_time:
            full_data = np.zeros([data.shape[0],data.shape[1]+2])
            full_data[:,0:data.shape[1]] = data
            full_data[:,data.shape[1]] = np.ones(data.shape[0])*distances_numbers[i]
            full_data[:,data.shape[1]+1] = np.ones(data.shape[0])*core_masses_numbers[j]
            first_time = False
        else:
            f_data = np.zeros([data.shape[0],data.shape[1]+2])
            f_data[:,0:data.shape[1]] = data
            f_data[:,data.shape[1]] = np.ones(data.shape[0])*distances_numbers[i]
            f_data[:,data.shape[1]+1] = np.ones(data.shape[0])*core_masses_numbers[j]
            full_data = np.vstack((full_data,f_data))

print '\t    Done!\n'

print '\t >> 3. Reading data...'
age,age_err,L,L_err,Mp,Mp_err,Rp,Rp_err,a,a_err,nsims,pname = read_input('input_data.gpc')
print '\t    Done!\n'

print '\t >> 4. Sampling core masses for planet '+pname+'...'
from scipy.interpolate import griddata
points = np.zeros([full_data.shape[0],4])
points[:,0] = full_data[:,0]  # Times in Gyr of the system
points[:,1] = full_data[:,2]  # Planet mass in Mj
points[:,2] = full_data[:,3]  # Planet radius in Rj
points[:,3] = full_data[:,4]  # System distance from central star (assumed solar) in AU
values = full_data[:,5]       # Core mass in Earth units

print '\t    Monte-carloing input values '+str(int(nsims))+' times...'

# Monte-carlo the age, mass, radius and distance of the planet...
t = np.random.normal(age,age_err,nsims)
m = np.random.normal(Mp,Mp_err,nsims)
r = np.random.normal(Rp,Rp_err,nsims)
d = np.random.normal(a,a_err,nsims)

# Monte-carlo the luminosity of the star and generate the equivalent
# distance to a solar-type star of the planet:
l = np.random.normal(L,L_err,nsims)
dsun = d*np.sqrt(1./l)

print '\t    Interpolating table...'
vals = griddata(points, values, (t,m,r,dsun), method='linear')
idx = -np.isnan(vals)
vals = vals[idx]
print '\t    Done!\n'
print '\t >> 5. Saving results...'
save_results(pname,vals)
cm = np.median(vals)
cm_err = np.sqrt(np.var(vals))
print "\t    Planet core simulations saved under the 'results' folder"
print '\t    The planet has a core mass of {0:2.2f} +- {1:2.2f} MEarth'.format(cm,cm_err)
print '\n'

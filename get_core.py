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
    print '\t Models not found. Downloading them from J. Fortney webpage...'
    get_models(core_masses,distances)
    print '\t Done!\n'
else:
    print '\t Model folder found!\n'
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

        print distance,core_mass
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

print '\t Done!\n'

print '\t >> 3. Sampling core masses...'
from scipy.interpolate import griddata
points = np.zeros([full_data.shape[0],4])
points[:,0] = full_data[:,0]  # Times in Gyr of the system
points[:,1] = full_data[:,2]  # Planet mass in Mj
points[:,2] = full_data[:,3]  # Planet radius in Rj
points[:,3] = full_data[:,4]  # System distance from central star (assumed solar) in AU
values = full_data[:,5]       # Core mass in Earth units
print 't,Mj,Rj,dist'
print points
print 'core mass'
print values

t = 2.0#1.0#4.5
m = 0.356#3.146#0.837
r = 0.718#1.217#1.065
d = 0.04288#0.02#0.03048

grid = griddata(points, values, (t,m,r,d), method='linear')
print grid

print '\n'

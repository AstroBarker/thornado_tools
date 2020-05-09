###############################################################################
#
# Quick plotting script for plotting 1D thornado data.
#
# Syntax is `python plot_compare.py fileNumber field`, e.g., 
#  plot_thor1d.py 000123 uCF_D -x uAF_T
# The -x argument is optional -- default is x1
#
###############################################################################

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py
import sys
import argparse

mb = 1.660539 * pow(10,-24)

parser = argparse.ArgumentParser(description='Quick plot some data')
parser.add_argument('fileNumber', metavar='file', type=str, 
    help='file to plot')
parser.add_argument('y', metavar='y', type=str, 
    help='field to plot along y axis', default = 'uCF_D')
parser.add_argument('-x', metavar='x', type=str, 
    help='field to plot along x axis', default='x')    

args = parser.parse_args()

# Turn args into filenames
# --------------------------- USER PARAMETERS -----------------------------
dataDir = '/Users/bbarker/dgHydro/analysis/data/1d/gravitational_collapse/'
prog = 'GravitationalCollapse'
sim = '256_B1.75_C0.0/' # Will have to change if different run!!!
# -------------------------------------------------------------------------
fns = []
fns.append(dataDir + 'cw/' + sim + 'Output/' + prog + '_FluidFields_' + 
            args.fileNumber + '.h5')
fns.append(dataDir + 'clim/' + sim + 'Output/' + prog + '_FluidFields_' + 
            args.fileNumber + '.h5')  

fields = []
labels = []
units = []

for fn in fns: 
    with h5py.File(fn, 'r') as f:
        for key in f.keys():
            print(key)

        for foo in args.x, args.y:
            if (foo == 'uCF_D'):
                df = f['/Fluid Fields/Conserved/Conserved Baryon Density'][:]
                label = 'Density'
                unit = 'g/cc'
            elif (foo == 'uAF_P'):
                df =f['/Fluid Fields/Auxiliary/Pressure'][:]
                label = 'Pressure'
                unit = r'erg cm$^{-2}$'
            elif (foo == 'uAF_T'):
                df =f['/Fluid Fields/Auxiliary/Temperature'][:]
                label = 'Temperature'
                unit = 'K'
            elif (foo == 'uPF_V1'):   
                df = f['/Fluid Fields/Primitive/Three-Velocity (1)' ][:] 
                label = 'Velocity 1'
                unit = 'cm/s'
            elif (foo == 'uAF_Ye'):
                uCF_Ne = f['/Fluid Fields/Conserved/Conserved Electron Density'][:]
                uCF_D = f['/Fluid Fields/Conserved/Conserved Baryon Density'][:]
                df = mb * uCF_Ne / uCF_D
                label = 'Ye'
                unit = ' '
            elif (foo == 'uPF_D'):
                df = f['/Fluid Fields/Primitive/Comoving Baryon Density' ][:]
                label = 'Density Primitive Fields'
                unit = 'g/cc'
            elif (foo =='x' or foo == 'x1'):
                df = f['/Spatial Grid/X1'][:]  
                label = 'x'
                unit = 'km'
            else:
                print("Please supply a supported field, or add it in.") 
            fields.append(df)
            labels.append(label)
            units.append(unit)
        
        time = f['Time'][:]    
        print(time)   
if (args.x != 'x'):
    x_field_cw = fields[0][0][0][:]
    x_field_clim = fields[2][0][0][:]
else:
    x_field_cw = fields[0]  
    x_field_clim = fields[2]  
y_field_cw = fields[1][0][0][:]
y_field_clim = fields[3][0][0][:]

print(f"Plotting: {label}")
fig, cax = plt.subplots(1, sharex=True,figsize=(7,7))
cax.semilogx(x_field_cw, y_field_cw, '-o', label='Componentwise', color = "magenta", 
linewidth=1.5, fillstyle='none')#CWin
cax.semilogx(x_field_clim, y_field_clim, '-o',  label='Characteristic', color = "blue", 
linewidth=1.5, fillstyle='none')#CLIM
cax.set(xlabel=labels[0] + ' [' + units[0] + ']', 
        ylabel = labels[1] + ' [' + units[1] + ']',
        title = labels[1])
cax.legend()
plt.show()


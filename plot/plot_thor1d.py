###############################################################################
#
# Quick plotting script for plotting 1D thornado data.
#
# Syntax is `python plot_thor1d.py file.h5 field`, e.g., 
#  plot_thor1d.py Output/RiemannProblem_FluidFields_000010.h5 uCF_D -x uAF_T
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
parser.add_argument('file', metavar='file', type=str, 
    help='file to plot')
parser.add_argument('y', metavar='y', type=str, 
    help='field to plot along y axis', default = 'uCF_D')
parser.add_argument('-x', metavar='x', type=str, 
    help='field to plot along x axis', default='x')    

args = parser.parse_args()

with h5py.File(sys.argv[1], 'r') as f:
    for key in f.keys():
        print(key)

    fields = []
    labels = []
    units = []
    for foo in args.x, args.y:
        if (foo == 'uCF_D'):
            df = f['/Fluid Fields/Conserved/Conserved Baryon Density'][:]
            label = 'Density'
            unit = 'g/cc'
        if (foo == 'uCF_E'):
            df = f['/Fluid Fields/Conserved/Conserved Energy Density'][:]
            label = 'Energy Density'
            unit = 'erg/cc'
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
            # uCF_Ne = f['/Fluid Fields/Conserved/Conserved Electron Density'][:]
            # uCF_D = f['/Fluid Fields/Conserved/Conserved Baryon Density'][:]
            # df = mb * uCF_Ne / uCF_D
            df = f['/Fluid Fields/Auxiliary/Electron Fraction'][:]
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
        elif (foo =='dPdYe'):
            df1 = f['/Fluid Fields/Auxiliary/Electron Fraction'][:]
            df2 =f['/Fluid Fields/Auxiliary/Pressure'][:]
            df = np.diff(df2) / np.diff(df1)
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
    x_field = fields[0][0][0][:]
else:
    x_field = fields[0]    
y_field = fields[1][0][0][:]

print(f"Plotting: {label}")
fig, cax = plt.subplots(1, sharex=True,figsize=(7,7))
cax.plot(x_field, y_field, '.', label=labels[1], color = "magenta", linewidth=1.5, fillstyle='none')
cax.set(xlabel=labels[0] + ' [' + units[0] + ']', 
        ylabel = labels[1] + ' [' + units[1] + ']')
cax.legend()
plt.show()


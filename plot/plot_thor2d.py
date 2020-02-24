###############################################################################
#
# Quick plotting script for plotting 2D thornado data.
#
# Syntax is `python plot_thor1d.h5 file.h5 field`, e.g., 
#  plot_thor1d.py Output/Jet_FluidFields_000010.h5 uCF_D
#
###############################################################################

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py
import sys

# Global Plotting Settings
mpl.rcParams['lines.linewidth'] = 4
mpl.rcParams['legend.handlelength']=4
mpl.rcParams['legend.fontsize']=14
mpl.rcParams['legend.frameon']=False
mpl.rcParams['axes.labelsize']=18
mpl.rcParams['xtick.minor.visible']=True
mpl.rcParams['ytick.minor.visible']=True
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['xtick.minor.width'] = 2
mpl.rcParams['ytick.minor.width'] = 2
mpl.rcParams['xtick.labelsize']   = 14
mpl.rcParams['ytick.labelsize']   = 14

mb = 1.660539 * pow(10,-24)

with h5py.File(sys.argv[1], 'r') as f:
    for key in f.keys():
        print(key)

    # These are the only supported fields for quick plotting. Add more if necessary.
    if (sys.argv[2] == 'uCF_D'):
        df = f['/Fluid Fields/Conserved/Conserved Baryon Density'][:]
    elif (sys.argv[2] == 'uAF_P'):
        df =f['/Fluid Fields/Auxiliary/Pressure'][:]
    elif (sys.argv[2] == 'uPF_V1'):   
        df = f['/Fluid Fields/Primitive/Three-Velocity (1)' ][:] 
    elif (sys.argv[2] == 'uAF_Ye'):
        uCF_Ne = f['/Fluid Fields/Conserved/Conserved Electron Density'][:]
        uCF_D = f['/Fluid Fields/Conserved/Conserved Baryon Density'][:]
        df = mb * uCF_Ne[0][0][:] / uCF_D[0][0][:]  
    else:
        Print("Please supply a supported field.")      
    
    time = f['Time'][:]
    x = f['/Spatial Grid/X1'][:]
    y = f['/Spatial Grid/X2'][:]
    
    print(time)   

data = np.zeros(len(x1))   
data = df[0]

print("Plotting: %s" % sys.argv[2])
cmap = plt.get_cmap('Blues')
fig, cax = plt.subplots(1, sharex=True,sharey=True,figsize=(10,10))
for i in range(1) :
    im = cax.pcolormesh(x, y, np.log10(data), cmap=cmap)#, norm=norm)
    cax.set_aspect('auto')
    cax.set(xlabel=r'x [km]', ylabel=r"y [km]")
    cax.set_title("Log Density")
    plt.gca().set_aspect('equal', adjustable='box')
level=np.logspace(np.log10(data_d.min()), np.log10(data_d.max()), num=30)
cf = cax.contour(x1,
               x2, data_d,colors='k', linewidths=1.0,levels=level,
               )   
cax.set(xlabel="x [km]",ylabel = sys.argv[2])
cax.legend()
plt.show()


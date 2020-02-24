

import os, sys
import matplotlib.pyplot as plt
import numpy as np 
import yt
import subprocess
import h5py    
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable  
import json

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

def get_data( directory, mode, sim ):
    ''' Gets the specified data and writes to to a json file to be plotted. 
    
    Parameters:
    --------------
    directory: the paraent directory
    mode: either 'ref' or 'comp'
        ref: works with the nx=10000 reference run
        comp: compares low res CLIM and CW
    sim: the desired run to get. e.g., 400_B1.75_C0.0
        
    '''

    if( mode == 'comp'):

        #Deal with output directory separately, so we can use original dir for naming. 
#         sim = "400_B1.75_C0.0"
        # sim = "ye_no_discont"
        outputdir_cw = directory + '/clim/' + sim + '/Output/'
        outputdir_clim = directory + '/cw/' + sim + '/Output/'
        
        # print("Data Directory:", outputdir)
        
        dirs = {}
        dirs['cw'] = os.listdir( outputdir_cw )
        dirs['clim'] = os.listdir( outputdir_clim )

    elif( mode == 'ref'):

        #Deal with output directory separately, so we can use original dir for naming. 
#         sim = "400_B1.75_C0.0"
        outputdir_clim = directory + '/ref/' + sim + '/Output/'
        
        # print("Data Directory:", outputdir)
        
        dirs = {}
        dirs['ref'] = os.listdir( outputdir_clim )    

    else:
        print('{mode} is not a valid mode.')
        exit


    # print(dirs['clim'])

    files = []
    # os.chdir(outputdir)

    # Initialize data structures
    time = {}
    x1 = {}
    uAF_P = {}
    uCF_D = {}
    uAF_T = {}
    uPF_V1 = {}
    uAF_Ye = {}
    uAF_Cs = {}
    uAF_Gm = {}
    uAF_F = {}
    uAF_S = {}
    uAF_e = {}

    data = {}
    
    # Loop over all "keys" (in this case, the CW and CLIM data)
    for k in dirs.keys():
        print(k)
        data[k] = {}

        for dat in dirs[k]:
            
            fn = k + '/' + sim + '/Output/' + dat
            #print outputdir + '/' + data
            print("Loading File: ", dat) 
            #Load HDF Data
            with h5py.File(fn, 'r') as f:
                # for key in f.keys():
                #     print(key)   

                time[k] = f['Time'][:]
                x1[k] = f['/Spatial Grid/X1'][:]

                uAF_P[k]  = f['/Fluid Fields/Auxiliary/Pressure'][:]
                uAF_T[k] = f['/Fluid Fields/Auxiliary/Temperature'][:]
                uAF_Ye[k] = f['/Fluid Fields/Auxiliary/Electron Fraction'][:]
                uAF_Cs[k] = f['/Fluid Fields/Auxiliary/Sound Speed'][:]
                uAF_Gm[k] = f['/Fluid Fields/Auxiliary/Ratio of Specific Heats (Gamma)'][:]
                uAF_S[k] = f['/Fluid Fields/Auxiliary/Entropy Per Baryon'][:]
                uAF_e[k] = f['/Fluid Fields/Auxiliary/Specific Internal Energy'][:]

                uCF_D[k] = f['/Fluid Fields/Conserved/Conserved Baryon Density'][:]

                uPF_V1[k]  = f['/Fluid Fields/Primitive/Three-Velocity (1)' ][:]
                f.close()

            print("Time: ", time, "ms")  
        


        # Actual data structures, for convenience.
        
            data[k][time[k][0]] = {}

            data[k][time[k][0]]['x1'] = x1[k][:].tolist()
            data[k][time[k][0]]['uCF_D'] = uCF_D[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_P'] = uAF_P[k][0][0][:].tolist()
            data[k][time[k][0]]['uPF_V1'] = uPF_V1[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_T'] = uAF_T[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_Ye'] = uAF_Ye[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_Cs'] = uAF_Cs[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_Gm'] = uAF_Gm[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_S'] = uAF_S[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_e'] = uAF_e[k][0][0][:].tolist()
            data[k][time[k][0]]['uAF_F'] = (uAF_e[k][0][0][:] - uAF_T[k][0][0][:] * uAF_S[k][0][0][:]).tolist()

        print(data.keys())

        fn = sim + '_dat.json'
        with open(fn, 'w') as outfile:
            json.dump(data, outfile)

    return fn

def MakeMovie( filename, mode, field_x, field_y ):
    ''' Create a movie of the data written by 'get_data'.
        Parameters: 
            filename - a json file output by get_data() 

            mode: ref or comp.

            field_x, field_y - string, the fields to plot. uCF_D, uAP_P, etc. Naming follow thornado names. 
            Not implemented for all fields. '''

    with open(filename) as json_file:
        data = json.load(json_file)

    if(mode == 'comp'):
        times = data['cw'].keys()
    else:
        times = data['ref'].keys()    
    times_sorted = np.sort(list(times))

    # Find the minimum and maximum values of field_y, field_x for plotting
    min_y = np.min(data['cw'][times_sorted[0]][field_y])
    max_y = np.max(data['cw'][times_sorted[0]][field_y])

    min_x = np.min(data['cw'][times_sorted[0]][field_x])
    max_x = np.max(data['cw'][times_sorted[0]][field_x])

    for j in range(len( times_sorted )):
        if(np.min(data['cw'][times_sorted[j]][field_y]) < min_y):
            min_y = np.min(data['cw'][times_sorted[j]][field_y])
        if(np.max(data['cw'][times_sorted[j]][field_y]) > max_y):
            max_y = np.max(data['cw'][times_sorted[j]][field_y])
        if(np.min(data['cw'][times_sorted[j]][field_x]) < min_x):
            min_x = np.min(data['cw'][times_sorted[j]][field_x])
        if(np.max(data['cw'][times_sorted[j]][field_x]) > max_x):
            max_x = np.max(data['cw'][times_sorted[j]][field_x])


    for j in range(len( times_sorted )):

        fig, ax = plt.subplots()

        fig, cax = plt.subplots(1, sharex=True,sharey=True,figsize=(10,10))


        for i in range(1) :
            # cax.plot(data['cw'][times_sorted[j]]['x1'], data['cw'][times_sorted[j]][field], label = "Componentwise")
            # cax.plot(data['clim'][times_sorted[j]]['x1'], data['clim'][times_sorted[j]][field], label = "Characteristic")
            if(mode == 'comp'):
                cax.plot(data['cw'][times_sorted[j]][field_x], data['cw'][times_sorted[j]][field_y], '.', label = "Componentwise")
                cax.plot(data['clim'][times_sorted[j]][field_x], data['clim'][times_sorted[j]][field_y], '.', label = "Characteristic")
                cax.set_ylim([min_y, max_y])
                cax.set_xlim([min_x, max_x])
            else:
                cax.plot(data['ref'][times_sorted[j]][field_x], data['ref'][times_sorted[j]][field_y], '.', label = "Reference")

            cax.set(xlabel=field_x, ylabel=field_y)
            cax.legend()

        if (j < 10):
            id_string = '00' + str(j)
        elif( j >= 10 and j < 100):
            id_string = '0' + str(j)
        else :
            id_string = str(j)

        # outDir = './Images_' + str(field_x) + '_' + str(field_y) + '_' + str(mode) + '/'
        outDir = 'Images/' + filename[:-9] #+ '/' + str(field_x) + '_' + str(field_y) + '_' + str(mode) + '/'
        
        # Go through one directory at a time and make all needed

        if not os.path.isdir(outDir):
            os.mkdir(outDir)

        outDir = outDir + '/' + str(field_x) + '_' + str(field_y) + '_' + str(mode) + '/'
        print(outDir)

        if not os.path.isdir(outDir):
            os.mkdir(outDir)

        fname = outDir + id_string + ".png"

        print('Saving frame', fname, "\n")
        plt.savefig(fname)

    
    os.chdir(outDir)
    # Remove the `output.mp4` file if it exists. The jupyter notebook cannot overwrite it.
    if os.path.isfile('output.mp4'):
        print('rm -f output.mp4')
        os.system('rm -f output.mp4') 
    cmd = "ffmpeg -f image2 -r 10 -pattern_type glob -i '*.png' -vcodec libx264 -pix_fmt yuv420p output.mp4"    
    print( cmd )
                
    os.system( cmd )
    return;

if __name__=='__main__':
    import sys

    # Write a json file containing data
    mode = str(sys.argv[2])
    fn = get_data('./', mode)

    MakeMovie(fn, mode, sys.argv[1])

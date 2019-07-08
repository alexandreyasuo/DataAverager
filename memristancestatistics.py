import exitroutines
# exit and cleanup

import csv
# needed to read raw data in CSV

import os
import glob
import sys
# needed for directory manipulation

import configparser
# for config file

import numpy as np
# numerical functions

import io
# needed for separating bitstreams

import openpyxl
# needed to save to XLSX

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# plotting

# Initialization of parameters1
config = configparser.ConfigParser()

#counter variables
warning = 0
verbose = 10

if os.path.exists('config.ini'):
    config.read('config.ini')
else:
    print('WARNING: Configuration file not found. Initiating config file with default values')
    warning += 1
    configfile = open('config.ini', 'w')
    config['Directories'] = {'WorkingDir' : os.path.dirname(os.path.realpath(__file__))}
    config['Settings'] = {'Verbose' : 10}
    config.write(configfile)
    configfile.flush()
    configfile.close()
    print('Done')

if 'WorkingDir' in config['Directories']:
    workdirectory = config['Directories']['WorkingDir']
else:
    print('ERROR: Working directory not in configuration. Is the ini file correct and not corrupted?')
    exitroutines.getout(warning, -1)

try:
    verbose = (int)(config['Settings']['Verbose'])
except:
    print('WARNING: Verbose not in configuration file. Assigning default value: ', verbose)
    warning += 1

print('Changing to working directory...')
try:
    os.chdir(os.path.join(workdirectory, 'data'))
except:
    print('ERROR: Could not change to working directory. Does directory exist?')
    exitroutines.getout(warning, -1)

numberofcsvs = [i for i in glob.glob('*.{}'.format('csv'))]

if numberofcsvs == []:
    print('Nothing to do, no CSV files found')
    exitroutines.getout(warning, 1)

maindata=[]
voltages=[]
currents=[]
charges=[]
resistances=[]
fluxes=[]
conductances=[]
times=[]

currentflux = 0
currentcharge = 0

for i in numberofcsvs:
    data = np.genfromtxt(i, skip_header=0, skip_footer=0, names=['frequency', 'fwdarea', 'bwdarea', 'fwdaread', 'bwdaread'], delimiter=",")

    plt.figure(figsize=(8,8))
    plt.subplot(221)
    plt.semilogx(data['frequency'], data['fwdaread'], c='k')
    plt.semilogx(data['frequency'], data['fwdarea'], c='b')
    title = str('Forward loop area x f')
    plt.title(title)
    plt.ylabel('Forward loop area [W]')
    plt.xlabel('Frequency [Hz]')
    plt.tight_layout()

    plt.subplot(222)
    plt.semilogx(data['frequency'], data['bwdaread'], c='k')
    plt.semilogx(data['frequency'], data['bwdarea'], c='b')
    title = str('Backward loop area x f')
    plt.title(title)
    plt.ylabel('Backward loop area [W]')
    plt.xlabel('Frequency [Hz]')
    plt.tight_layout()
                    
    plt.savefig('Final.png')
    plt.close()
    

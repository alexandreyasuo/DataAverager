import exitroutines
# exit and cleanup

import circle_fit as cf

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

voltagechunk = []
currentchunk = []
capacitances = []

for i in numberofcsvs:

    for j in range(0,100):
        voltagechunk.append(0)
        currentchunk.append(0)
    
    data = np.genfromtxt(i, skip_header=0, skip_footer=0, names=['Voltage', 'Current'], delimiter=",")
    maxv = np.amax(data['Voltage'])
    maxi = np.amax(data['Current'])
    for j in range(0,len(data['Voltage'])):
        data['Voltage'][j] = data['Voltage'][j]/maxv
        data['Current'][j] = data['Current'][j]/maxi

    radiuses = data['Voltage']

    
    for j in range(0,len(radiuses)):
        radiuses[j] = 0

    for j in range(0,len(data['Voltage'])-100):
        for k in range(0,100):
            voltagechunk[k] = data['Voltage'][k+j]
            currentchunk[k] = data['Current'][k+j]

        #bestcirclefit = circlefit.leastsquares(voltagechunk,currentchunk)
        xc,yc,r,_ = cf.least_squares_circle([voltagechunk,currentchunk])
        radiuses[j] = (2*maxi)*2*3.14159*10/(2*r*maxv)

radiuses = radiuses[:len(radiuses)-100]
        
fig = plt.figure(1, figsize=(8, 6))
n, b, patches = plt.hist(radiuses, bins=30, color='k')
plt.ylabel("Count")
plt.xlabel("Memristance [GCh]")
plt.savefig("xaxis.png")

bin_max = np.where(n == n.max())
print(b[bin_max][0])
print(maxv)
print(maxi)

exitroutines.getout(warning, 1)

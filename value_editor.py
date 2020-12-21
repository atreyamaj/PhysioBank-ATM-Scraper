import os
from scipy.io import loadmat, savemat
import numpy as np
#First signal at index 30 in .info file
#Last signal at len(info) - 24
#Skip between 2 dataset names = 4 items in between
#Gain starts at 31
#Base starts at 32

def edit_single(num_str): #For editing a single file
    file_open = open("Download_log.txt", "a") #Open download log in append mode
    file_open.write("Editing Record " + num_str + " ... \n") #Update download log
    info_file = "records/" + num_str + "m.info"
    mat_file = "records/" + num_str + "m.mat"
    info = open(info_file).read().split() #Forming the array with all the given file numbers
    mat = loadmat(mat_file) #Loading the .mat file using scipy.io.loadmat(*)
    #Storing the values in lists:
    db_names = []
    base_vals = []
    gain_vals = []
    for xd in range(30, len(info),5):
        db_names.append(info[xd])
        base_vals.append(float(info[xd + 1]))
        gain_vals.append(float(info[xd + 2]))
        if xd >= len(info) - 24:
            break

    emp = []
    #Finding indices for ABP and PLETH values to access them easily
    abp_index = db_names.index('ABP')
    pleth_index = db_names.index('PLETH')
    #Storing some basic values
    abp_gain = gain_vals[abp_index]
    pleth_gain = gain_vals[pleth_index]
    abp_base = base_vals[abp_index]
    pleth_base = base_vals[pleth_index]

    #Finishing making the lists
    emp.append(mat['val'][abp_index])
    emp.append(mat['val'][pleth_index])

    #Converting the previously formed lists into Numpy arrays for optimized computation speed
    #Program has been speeded up by more than 10x
    abp_np = np.array(emp[0])
    pleth_np = np.array(emp[1])

    #Basic Pre-processing before storing in a dictionary
    final_abp = (abp_np - abp_gain) / abp_base
    final_pleth = (pleth_np - pleth_gain) / pleth_base

    valdict = {'ABP' : final_abp, 'PLETH' : final_pleth} #Converting to dictionary so that it can be saved as a .mat file
    
    savemat("records/" + num_str + "_final" + '.mat', valdict) #Converting dictionary to .mat format
    file_open.write("Edited and Saved Record " + num_str + "\n") #Updating Download Log
    file_open.close()




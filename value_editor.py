import os
from scipy.io import loadmat, savemat
import numpy as np
#First signal index at 30
#Last signal at len(info) - 24
#Skip between 2 dataset names = 4 items in between
#Gain starts at 31
#Base starts at 32


#signal_types = ['II', 'AVR', 'V', 'RESP', 'PLETH', 'ABP', 'I', 'III', 'aVR', 'ART', 'CVP', 'MCL', 'aVL', 'AVL', 'PLETH', 'PAP',  ]

def edit_mats():
    sub = 'records/'
    files = os.listdir(sub)
    file_nums = []
    #print(files)
    for i in files:
        string = ""
        for j in i:
            if j == 'm':
                break
            else:
                string += j
        
        file_nums.append(string)
    file_nums.sort()
    #print(file_nums)  

    res = []
    [res.append(x) for x in file_nums if x not in res] 
    #print(res)

    for i in res:
        #print(type(i))
        #print(type(i))
        mat = loadmat(sub + i + "m.mat")
        #print(mat['val'])

        info = open(sub + i + "m.info").read().split()
        #print(info.index('ABP'))
        #print(len(info) - 24)
        #print(info[30], info[len(info) - 24])

        
        '''
        for i in range(30,len(info),5):
            print(info[i])
            if i == len(info) - 24:
                break
        '''
        
        #print(info[37])

        db_names = []
        base_vals = []
        gain_vals = []
        for xd in range(30, len(info),5):
            db_names.append(info[xd])
            base_vals.append(float(info[xd + 1]))
            gain_vals.append(float(info[xd + 2]))
            if xd >= len(info) - 24:
                break
        #print(db_names)
        #print(base_vals)
        #print(gain_vals)
        


        emp = []
        abp_index = db_names.index('ABP')
        pleth_index = db_names.index('PLETH')

        #print (abp_index, pleth_index)
        abp_gain = gain_vals[abp_index]
        pleth_gain = gain_vals[pleth_index]
        abp_base = base_vals[abp_index]
        pleth_base = base_vals[pleth_index]

        emp.append(mat['val'][abp_index])
        #print(len(emp[0]))
        emp.append(mat['val'][pleth_index])
        #print(len(emp[1]))
        #print(emp)
        '''
        x = [[],[]]  #First column abp, second pleth
        for k in emp[0]:
            val = (k - abp_base) / abp_gain    #CONVERT TO NUMPY IMPLEMENTATION
            x[0].append(val)
        for p in emp[1]:
            val = (p - pleth_base) / pleth_gain
            x[1].append(val)
        '''

        abp_np = np.array(emp[0])
        pleth_np = np.array(emp[1])
        final_abp = (abp_np - abp_base) / abp_gain
        final_pleth = (pleth_np - pleth_base) / pleth_gain

        #abpvals = np.array(x[0])
        #plethvals = np.array(x[1])

        valdict = {'ABP' : final_abp, 'PLETH' : final_pleth}
        savemat('Edited_mats/' + i + "_final" + '.mat', valdict)

        #diction = {'ABP' : abpvals, 'PLETH' : plethvals}

        #savemat( i + ".mat", diction)
        



        
        '''
        for i in range(len(db_names)):
            for j in mat['val'][i]:
                x = (j - base_vals[i]) / (gain_vals[i] + 0.00000001)
                emp[i].append(x)
        print(emp)

        '''
#edit_mats()
def edit_single(num_str):
    file_open = open("Download_log.txt", "a")
    file_open.write("Editing Record " + num_str + " ... \n")
    info_file = "records/" + num_str + "m.info"
    mat_file = "records/" + num_str + "m.mat"
    info = open(info_file).read().split()
    mat = loadmat(mat_file)
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
    abp_index = db_names.index('ABP')
    pleth_index = db_names.index('PLETH')
    abp_gain = gain_vals[abp_index]
    pleth_gain = gain_vals[pleth_index]
    abp_base = base_vals[abp_index]
    pleth_base = base_vals[pleth_index]

    emp.append(mat['val'][abp_index])
    emp.append(mat['val'][pleth_index])

    abp_np = np.array(emp[0])
    pleth_np = np.array(emp[1])

    final_abp = (abp_np - abp_gain) / abp_base
    final_pleth = (pleth_np - pleth_gain) / pleth_base

    valdict = {'ABP' : final_abp, 'PLETH' : final_pleth}
    #savemat('Edited_mats/' + num_str + "_final" + '.mat', valdict)
    savemat("records/" + num_str + "_final" + '.mat', valdict)
    file_open.write("Edited and Saved Record " + num_str + "\n")
    file_open.close()


#edit_single("3002094")

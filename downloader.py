import pyautogui as pa
from time import sleep
import os
from value_editor import *  #Imports the edit_single function, which is used later on in the program

#https://archive.physionet.org/cgi-bin/atm/ATM/

#https://archive.physionet.org/atm/mimic2wdb/30/


#Patient Record Numbers:
f = open('/home/atreyamaj/Desktop/Physi_CDL/try11.txt', 'r')
text = f.read()
numbers= text.split()
log = open('Download_log.txt','a')



def main_check():
    while True:
        checker = pa.locateOnScreen('load_check_home.png')
        sleep(0.5)
        if checker != None:
            break
#Open Chrome
chrome = pa.locateOnScreen('chrome_icon.png')
pa.rightClick(chrome[0], chrome[1])

#Open a new Window
new_win = pa.locateOnScreen('new_window.png')
pa.click(new_win[0], new_win[1])
sleep(2)


#Format for info files:   https://archive.physionet.org/atm/mimic2wdb/30/3000003/3000003/0/e/export/matlab/3000003m.info
base_url = "https://archive.physionet.org/atm/mimic2wdb/"
matlab_exp = "export/matlab/"
info_name = "m.info"
mat_name = "m.mat"

db_num = "30/"
db_index = "0/"
identifier = "e/"


for i in numbers:
    num = i
    pa.hotkey('ctrl', 'l')
    #Open the File URL, on Chrome it automatically starts downloading the file.
    new_url = base_url + db_num + num + "/" + num + "/" + db_index + identifier + matlab_exp + num 
    sleep(2)
    pa.typewrite(new_url + info_name)
    sleep(1)
    pa.hotkey('Enter')
    sleep(2)
    
    #We need to check if both 'ABP' and "PLETH' values are present in the downloaded .info file
    #If they are, we will download the corresponding .mat file
    abp_check = False
    pleth_check = False
    sleep(2)
    dwn = "records/"  #Directory for saving the files
    new = dwn + num + info_name
    base = dwn + num
    
    if os.path.exists(new): #Checks if the file has finished downloading and exists in the download directory
        file_open = open("Download_log.txt","a") #Log to track which actions are being taken
        file_open.write("Downloading mat file for " + num + "\n") #Updating the download log.
        file_open.close()
        new_f = open(new, 'r')
        text_check = new_f.read()
        checker = text_check.split()
        for i in checker:  #Checking if both ABP and PLETH ECG values exist in the downloaded .info file
            if i == "ABP":
                abp_check = True
            elif i == "PLETH":
                pleth_check = True
        new_f.close()

        if abp_check == True and pleth_check == True: #If both ABP and PLETH ECG values exist, download the .mat file for that number
            pa.hotkey("ctrl", "l")
            pa.typewrite(new_url + mat_name)
            pa.hotkey("Enter")

            mat_checker = False
            while mat_checker != True:
                if os.path.exists("records/" + num + "m.mat"):
                    mat_checker = True
            edit_single(num) #Segregates the ABP and PLETH values from the others, code is in value_editor.py
            os.remove("records/" + num + "m.mat") #Deleting the old unedited file to optimize storage
            file_open = open("Download_log.txt", "a")
            file_open.write("Deleting Original mat file for record" + num + "\n") #Update Download Log
            file_open.close()
            sleep(2)
        else:
            os.remove("records/" + num + "m.info") #If ABP and PLETH don't exist, delete the .info file
            file_open = open("Download_log.txt", "a")
            file_open.write("No ABP and PLETH. Deleting info file for record " + num) #Updating Log
    else:
        continue #To avoid runtime errors






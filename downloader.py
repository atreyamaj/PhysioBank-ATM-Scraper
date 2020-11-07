import pyautogui as pa
from time import sleep
import os
from value_editor import *

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
    new_url = base_url + db_num + num + "/" + num + "/" + db_index + identifier + matlab_exp + num 
    sleep(2)
    pa.typewrite(new_url + info_name)
    sleep(1)
    pa.hotkey('Enter')
    sleep(2)
    #print(num)
    abp_check = False
    pleth_check = False
    sleep(2)
    dwn = "records/"
    new = dwn + num + info_name
    base = dwn + num
    #print(new)
    if os.path.exists(new):
        file_open = open("Download_log.txt","a")
        file_open.write("Downloading mat file for " + num + "\n")
        file_open.close()
        new_f = open(new, 'r')
        text_check = new_f.read()
        checker = text_check.split()
        for i in checker:
            if i == "ABP":
                abp_check = True
            elif i == "PLETH":
                pleth_check = True
        new_f.close()

        if abp_check == True and pleth_check == True:
            pa.hotkey("ctrl", "l")
            pa.typewrite(new_url + mat_name)
            pa.hotkey("Enter")

            mat_checker = False
            while mat_checker != True:
                if os.path.exists("records/" + num + "m.mat"):
                    mat_checker = True
            edit_single(num)
            os.remove("records/" + num + "m.mat")
            file_open = open("Download_log.txt", "a")
            file_open.write("Deleting Original mat file for record" + num + "\n")
            file_open.close()
            sleep(2)
        else:
            os.remove("records/" + num + "m.info")
            file_open = open("Download_log.txt", "a")
            file_open.write("No ABP and PLETH. Deleting info file for record " + num)
    else:
        continue






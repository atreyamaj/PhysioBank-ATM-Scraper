# Anomaly Detection in PhysioBank ATM ECG Heart Beat data

The PhysioBank ECG ATM, maintained by MIT, is notoriously hard to scrape as it is designed to block users from accessing the site as soon as it detects any sort of automation. 
To bypass this, I have written a scraper that makes use of GUI manipulation in order to get ECG data from the ATM which mimics how a human would navigate through the ATM, after which I use an LSTM autoencoder in order to encode the data and cluster them later for automatic anomaly detection to find if a person's heartbeat is indicative of a potential cardiac disorder. 
This repository currently contains code upto the Autoencoder step.


## To Use this Repository:
1. Make a folder named 'Records' or whatever name you want (edit the code accordingly), and set Chrome's download folder to your folder.
2. Edit the file paths used accordingly.
3. This code is specific to the "MIMIC II/III Waveform Database, part 0 (mimic2wdb/30)" archive at https://archive.physionet.org/cgi-bin/atm/ATM/

To use this code for other archives, save the file numbers from the JavaScript Code (You can find this using Inspect Element) and use a Matlab delimiter on it to segretate the file names. The numbers are stored in try11.txt for this archive. For archives 31 and 32, the numbers are stored in try13.txt and try15.txt respectively.

4. After everything is set up, run 'downloader.py' to download the ECG data.
5. After the data is downlaoded, run 'LSTM_auto_cluster.py' in order to auto-Encode the data using LSTMs. The clustering step will be added soon. 
6. Install Python 3.6.x, and the following libraries: PyAutoGUI, Keras, Numpy, Matplotlib.pyplot, Sci-kit Learn

`$sudo -H pip3 install keras numpy pyautogui matplotlib sklearn`
  
The above is meant for Debian Linux based distributions (In my case, I used Ubuntu 20.04 LTS)
## To come:
1. The clustering part will be added soon in order to carry out automatic anomaly detection.
2. After the entire pipeline is up and running, I plan on deploying the model on a website that I will be designing and making. I am currently thinking of opting to use Heroku or a similar service for deployment. Users will be able to upload files and the model will try to look for anomalies in the user's heart beat data.

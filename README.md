# Anomaly Detection in PhysioBank ATM ECG Heart Beat data

The PhysioBank ECG ATM, maintained by MIT, is notoriously hard to scrape as it is designed to block users from accessing the site as soon as it detects any sort of automation. 
To this end, I have written a GUI-based scraper in order to get ECG data from the ATM which mimics how a human would navigate through the ATM, after which I use an LSTM autoencoder in order to encode the data and cluster them later for automatic anomaly detection to find if a person's heartbeat is indicative of a potential cardiac disorder. 
This repository currently contains code upto the Autoencoder step.


## To Use this Repository:
1. Make a folder named 'Records' or whatever name you want (edit the code accordingly), and set Chrome's download folder to your folder.
2. Edit the paths used accordingly.
3. This code is specific to the "MIMIC II/III Waveform Database, part 0 (mimic2wdb/30)" archive at https://archive.physionet.org/cgi-bin/atm/ATM/

To use this code for other archives, save the file numbers from the JavaScript Code (You can find this using Inspect Element) and use a Matlab delimiter on it to segretate the file names.

4. After everything is set up, run 'downloader.py' to download the ECG data.
5. After the data is downlaoded, run 'LSTM_auto_cluster.py' in order to auto-Encode the data using LSTMs. The clustering step will be added soon. 
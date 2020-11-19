#PhysioBank-ATM-ECG-Anomaly-Detection

The PhysioBank ECG ATM, maintained by MIT, is notoriously hard to scrape as it is designed to block users from accessing the site as soon as it detects any sort of automation. 
To this end, I have written a GUI-based scraper in order to get ECG data from the ATM, after which I use an LSTM autoencoder in order to encode the data and cluster them later for automatic anomaly detection to find if a person's heartbeat is indicative of a potential cardiac disorder. 
This repository currently contains code upto the Autoencoder step.

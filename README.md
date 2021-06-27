<p align="center"> <img src="https://github.com/xSneaky/Openus/blob/abc418ca919e3d4d7337f4bcca8baddf9f3b9d6b/images/logo.gif"> </p>


## About The Project
OPENUX was a private project of mine that I have been working on for a few months. While developing this tool I have learned a lot and although this tool is not perfect I will carry on imporving this untill it's perfect. 

## What does it do?
There are currently two scripts that are used to work the tool. The hunter.py script generates random IP addresses that's scanned with map to check if a web server is running on the host. If a web server is running the hunter script will then check the page title and headers comparing them to a blacklist. As long as the it does not match the blacklists, it will be put in a search index engine file named IP_Database then saved in the following format:
IP, URL, page title, time, date, Web server software, PHP Version, Scanned by openvas and ID.
To speed up this process you can set how many threads we want the hunter to use in /modules/config.ini but make sure you leave enough for openvas scans. When the hunter finds a host you will get an alert though discord using webhooks.

The Second scrip is open-face. Pi does all the automation for openvas grabbing data from IP_Database as long as "Scanned=False" to stop repeated scans. Again, like the hunter you can configure username, password, gvm sock location, scan_id, config_id, pdf_id, discord alert webhooks and how many hosts to scan at one time.At the moment the severity level is set to 5.9 so any results, lower than this will be ignored and anything higher will be made into a PDF and saved in /results as well as send to discord via webhook.

## Main Features
- Multi Threading for Nmap
- Discord webhooks for Found Targets, Scanning Targets and PDF Reports
- Openvas Scan Limit to stop overloading
- Search Indexing Engine using whoosh to store hosts information


## System Recommendation
We recommend using a VPS since you are scanning many random IP addresses your ISP might send you letters, terminate contract or even be blacklisted from many websites. Openvas also has to check thousands of signatures on hosts so you will need a system with more than 4 cores and 8GB ram otherwise you might run into issues like Openven crashing, slow scans or been limited of how many hosts you can scan.


## Road map
- Add Discord bot for searching the index
- Integrate with Metasploit for auto exploitation
- Clean up some code and make it more user friendly  
## Images
Scan added to openvas
<p align="left"> <img src="https://github.com/xSneaky/Openus/blob/0938f91b1a21771d5c9e89b3122fda8aefb26255/images/ScanAdded.png"> </p>

Host Found with nmap and added to index
<p align="left"> <img src="https://github.com/xSneaky/Openus/blob/6df8d51bc018c02ecb6328361f7a37c9354e3917/images/ScanFound.png"> </p>

PDF Reports
<p align="left"> <img src="https://github.com/xSneaky/Openus/blob/b19c3b3a0276edc23d03d33f9f8faa8172516953/images/PDF.png"> </p>


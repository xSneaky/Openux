<p align="center"> <img src="https://github.com/xSneaky/Openus/blob/abc418ca919e3d4d7337f4bcca8baddf9f3b9d6b/images/logo.gif"> </p>


## About

OPENUX was a private project of mine that I have been working on for a few months. This tool uses Openvas, Nmap-Python, Whoosh (Search Indexing Engine), Requests, bs4, Discord webhooks and gvm-tools to generate an IP address randomly. 

The IP is then passed to Nmap to find active web servers. If a web server is found, it will grab the web server's headers and page title comparing them to a blacklist.

If everything checks out it will be passed to Openvas to scan. After the scan is complete it will check the severity of the report. Depending on what you have set the settings to, it will then use Discord webhooks to send you the PDF report of the Medium or High Vulns.


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


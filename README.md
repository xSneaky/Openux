<p align="center"> <img src="https://github.com/xSneaky/Openus/blob/3fc7d26aef68effe7903847adcb49a497dcde3d2/logo.gif"> </p>


## About

OPENUX was a private project of mine that I have been working on for a few months. This tool uses Openvas, Nmap-Python, Whoosh (Search Indexing Engine), Requests, bs4, Discord webhooks and gvm-tools to generate an IP address randomly. 

The IP is then passed to Nmap to find active web servers. If a web server is found, it will grab the web server's headers and page title comparing them to a blacklist.

If everything checks out it will be passed to Openvas to scan. After the scan is complete it will check the severity of the report. Depending on what you have set the settings to, it will then use Discord webhooks to send you the PDF report of the Medium or High Vulns.

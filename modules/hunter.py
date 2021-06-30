import nmap
import random
import requests
from fake_useragent import UserAgent
from multiprocessing import Process, Queue
import datetime
from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.index import create_in
from whoosh.fields import *
from bs4 import BeautifulSoup
import re
import time
#from discordbot import *
import asyncio
import itertools
from discord_webhook import DiscordWebhook, DiscordEmbed

timedate = datetime.datetime.now()
date = timedate.strftime("%x")
time = timedate.strftime("%X")
title_search = ["Google", "Welcome to nginx!", "Apache2 Debian Default Page: It works", "Test Page for the Apache HTTP Server", "Apache HTTP Server Test Page powered by CentOS"]
Header_search = ["cloudflare"]
def worker():
    requests.packages.urllib3.disable_warnings()
    while True:
        try:
            ua = UserAgent()
            header = {'User-Agent':str(ua.random)}
            nscan = nmap.PortScanner()
            one = str(random.randint(0, 99))
            two = str(random.randint(0, 99))
            three = str(random.randint(0, 99))
            four = str(random.randint(0, 99))
            IP = one + "." + two + "." + three + "." + four
            nscan.scan(IP, '80-443', arguments="--min-rate 100")
            for host in nscan.all_hosts():
                for proto in nscan[host].all_protocols():
                    lport = nscan[host][proto].keys()
                    for port in lport:
                        if str(port) == "80" and nscan[host][proto][port]['state'] == "open":
                            req = requests.get("http://" + IP, allow_redirects=True, verify=False, headers=header)
                            server_header = req.headers.get('Server')
                            PHP_header = req.headers.get('X-Powered-By')
                            soup = BeautifulSoup(req.text, 'html.parser')
                            if str(req.status_code) == "200":
                                if str(soup.title).replace("<title>", "").replace("</title>", "") != title_search:
                                    if server_header != Header_search:
                                        #print("Found: " + IP + "\n" + req.url + "\n" + str(soup.title).replace("<title>", "").replace("</title>", "") + "\n" + server_header + "\n" + PHP_header + "\n")
                                        print("Found: " + IP)
                                        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/855544282668466187/UWLYBRAdLwoINDZZGdRwaGs3JOd0Ak6QIMj4_-q_pzhkZvbQ0Otdfqf5qZ-VzcrhtWo2")
                                        embed = DiscordEmbed(title="Target Found", color='03b2f8')
                                        embed.add_embed_field(name="IP Address", value=str(IP), inline=False)
                                        embed.add_embed_field(name="URL", value=str(req.url), inline=False)
                                        embed.add_embed_field(name="Page Title", value=str(soup.title).replace("<title>", "").replace("</title>", ""), inline=False)
                                        embed.add_embed_field(name="Date Added To Database", value=str(date), inline=False)
                                        embed.add_embed_field(name="Time Added To Database", value=str(time), inline=False)
                                        embed.add_embed_field(name="Web Server Version", value=str(server_header), inline=False)
                                        embed.add_embed_field(name="PHP Version", value=str(PHP_header), inline=False)
                                        webhook.add_embed(embed)
                                        response = webhook.execute()
                                        ix = index.open_dir("/home/data/Python/IP_Database")
                                        writer = ix.writer()
                                        writer.add_document(IP=IP, URL=req.url, page_title=str(soup.title).replace("<title>", "").replace("</title>", ""), time=time, date=date, Server=server_header, PHP=PHP_header, Scanned="False", path="/" + IP)
                                        writer.commit()
                            elif str(port) == "443" and nscan[host][proto][port]["state"] == "open":
                                req = requests.get("https://" + IP, allow_redirects=True, verify=True, headers=header)
                                print("Found port 443" + ":" + str(IP))
        except:
            pass

if __name__ == "__main__":
    queue = Queue()
    processes = [Process(target=worker, args=()) for x in range(5)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

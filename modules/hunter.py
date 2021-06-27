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
import asyncio
import itertools
from discord_webhook import DiscordWebhook, DiscordEmbed
import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(dir_path + 'config.ini')

timedate = datetime.datetime.now()
date = timedate.strftime("%x")
time = timedate.strftime("%X")
title_search = open(dir_path + "/../page-title-blacklist.txt", "r")
Header_search = open(dir_path + "/../headers-blacklist.txt", "r")
def worker():
    requests.packages.urllib3.disable_warnings()
    while True:
        try:
            ua = UserAgent()
            header = {'User-Agent':str(ua.firefox)}
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
                                if str(soup.title).replace("<title>", "").replace("</title>", "") in title_search:
                                    print("Blacklisted")
                                else:
                                    if server_header in Header_search:
                                        pass
                                    else:
                                        webhook = DiscordWebhook(url=config['HUNTER']['hunter-webhook'])
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
                                        ix = index.open_dir("/IP_Database")
                                        writer = ix.writer()
                                        writer.add_document(IP=IP, URL=req.url, page_title=str(soup.title).replace("<title>", "").replace("</title>", ""), time=time, date=date, Server=server_header, PHP=PHP_header, Scanned="False", path="/" + IP)
                                        writer.commit()
        except:
            pass

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
import configparser
from gvm.errors import GvmError
from gvm.errors import GvmResponseError
from gvm.transforms import EtreeCheckCommandTransform
import nmap
transform = EtreeCheckCommandTransform()
import requests
from bs4 import BeautifulSoup
import time
import datetime
import random
from threading import Thread
from gvm.xml import pretty_print
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed
from threading import Thread
from requests.exceptions import MissingSchema

#loads config
config = configparser.ConfigParser()
config.read("config.ini")

def Openvas():
    try:
        connection = UnixSocketConnection(path=config['OPENVAS']['gvm-socket-path'])
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(config['OPENVAS']['openvas-username'], config['OPENVAS']['openvas-password'])
    except GvmError as LoginError:
        if str(LoginError) == "Could not connect to socket " + config['OPENVAS']['gvm-socket-path']:
            print("Error: " + str(LoginError) + ", Please check if current path is set correct in the config file \"gvm-socket-path\" or make sure the services are running")
        else:
            print("Error: " + str(LoginError))

    def Current_Tasks():
        try:
            Running = 0
            Running_Tasks = gmp.get_tasks(filter_string='status="Running", rows=1000')
            for Running_Tasks_Now in Running_Tasks.xpath('//status'):
                Running +=1
            return Running
        except GvmResponseError:
            pass

    def Current_Requested_Tasks():
        Running = 0
        Requested_Tasks = gmp.get_tasks(filter_string='status="Requested", rows=1000')
        for Requested_Tasks_Now in Requested_Tasks.xpath('//status'):
            Running += 1
        return Running

    def Current_Queued_Tasks():
        Running = 0
        Queued_Tasks = gmp.get_tasks(filter_string='status="Queued", rows=1000')
        for Queued_Tasks_Now in Queued_Tasks.xpath('//status'):
            Running +=1
        return Running

    def Current_Done_Tasks():
        Running = 0
        Done_Tasks = gmp.get_tasks(filter_string='status="Done", rows=1000')
        for Done_Tasks_Now in Done_Tasks.xpath('//status'):
            Running +=1
        return Running

    def Interrupted_Done_Tasks():
        Running = 0
        Interrupted_Tasks = gmp.get_tasks(filter_string='status="Interrupted", rows=1000')
        for Interrupted_Tasks_Now in Interrupted_Tasks.xpath('//status'):
            Running +=1
        return Running
        
    def Nmap():
        while True:
            nscan = nmap.PortScanner()
            one = str(random.randint(0, 99))
            two = str(random.randint(0, 99))
            three = str(random.randint(0, 99))
            four = str(random.randint(0, 99))
            IP = one + "." + two + "." + three + "." + four
            #IP = "50.63.35.99"
            print("Trying: " + str(IP))
            nscan.scan(IP,'80', arguments="--min-rate 100")
            for host in nscan.all_hosts():
                for proto in nscan[host].all_protocols():
                    lport = nscan[host][proto].keys()
                    for port in lport:
                        if port == 80:
                            try:
                                #print("Found: " + IP + ":" + str(port))
                                requests.packages.urllib3.disable_warnings()
                                req = requests.get("http://" + IP, allow_redirects=True, verify=False, timeout=10)
                                URL = req.url
                                server_header = req.headers.get('Server')
                                PHP_header = req.headers.get('X-Powered-By')
                                soup = BeautifulSoup(req.text, 'html.parser')
                                page_title = str(soup.title).replace("<title>", "").replace("</title>", "")
                                if str(req.status_code) == "200":
                                    with open("page-title-blacklist.txt", "r") as titleblacklist:
                                        if str(soup.title).replace("<title>", "").replace("</title>", "") in titleblacklist.read():
                                            print("Skipping IP: " + IP + "\nReason: " + str(soup.title).replace("<title>", "").replace("</title>", ""))
                                            break
                                        else:
                                            with open("headers-blacklist.txt", "r") as headersblacklist:
                                                if server_header in headersblacklist.read():
                                                    print("Skipping IP: " + IP + "\nReason: " + server_header)
                                                    break
                                                else:
                                                    try:
                                                    #print("\n--Found Target--" + "\nIP: " + IP + "\nServer header: " + str(server_header) + "\nPHP Version: " + str(PHP_header) + "\nPage Title: " + str(soup.title).replace("<title>", "").replace("</title>", ""))
                                                        webhook = DiscordWebhook(url=config['DISCORD']['Target-Found'])
                                                        embed = DiscordEmbed(title="Target Found", color='03b2f8')
                                                        embed.add_embed_field(name="IP Address", value=str(IP), inline=False)
                                                        embed.add_embed_field(name="URL", value=str(URL), inline=False)
                                                        embed.add_embed_field(name="Page Title", value=str(page_title), inline=False)
                                                        embed.add_embed_field(name="Web Server Version", value=str(server_header), inline=False)
                                                        embed.add_embed_field(name="PHP Version", value=str(PHP_header), inline=False)
                                                        webhook.add_embed(embed)
                                                        response = webhook.execute()
                                                    except MissingSchema as E:
                                                        print("Please Check if Discord:Openvas-Stats in config.ini is correct, " + str(E))
                                                        sys.exit()
                                                    return IP, server_header, PHP_header, page_title, URL;
                            except:
                                pass
    def CVE_Check():
        CVE_Check = gmp.get_tasks(filter_string='status="Done", rows=1000')
        for task in CVE_Check.findall('task'):
            task_ID = task.get('id')
            report = task.find('last_report')
            last = task.find('last_report')
            if last is not None:
                report = last.find('report')
                if report is not None:
                    full_report = gmp.get_report(report.get('id'), details=True, filter_string="severity>6.9")
                    jmpToResults = full_report.find('report').find('report').find('results')
                    for result in jmpToResults:
                        host = result.find('nvt')
                        for cve in host.find('refs'):
                            da = cve.attrib
                            if da.get('type') == "cve":
                                ss = gmp.get_cve(da.get('id'))
                                for ssf in ss.xpath('//info/cve/raw_data'):
                                    for entry in ssf.findall('{http://scap.nist.gov/schema/feed/vulnerability/2.0}entry'):
                                        for summary in entry.findall('{http://scap.nist.gov/schema/vulnerability/0.4}summary'):
                                            for software in entry.findall('{http://scap.nist.gov/schema/vulnerability/0.4}references'):
                                                for ll in software.findall('{http://scap.nist.gov/schema/vulnerability/0.4}source'):
                                                    if ll.text == "EXPLOIT-DB":
                                                        for gg in software.findall('{http://scap.nist.gov/schema/vulnerability/0.4}reference'):
                                                            summary = str(summary.text)
                                                            exploit_DB_ID = str(gg.get('href').replace("http://www.exploit-db.com/exploits/", "").replace("/", ""))
                                                            return summary, exploit_DB_ID, task_ID;
    def Add_Target():
        name = "Suspect Host {} {}".format(Target_IP, str(datetime.datetime.now()))
        response = gmp.create_target(name=name, hosts=[Target_IP], port_list_id=config['OPENVAS']['gvm-port-list-id'])
        name = "Scan Suspect Host {}".format(Target_IP)
        response = gmp.create_task(name=name, config_id=config['OPENVAS']['gvm-config-id'], target_id=response.get('id'), scanner_id=config['OPENVAS']['gvm-scanner-id'])
        response = gmp.start_task(response.get('id'))

    task_id_list = []
    while True:
        Running = int(Current_Tasks())
        Requested = int(Current_Requested_Tasks())
        Queued = int(Current_Queued_Tasks())
        Done = int(Current_Done_Tasks())
        Interrupted = int(Interrupted_Done_Tasks())
        Total = Running + Requested + Queued
        print("\n--Status--" + "\nDone: " + str(Done) + "\nRunning: " + str(Running) + "\nRequested: " + str(Requested) + "\nQueued: " + str(Queued) + "\nInterrupted: " + str(Interrupted) + "\nTotal Running: " + str(Total) + "\n")
        try:
            webhook = DiscordWebhook(url=config['DISCORD']['Openvas-Stats'])
            embed = DiscordEmbed(title="Openvas Status", color='03b2f8')
            embed.add_embed_field(name="Running", value=int(Running), inline=False)
            embed.add_embed_field(name="Requested", value=int(Requested), inline=False)
            embed.add_embed_field(name="Queued", value=int(Queued), inline=False)
            embed.add_embed_field(name="Done", value=int(Done), inline=False)
            embed.add_embed_field(name="Interrupted", value=int(Interrupted), inline=False)
            embed.add_embed_field(name="Total", value=int(Total), inline=False)
            webhook.add_embed(embed)
            response = webhook.execute()
        except MissingSchema as E:
            print("Please Check if Discord:Openvas-Stats in config.ini is correct, " + str(E))
            sys.exit()

        if Total != int(config['OPENVAS']['Scan-Limit']):
            Target_IP = Nmap()
            Add_Target()
        else:
            print("Hit Scan Limit: " + str(Total))
            if Done >= 1:
                summary, exploit_DB_ID, task_ID = CVE_Check()
                IP, server_header, PHP_header, page_title, URL = Nmap()
                if str(task_ID) not in task_id_list:
                    task_id_list.append(task_ID)
                    #print(task_id_list)
                    #print("Found Exploits")
                    #print("Summary: " + summary)
                    #print("Task ID: " + task_ID)
                    #print("ExploitDB-ID: " + exploit_DB_ID)
                    #print("\n")
                    try:
                        webhook = DiscordWebhook(url=config['DISCORD']['CVE-Found-Webhook'])
                        embed = DiscordEmbed(title="CVE Found", color='03b2f8')
                        embed.add_embed_field(name="IP Address", value=str(IP), inline=False)
                        embed.add_embed_field(name="URL", value=str(URL), inline=False)
                        embed.add_embed_field(name="Page Title", value=str(page_title), inline=False)
                        embed.add_embed_field(name="Web Server Version", value=str(server_header), inline=False)
                        embed.add_embed_field(name="PHP Version", value=str(PHP_header), inline=False)
                        webhook.add_embed(embed)
                        response = webhook.execute()
                    except MissingSchema as E:
                        print("Please Check if Discord:Openvas-Stats in config.ini is correct, " + str(E))
                        sys.exit()
                    time.sleep(60)
    #(CVE_Check())


Openvas()


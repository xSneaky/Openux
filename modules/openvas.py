#Openvas
import xml.etree.ElementTree as ET
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
import datetime
import sys
from argparse import Namespace
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.index import create_in
from whoosh.fields import *
from discord_webhook import DiscordWebhook, DiscordEmbed
from base64 import b64decode
from pathlib import Path
import os
import time

def main():
    connection = UnixSocketConnection(path="/opt/gvm/var/run/gvmd.sock", timeout=600000000)
    transform = EtreeTransform()
    with Gmp(connection, transform=transform) as gmp:
        gmp.authenticate('gvmadmin', '*-__Rosi3__-*')

    Tasks_Running = 0
    while True:
        try:
            Tasks_Running = 0
            get_status = gmp.get_tasks()
            for status in get_status.xpath('//status'):
                if status.text != 'Done':
                    Tasks_Running += 1
            print(Tasks_Running)
            time.sleep(60)
            if Tasks_Running != 1:
                load_data = index.open_dir("/home/data/Python/IP_Database")
                with load_data.searcher() as searcher:
                    query = QueryParser("Scanned", load_data.schema).parse("False")
                    results = searcher.search(query, limit=1)
                    for result in results:
                        ipaddress = result.get('IP')
                        URL = result.get('URL')
                        page_title = result.get('page_title')
                        date = result.get('date')
                        time1 = result.get('time')
                        server = result.get('Server')
                        PHP = result.get('PHP')
                        path = result.get('path')
                    name = "Suspect Host {} {}".format(ipaddress, str(datetime.datetime.now()))
                    response = gmp.create_target(name=name, hosts=[ipaddress], port_list_id="33d0cd82-57c6-11e1-8ed1-406186ea4fc5")
                    name = "Scan Suspect Host {}".format(ipaddress)
                    response = gmp.create_task(name=name, config_id="daba56c8-73ec-11df-a475-002264764cea", target_id=response.get('id'), scanner_id="08b69003-5fc2-4037-a479-93b440211c73")
                    response = gmp.start_task(response.get('id'))
                    writer = load_data.writer()
                    writer.update_document(IP=ipaddress, URL=URL, page_title=page_title, time=time1, date=date, Server=server, PHP=PHP, Scanned="True", path=path)
                    writer.commit()
                    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/855074456212733953/j8QDLp8z5QxC9tO_aEs2EOpLne3ODgWkH3Bjc5HGy8v6T_fD6rmKbULa_RyOZVMcRLSd")
                    embed = DiscordEmbed(title="Target Added For Scanning", color='03b2f8')
                    embed.add_embed_field(name="IP Address", value=str(ipaddress), inline=False)
                    embed.add_embed_field(name="URL", value=str(URL), inline=False)
                    embed.add_embed_field(name="Page Title", value=str(page_title), inline=False)
                    embed.add_embed_field(name="Date Added To Database", value=str(date), inline=False)
                    embed.add_embed_field(name="Time Added To Database", value=str(time1), inline=False)
                    embed.add_embed_field(name="Web Server Version", value=str(server), inline=False)
                    embed.add_embed_field(name="PHP Version", value=str(PHP), inline=False)
                    webhook.add_embed(embed)
                    response = webhook.execute()
            else:
                print("Too many tasks running")
                print("Checking for Done tasks")
                for status in get_status.xpath('//status'):
                    if status.text == "Done":
                        resp = gmp.get_tasks()
                        for task in resp.findall('task'):
                            last = task.find('last_report')
                            if last is not None:
                                report = last.find('report')
                                if report is not None:
                                    specReport = gmp.get_report(report.get('id'),filter_string="severity>5.9", details=True)
                                    jmpToResults = specReport.find('report').find('report').find('results')
                                    for result in jmpToResults:
                                        host = result.find('host')
                                        file_check = os.path.isfile("/home/data/Python/PDFS/" + host.text + ".pdf")
                                        if file_check == False:
                                            pdf_filename = "/home/data/Python/PDFS/" + host.text + ".pdf"                                
                                            pdf_report_format_id = "c402cc3e-b531-11e1-9163-406186ea4fc5"
                                            response = gmp.get_report(report_id=report.get('id'), report_format_id=pdf_report_format_id, filter_string="apply_overrides=1 min_qod=70 first=1 sort-reverse=severity rows=10 severity>5.9")
                                            report_element = response.find("report")
                                            content = report_element.find("report_format").tail
                                            binary_base64_encoded_pdf = content.encode('ascii')
                                            binary_pdf = b64decode(binary_base64_encoded_pdf)
                                            pdf_path = Path(pdf_filename).expanduser()
                                            pdf_path.write_bytes(binary_pdf)
                                            webhook = DiscordWebhook(url="https://discord.com/api/webhooks/855496703385403422/LzeOkjgJcoaWMO6pjIhqrJEaamvZhiBXZ-MJsU3KZmM6sPVT9cR-iYK984_-OJBo1xBf")
                                            print("Sending PDF Report")
                                            with open("/home/data/Python/PDFS/" + host.text + ".pdf", "rb") as f:
                                                webhook.add_file(file=f.read(), filename=host.text + ".pdf")
                                            response = webhook.execute()
                                        else:
                                            pass
                                else:
                                    pass
        except:
            print("Socket Error, restarting services")
            gvm_restart = os.popen("systemctl restart gsa.service && gvm.service && openvas,service")
            time.sleep(60)

from modules import hunter
from modules import openvas
from threading import Thread
import configparser
from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.index import create_in
from whoosh.fields import *
import datetime
import os.path

#Creates Files
dir_path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(dir_path + "/IP_Database"):
    print("Creating Search Indexing")
    os.mkdir(dir_path + "/IP_Database")
    schema = Schema(IP=TEXT(stored=True), URL=TEXT(stored = True), page_title=TEXT(stored = True), time=TEXT(stored = True), date=TEXT(stored = True), Server=TEXT(stored = True), PHP=TEXT(stored = True), Scanned=TEXT(stored = True), path=ID(unique=True, stored = True))
    ix = create_in(dir_path + "/IP_Database/", schema)
    print("Done")
if not os.path.exists(dir_path + "/reports"):
    print("Creating reports file")
    os.mkdir(dir_path + "/reports")
    print("Done")
if not os.path.exists(dir_path + "/page-title-blacklist.txt"):
    print("Creating page title blacklist")
    open(dir_path + "/page-title-blacklist.txt", "w")
    print("Done")
if not os.path.exists(dir_path + "/headers-blacklist.txt"):
    print("Creating headers blacklist")
    open(dir_path + "/headers-blacklist.txt", "w")
    print("Done")

#Starts Modules
config = configparser.ConfigParser()
config.read(dir_path + "/modules/config.ini")
Thread(target=openvas.main).start()
if openvas.main() == False:
    print("Error, Please check username or password")
    sys.exit()
else:
    for x in range(int(config['HUNTER']['nmap-threads'])):
        Thread(target=hunter.worker).start()

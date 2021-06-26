from modules import hunter
from modules import openvas
from threading import Thread
import configparser

config = configparser.ConfigParser()
config.read("/home/data/Python/openux/modules/config.ini")
Thread(target=openvas.main).start()
for x in range(int(config['HUNTER']['nmap-threads'])):
    Thread(target=hunter.worker).start()

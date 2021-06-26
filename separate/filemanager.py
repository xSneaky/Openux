from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.index import create_in
from whoosh.fields import *
import datetime
import os.path
timedate = datetime.datetime.now()
time = timedate.strftime("%x")
date = timedate.strftime("%X")
import pprint

#Creates Data File
if not os.path.exists("/home/data/Python/IP_Database"):
    os.mkdir("/home/data/Python/IP_Database")
schema = Schema(IP=TEXT(stored=True), URL=TEXT(stored = True), page_title=TEXT(stored = True), time=TEXT(stored = True), date=TEXT(stored = True), Server=TEXT(stored = True), PHP=TEXT(stored = True), Scanned=TEXT(stored = True), path=ID(unique=True, stored = True))
#ix = create_in("/home/data/Python/IP_Database/", schema)
#open the file and search

load_data = index.open_dir("/home/data/Python/IP_Database")
with load_data.searcher() as searcher:
    query = QueryParser("Scanned", load_data.schema).parse("False")
    results = searcher.search(query, limit=1)
    for result in results:
        print(result.get('IP'))
        x = datetime.datetime.now()
        gmp.create_target(name=result.get('IP') + "-" + x.strftime("%x-%X"), hosts=result.get('IP'))
        

#ix = index.open_dir("/home/data/Python/IP_Database")
#load_data = searcher()
#query = QueryParser("IP", load_data.schema) #.parse(".*.")
#results = searcher.search(query, limit=None)
#stored_fields = searcher.stored_fields("IP")
#print(str(stored_fields))
#writer = ix.writer()
#writer.update_document(path='/45.12.49.74', Scanned='False')
#writer.commit()



#with load_data.searcher() as searcher:
#    #query = QueryParser("IP", load_data.schema) #.parse(".*.")
#    results = searcher.search(query, limit=None)
#    for t in list(searcher.lexicon("IP")):
 #       print(t)
#        print(str(t).replace("b'", "").replace("'", ""))
#    for result in results:
#        print(result.get('IP'))
#        print(result.get('URL'))
#        print(result.get('page_title'))
#        print(result.get('date'))
#        print(result.get('time'))
#        print(result.get('Server'))
#        print(result.get('PHP'))

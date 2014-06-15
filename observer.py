
import time
import Queue

from datetime import datetime

from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS
from pymongo.errors import AutoReconnect

from server import server
from control import fail

work_queue = Queue.Queue()

def run_observer(config):
   """This function will attach to the configured mongo server's oplog and
      continually feed the queue with items that it needs to process"""

   try:
      tail_opts = { 'tailable': True, 'await_data': True }
      sleep = config.observer_sleep

      # connect to the target mongo server
      mongo_url = 'mongodb://%s:%s' % (config.mongo_host, config.mongo_port)
      db = MongoClient(mongo_url).local

      # get the latest timestamp in the database
      last_ts = db.oplog.rs.find().sort('$natural', -1)[0]['ts'];

      while True:
         # prepare the tail query and kick it off
         query = { 'ts': { '$gt': last_ts } }
         cursor = db.oplog.rs.find(query, **tail_opts)
         cursor.add_option(_QUERY_OPTIONS['oplog_replay'])

         try:
            while cursor.alive:
               try:
                  # grab a document if available
                  doc = cursor.next()
                  # send it to the queue
                  work_queue.put(doc)
               except StopIteration:
                  time.sleep(sleep)

               if not running:
                  try:
                     server.server_close()
                  finally:
                     sys.exit(0)
         finally:
            cursor.close()
   except:
      fail("Problem running the observer!")

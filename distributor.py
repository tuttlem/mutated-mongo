
import Queue

from observer import work_queue
from server import broadcast, clients
from control import fail, running

def run_distributor(config):
   """This function will continually process the queue looking for messages
      that connected clients are interested in. It will distribute these
      messages back to those clients when conditions meet"""
   try:
      while True:
         try:
            doc = work_queue.get(True, config.queue_block)
            ns = doc['ns']

            # determine the client list that will want to know
            # about this particular update
            if ns in clients:
               broadcast(clients[ns], doc, config)

         except Queue.Empty:
            pass

         if not running:
            sys.exit(0)
   except:
      fail("Distributor has failed")

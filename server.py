
import SocketServer

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads

from control import fail

server = None
clients = {}

class MutantRequestHandler(SocketServer.BaseRequestHandler):
   """
   The request handler for mutant clients
   """

   def handle(self):
      quit_requested = False
      self.data = None

      # persistent connection until the client requests that
      # they want out
      while not quit_requested:
         # read 1k
         self.data = self.request.recv(1024).strip()

         if (len(self.data) > 0):
            message = loads(self.data)

            if message['action'] == 'quit':
               quit_requested = True
            elif message['action'] == 'sub':
               add_client(message['ns'], message['q'], self.request)
         else:
            quit_requested = True


def run_server(config):
   """This is the server process that provides a front door for clients to
      connect. This function will handle client communications for protocol
      messages"""

   server = SocketServer.TCPServer(
      (config.server_host, config.server_port), MutantRequestHandler
   )

   try:
      server.serve_forever()

   except:
      fail("Server failed to run")

   finally:
      server.shutdown()

def broadcast(cs, doc, config):
   # connect to the target mongo server
   mongo_url = 'mongodb://%s:%s' % (config.mongo_host, config.mongo_port)
   db = MongoClient(mongo_url).local

   # prepare the message now (just once)
   message = {
      "op": doc["op"],
      "o": dumps(doc["o"])
   }

   removable = []

   # check every client identified for this namespace
   for client in cs:

      notify = False

      # if the client subscribed to this namespace without a query, they're
      # looking for any change at all, so - only go checking if a query
      # is present
      if client["query"] == None:
         notify = True
      else:
         # build a query that will test if the client
         # is actually interested in this change
         query = {
            "$and": [
               client["query"],
               { "h": doc["h"] }
            ]
         }

         notify = db.oplog.rs.find(query).count() > 0

      # only broadcast if the client is interested
      if notify:
         try:
            client['request'].send(dumps(message))
         except:
            removable.append(client)

   # clean up any dead-beats just stinkin' up the joint
   for client in removable:
      try:
         client['request'].close()
      finally:
         cs.remove(client)

def add_client(ns, q, req):
   """This function will add a new client to the list"""
   client = {
      'query': q,
      'request': req
   }

   if ns in clients:
      clients[ns].append(client)
   else:
      clients[ns] = [client]


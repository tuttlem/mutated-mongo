
import socket
import sys
import thread
from bson.objectid import ObjectId
from bson.json_util import dumps, loads

class MutatedReceiver:
   """Client communication handling to the mutated server"""

   def start(self, host, port):
      """Starts the persistent connection to the server"""
      self.up = True
      self.host = host
      self.port = port

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect((self.host, self.port))

      thread.start_new_thread(self.client_loop, ())

   def stop(self):
      """Stops the connection to the server"""

      message = {
         "action": "quit"
      }

      self.send_message(message)
      self.sock.close()

   def client_loop(self):
      """Internal client loop that keeps the connection alive"""

      while self.up:
         data = self.sock.recv(1024)

         if data == '':
            try:
               self.stop()
            finally:
               self.up = False
         else:
            self.handle_message(loads(data))

   def subscribe_to_query(self, ns, query):
      """Client wants to subscribe the a particular query"""

      message = {
         "action": "sub",
         "ns": ns,
         "q": query
      }

      self.send_message(message)

   def subscribe_to_id(self, ns, oid):
      """Client wants to subscribe to a particular record, identified by its id"""

      query = {
         "$or": [
            { "o._id": ObjectId(oid) },
            { "o2._id": ObjectId(oid) }
         ]
      }

      message = {
         "action": "sub",
         "ns": ns,
         "q": query
      }

      self.send_message(message)

   def subscribe_to_collection(self, ns):
      """Subscribes to any action performed on a record within a given collection"""

      message = {
         "action": "sub",
         "ns": ns,
         "q": None
      }

      self.send_message(message)

   def handle_message(self, message):
      pass

   def send_message(self, message):
      self.sock.sendall(dumps(message))

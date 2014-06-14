import time
from client import MutatedReceiver

class MyReceiver(MutatedReceiver):

   def handle_message(self, message):
      print 'Got: %s' % (str(message),)
      pass


receiver = MyReceiver()

try:
   receiver.start('localhost', 9994)
 #  receiver.subscribe_to_collection('people.employees')
   receiver.subscribe_to_id('people.employees', '539a8bd915fc69ef3f011722')

   while True:
      time.sleep(1000)

finally:
   receiver.stop()



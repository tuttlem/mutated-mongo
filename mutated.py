#!/usr/bin/env python

import thread
import time
import sys

from distributor import run_distributor
from server import run_server
from observer import run_observer

config = {
   'mongo_host': '192.168.56.101',
   'mongo_port': 27017,
   'observer_sleep': 1,
   'queue_block': 5,
   'server_host': '127.0.0.1',
   'server_port': 9994
}

def main():
    try:
        thread.start_new_thread(run_observer, (config,))
        thread.start_new_thread(run_distributor, (config,))
        thread.start_new_thread(run_server, (config,))
    except:
        print 'Error: Unable to start the processing threads'
        sys.exit(1)

    while True:
        time.sleep(10000)

if __name__ == '__main__':
   main()



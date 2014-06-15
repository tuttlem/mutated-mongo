#!/usr/bin/env python

import thread
import time
import sys
from optparse import OptionParser

from distributor import run_distributor
from server import run_server
from observer import run_observer

import control

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-m", "--host", dest="mongo_host",
                                      help="mongo host to listen to",
                                      default="localhost")

    parser.add_option("-p", "--port", dest="mongo_port",
                                      help="mongo port to listen on",
                                      default=27017)

    parser.add_option("-s", "--sleep", dest="observer_sleep",
                                       help="seconds the observer sleeps after exhausting all records from the cursor",
                                       default=1)

    parser.add_option("-b", "--block", dest="queue_block",
                                       help="seconds the distributor sleeps for after timeing out waiting for work",
                                       default=5)

    parser.add_option("-a", "--shost", dest="server_host",
                                         help="host address that this server will start on",
                                         default="localhost")

    parser.add_option("-n", "--sport", dest="server_port",
                                       help="host port that this server will start on",
                                       default=9994)

    (config, args) = parser.parse_args()

    try:
        observer_thread = thread.start_new_thread(run_observer, (config,))
        distributor_thread = thread.start_new_thread(run_distributor, (config,))
        server_thread = thread.start_new_thread(run_server, (config,))
    except:
        print 'Error: Unable to start the processing threads'
        sys.exit(1)

    while control.running == True:
        time.sleep(1)

if __name__ == '__main__':
   main()



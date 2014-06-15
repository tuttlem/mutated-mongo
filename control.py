
running = True

observer_thread = None
distributor_thread = None
server_thread = None

def fail(message):
    global running
    print 'Fail: %s' % (message, )
    print 'Global signal is now set to exit. Standby'

    running = False

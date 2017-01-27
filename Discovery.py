import logging
import threading
import signal
from DatabaseConnection import *

import sys, os
from random import randint
from RestService import *

'''Purpose is to automatically discover Fog devices through a client push system'''
class Discovery:


    #Threaded function
    def start_rest(db):
        rest = RestService(db)

    db = DatabaseConnection()
    threading.Thread(target=start_rest, args=(db,)).start()


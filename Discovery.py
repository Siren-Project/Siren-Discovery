import logging
import threading
from DatabaseConnection import *
from RestService import *


class Discovery:
    """Purpose is to automatically discover Fog devices through a client push system"""

    #Threaded function TODO add handler to kill this thread correctly on sigkil.
    def start_rest(db):
        rest = RestService(db)

    db = DatabaseConnection()
    threading.Thread(target=start_rest, args=(db,)).start()


from pymongo import MongoClient
from pprint import pprint
import json

'''Connects with mongoDB'''
class DatabaseConnection:

    def __init__(self):
        with open('config.json') as json_data:
            data = json.load(json_data)
            self.password = data['db_password']
            self.username = data['db_username']
            self.port = data['db_port']

        self.connection = MongoClient(host="127.0.0.1", port=self.port)
        self.siren_db = self.connection.siren
        if not self.password == "Null":
            self.siren_db.authenticate(self.username, self.password)
        self.nodes_table = self.siren_db.nodes
        print(type(self.nodes_table.find()))
        for node in self.nodes_table.find():
            pprint("Node :" + str(node))

        self.connection.close()

    def add_node(self, ip_addr):
        # Potential to add more fields here. Such as information gained from docker info.
        self.nodes_table.insert_one({'ip':ip_addr})

    def get_nodes(self):
        return self.nodes_table.find()

    def drop_nodes(self):
        self.nodes_table.drop()
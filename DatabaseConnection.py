from pymongo import MongoClient
from pprint import pprint
import json

'''Connects with mongoDB instance. See config.json for configuration'''


class DatabaseConnection:

    def __init__(self):
        with open('config.json') as json_data:
            data = json.load(json_data)
            self.password = data['db_password']
            self.username = data['db_username']
            self.port = data['db_port']
            self.host = data['host']

        self.connection = MongoClient(host=self.host, port=self.port)
        self.siren_db = self.connection.siren
        if not self.password == "Null" and not self.username == "Null":
            self.siren_db.authenticate(self.username, self.password)
        self.nodes_table = self.siren_db.nodes
        print(type(self.nodes_table.find()))
        for node in self.nodes_table.find():
            pprint("Node :" + str(node))

    def add_node(self, data):
        self.nodes_table.insert_one(data)

    def get_nodes(self):
        return self.nodes_table.find()

    def drop_nodes(self):
        self.nodes_table.drop()
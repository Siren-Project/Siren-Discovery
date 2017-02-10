from flask import Flask, url_for, request, Response
import json
import logging
from bson.json_util import dumps
from random import randint
import datetime


class RestService:
    """Hosts rest service for adding and retrieving devices and context"""
    app = Flask(__name__)
    db = None

    @app.route('/')
    def api_root():
        """Returns GitHub directory to help with docs."""
        return 'Read <a href="https://github.com/lyndon160/Siren-Discovery"> https://github.com/lyndon160/Siren-Discovery </a> for RESTful documentation'

    @app.route('/nodes', methods=['GET'])
    def api_nodes():
        """Returns all devices and context"""
        data = dumps(db.get_nodes())
        resp = Response(data)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return resp



    @app.route('/nodes/register_node', methods=['POST', 'GET'])
    def api_register_node():
        """Adds single new node to the database. This includes the nodes IP address"""
        logging.debug(request.json)
        # TODO add more checking for different fields
        if not request.json or 'ip' not in request.json:
            logging.warning("Missing information of provision %s", request.json)
            resp = Response("Error, did not include correct request information", status=400,
                            mimetype='application/json')
            return resp

        data = request.json
        data['time'] = datetime.datetime.now()
        data['remote_ip'] = request.remote_addr
        data['docker_port'] = 2375

        db.add_node(data)

        logging.info("Node added to db %s", data)
        resp = Response("Node added", status=200, mimetype='application/json')
        return resp

    @app.route('/reset_all', methods=['GET'])
    def api_reset_all():
        """Flushes all records in database"""
        db.drop_nodes()
        resp = Response(json.dumps("Database reset"))
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return resp

    def __init__(self, database):
        global db
        self.app.use_reloader = False
        db = database
        # self.app.debug = True
        self.app.run(host='0.0.0.0', port=61112, threaded=True)

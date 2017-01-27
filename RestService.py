from flask import Flask, url_for, request, Response
import json
import logging
from bson.json_util import dumps
from random import randint
class RestService:
    app = Flask(__name__)
    db = None
    @app.route('/')
    def api_root():
        return 'Read <a href="https://github.com/lyndon160/Siren-Discovery"> https://github.com/lyndon160/Siren-Discovery </a> for RESTful documentation'


    @app.route('/nodes', methods=['GET'])
    def api_nodes():
        data = dumps(db.get_nodes())
        resp = Response(data)
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return resp

    '''Adds single new node to the database. This includes the nodes IP address'''
    @app.route('/nodes/register_node', methods=['POST', 'GET'])
    def api_register_node():
        logging.info(request.json)
        if not request.json or 'ip' not in request.json:
            logging.warning("Missing information of provision %s", request.json)
            resp = Response("Error, did not include correct request information", status=400, mimetype='application/json')
            return resp
	# Removed because container cannot get host addr
	#        db.add_node(request.json['ip'])
	
	db.add_node(request.remote_addr)
	request.remote_addr

        logging.info("Node added to db %s",request.remote_addr)
        resp = Response("Node added", status=200, mimetype='application/json')
        return resp

    '''Flushes all records in database'''
    @app.route('/reset_all', methods=['GET'])
    def api_reset_all():
        db.drop_nodes()
        resp = Response(json.dumps("Database reset"))
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return resp

    def __init__(self, database):
        global db
        self.app.use_reloader=False
        db = database
        #self.app.debug = True
        self.app.run(host='0.0.0.0', port=61112, threaded=True)


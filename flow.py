from bottle import *

from neo4jrestclient import GraphDatabase
from models import Flow

db = GraphDatabase("http://localhost:7474/db/data/")


@route('/')
def front_page():
	flows = [rel.end for rel in db.nodes[0].relationships.outgoing(["Flow"])]
	return template('index', flows = flows)

@route('/start/:id')
def start(id):
	flow_start = [rel.end for rel in db.nodes[0].relationships.outgoing(["Flow"]) if rel.end['id'] == id]
	
	return flow_start[0]['description']
	
debug(True)
run(reloader = True)
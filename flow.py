from bottle import *

from neo4jrestclient import GraphDatabase
from models import Flow

db = GraphDatabase("http://localhost:7474/db/data/")


@route('/')
def front_page():
	flows = [rel.end for rel in db.nodes[0].relationships.outgoing(["Flow"])]
	return template('index', flows = flows)
	
	
debug(True)
run(reloader = True)
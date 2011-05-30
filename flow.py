from bottle import *

from neo4jrestclient import GraphDatabase
from models import Flow

db = GraphDatabase("http://localhost:7474/db/data/")

def find_flow(id):
	matching_flows = [rel.end for rel in db.nodes[0].relationships.outgoing(["Flow"]) if rel.end['id'] == id]
	
	if len(matching_flows) == 0:
		return None
		
	return matching_flows[0]
	
def find_question(flow_id, question_id):
	flow_start = [rel.end for rel in db.nodes[0].relationships.outgoing(["Flow"]) if rel.end['id'] == flow_id]
	
	if len(flow_start) == 0:
		return None
		
	flow_start = flow_start[0]
		
	questions = [rel.end for rel in flow_start.relationships.outgoing(['Question']) if rel.end.properties['id'] == question_id]
	
	
	if len(questions) == 0:
		return None
	
	return questions[0]

@route('/')
def front_page():
	flows = [rel.end for rel in db.nodes[0].relationships.outgoing(["Flow"])]
	return template('index', flows = flows)

@route('/start/:id')
def start(id):
	flow_start = find_flow(id)
	
	if not flow_start == None:
		questions = [rel.end.properties for rel in flow_start.relationships.outgoing(['Question'])]
		
		return template('questionnaire', questionnaire = flow_start, questions = questions)

@route('/flow/:flow_id/question/:question_id')
def question(flow_id, question_id):
	
	flow_start = find_flow(flow_id)
	
	if not flow_start == None:
		question = find_question(flow_id, question_id)
		
		if not question == None:
			answers = [answer.end.properties for answer in question.relationships.outgoing(['Answer'])]
			
			return template('question', flow = flow_start, question = question, answers = answers)
	
debug(True)
run(reloader = True)
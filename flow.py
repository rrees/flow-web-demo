from bottle import *

from finders import find_flow, find_question

from neo4jrestclient import GraphDatabase
db = GraphDatabase("http://localhost:7474/db/data/")

@route('/')
def front_page():
	flows = [rel.end for rel in db.nodes[0].relationships.outgoing(["Flow"])]
	return template('index', flows = flows)

@route('/flow/:id')
def flows(id):
	flow_start = find_flow(id)
	
	if flow_start == None:
		abort(404, 'That flow is unrecognised')

	questions = [rel.end.properties for rel in flow_start.relationships.outgoing(['Question'])]
		
	return template('questionnaire', questionnaire = flow_start, questions = questions)

@route('/flow/:flow_id/question/:question_id')
def question(flow_id, question_id):
	
	flow_start = find_flow(flow_id)
	
	if flow_start == None:
		abort(404, 'That flow is unrecognised')
	
	question = find_question(flow_id, question_id)
		
	if question == None:
		abort(404, 'That question is unrecognised')

	answers = [answer.end.properties for answer in question.relationships.outgoing(['Answer'])]
	
	return template('question', flow = flow_start, question = question, answers = answers)
			
@route('/start/flow/:flow_id')
def start(flow_id):
	from uuid import uuid4
	flow_start = find_flow(flow_id)
	
	if flow_start == None:
		abort(404, 'That flow is unrecognised')
		
	first_question = [rel.end for rel in flow_start.relationships.outgoing(['First'])]
	
	if len(first_question) == 0:
		abort(404, 'The flow has no first question identified')
		
	first_question = first_question[0]
	
	character_id = uuid4().hex
	new_character = db.nodes.create(id = character_id)
	
	flow_start.relationships.create("Character", new_character)
	
	new_character.relationships.create("Current", first_question)
	
	if not 'characters' in db.nodes.indexes:
		db.nodes.indexes.create('characters')
		
	db.nodes.indexes.get('characters').add('id', character_id, new_character)
	
	redirect('/character/%s' % character_id)
	
@route('/character/:character_id')
def show_character(character_id):
	
	character = db.nodes.indexes.get('characters')['id'][character_id].pop()
	
	return template('character', character = character.properties)
	
debug(True)
run(reloader = True)
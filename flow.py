from bottle import *

import finders

from neo4jrestclient import GraphDatabase
db = GraphDatabase("http://localhost:7474/db/data/")

@route('/')
def front_page():
	flows = db.nodes.indexes.get('flows')['flow']['start'][:]
	print flows
	return template('index', flows = flows)

@route('/flow/:id')
def flows(id):
	flow_start = finders.find_flow(id)
	
	if flow_start == None:
		abort(404, 'That flow is unrecognised')

	questions = [rel.end.properties for rel in flow_start.relationships.outgoing(['Question'])]
		
	return template('questionnaire', questionnaire = flow_start, questions = questions)

@route('/flow/:flow_id/question/:question_id')
def question(flow_id, question_id):
	def next_question(answer):
		decorated_answer = answer.properties
		decorated_answer['next'] = answer.relationships.outgoing(['Next'])[0].end.properties
		return decorated_answer
	
	flow_start = finders.find_flow(flow_id)
	
	if flow_start == None:
		abort(404, 'That flow is unrecognised')
	
	question = finders.find_question(flow_id, question_id)
		
	if question == None:
		abort(404, 'That question is unrecognised')

	answers = [answer.end for answer in question.relationships.outgoing(['Answer'])]
	
	answers = [answer.properties if not answer.relationships.outgoing(['Next']) else next_question(answer) for answer in answers]
	
	return template('question', flow = flow_start, question = question, answers = answers)

@route('/flow/:flow_id/question/:question_id/answer/:answer_id')
def answer(flow_id, question_id, answer_id):

	flow_start = finders.find_flow(flow_id)

	if flow_start == None:
		abort(404, 'That flow is unrecognised')

	question = finders.find_question(flow_id, question_id)

	if question == None:
		abort(404, 'That question is unrecognised')

	answers = [answer.end for answer in question.relationships.outgoing(['Answer']) if answer.end.properties['id'] == answer_id]
	
	if not len(answers) == 1:
		abort(404, 'Answer not found')

	answer = answers[0]
	
	next_questions = answer.relationships.outgoing(['Next'])
	
	if not next_questions:
		return template('conclusion')
	
	next_question_id = next_questions[0].end['id']
	
	return redirect('/flow/%s/question/%s' % (flow_id, next_question_id))

@route('/conclusion')
def conclusion():
	return template('conclusion')
	
@route('/start/flow/:flow_id')
def start(flow_id):
	from uuid import uuid4
	flow_start = finders.find_flow(flow_id)
	
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
	
@get('/character/:character_id')
def show_character(character_id):
	
	character = db.nodes.indexes.get('characters')['id'][character_id].pop()
	
	current_question = character.relationships.outgoing(['Current'])

	if len(current_question) == 0:
		attributes = character.relationships.outgoing(['Attribute'])
		return template('character', character = character.properties)
	
	current_question = finders.current_question(character)
	answers = current_question.relationships.outgoing(['Answer'])
	return template('character_question.tpl', character = character.properties, current_question = current_question.properties, answers = [answer.end.properties for answer in answers])

@post('/character/:character_id')
def record_answer(character_id):
	given_answer = request.params['answer']
	character = finders.find_character(character_id)
	current_question = finders.current_question(character)
	answers = [answer.end for answer in current_question.relationships.outgoing(['Answer'])]
	for answer in answers:
		if answer.properties['id'] == given_answer:
			for reward_rel in answer.relationships.outgoing(['Reward']):
				reward = reward_rel.end
				character.relationships.create("Attribute", reward)

			character.relationships.outgoing(['Current']).pop().delete()
			for next_question_rel in answer.relationships.outgoing(['Next']):
				next_question = next_question_rel.end
				character.relationships	.create('Current', next_question)
				print "Next", next_question
	redirect('/character/%s' % character_id)

debug(True)
run(reloader = True, port = 2222)
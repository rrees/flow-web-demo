from neo4jrestclient import GraphDatabase
from models import Flow, Question, Answer

flows = [Flow('morrowind', "Morrowind-style", "A fantasy character creation process like the one at the start of the game Morrowind.")]

def morrowind_flow(start_node):
	flow_id = 'morrowind'
	question_index = db.nodes.indexes.get('questions')
	
	q1 = Question(id = 'q1', text = 'What surrounded you when you were young?',
		answers = [Answer(id = 'q1a1', text = 'The sea', reward_type = 'Background', reward_value = 'Coastal', next='q4'),
			Answer(id = 'q1a2', text = 'Fields', reward_type = 'Background', reward_value = 'Rural', next = 'q2'),
			Answer(id = 'q1a3', text = 'Buildings', reward_type = 'Background', reward_value = 'Urban', next = 'q2'),
			Answer(id = 'q1a4', text = 'Trees', reward_type = 'Background', reward_value = 'Backwoods', next = 'q2'),])
	
	q2 = Question(id = 'q2', text = 'When you were young your family home caught fire. You could hear your mother crying for help inside. How did you save her?',
		answers = [Answer(id = 'q2a1', text = "I seized an axe and cut through the wall of the house, creating an escape route.", reward_type = 'Body', reward_value = '+1', next = 'q3'),
			Answer(id = 'q2a2', text ='I gathered up a rope and covered my mouth with a damp cloth. I made my way through the smoke and followed the rope back to safety.', reward_type = 'Mind', reward_value = '+1', next = 'q3'),
			Answer(id = 'q2a3', text = 'I charged into the house immediately and found her. We made it out together.', reward_type = 'Spirit', reward_value = '+1', next = 'q3')])
	
	q3 = Question(id = 'q3', text = 'You won a prize at your county fair. What was is it that won you this accolade?',
		answers = [Answer(id = 'q3a1', text = 'My skills in archery.', reward_type = 'Skill', reward_value = 'Archery'),
			Answer(id = 'q3a2', text = 'I was a fearless bull leaper.', reward_type = 'Skill', reward_value = 'Acrobatics'),
			Answer(id = 'q3a3', text = 'My horsemanship.', reward_type = 'Skill', reward_value = 'Riding')])
	
	q4 = Question(id = 'q4', text = 'Did you have your own boat?',
		answers = [Answer(id = 'q4a1', text ="No, the sea terrified me.", reward_type = "Trait", reward_value = "Cautious", next = 'q2'),
			Answer(id = 'q4a2', text = "No, I helped crew my father's boat.", reward_type = "Trait", reward_value = "Salty dog", next = 'q2'),
			Answer(id = 'q4a3', text ="Yes, I would sail her whenever I could.", reward_type = "Skill", reward_value = "Sailor", next = 'q2')])
		
	questions = [q1, q2, q3, q4,]
	
	current_questions = start_node.relationships.outgoing(['Question'])
	
	for question in questions:
		if not question.id in [q.end.properties['id'] for q in current_questions]:
			new_question = db.nodes.create(id = question.id, text = question.text)
			start_node.relationships.create('Question', new_question)
			question_index[flow_id][question.id] = new_question
	
	
	for question in questions:
			question_node = question_index[flow_id][question.id][0]
			for answer in question.answers:
				answer_node = db.nodes.create(id = answer.id, text = answer.text)
				reward_node = db.nodes.create(type = answer.reward_type, value = answer.reward_value)
				answer_node.relationships.create('Reward', reward_node)
				question_node.relationships.create('Answer', answer_node)
				
				if answer.next and question_index[flow_id][answer.next]:
					answer_node.relationships.create('Next', question_index[flow_id][answer.next][0])
		
		
	if len(start_node.relationships.outgoing(['First'])) == 0:
		first_question = [question.end for question in start_node.relationships.outgoing(['Question']) if question.end.properties['id'] == 'q1'][0]
		start_node.relationships.create('First', first_question)
	

db = GraphDatabase("http://localhost:7474/db/data/")

for index_name in ['flows', 'questions']:
	if not index_name in db.nodes.indexes.keys():
		db.nodes.indexes.create(index_name)
		print 'Created index %s' % index_name

for flow in flows:
	flow_index = db.nodes.indexes.get("flows")
	if not flow_index['flow']['start']:
		new_flow_node = db.nodes.create(id = flow.id, title = flow.title, description = flow.description)
		flow_index['flow']['start'] = new_flow_node
		print "Created flow %s" % flow.title
		
morrowind_flow([node for node in db.nodes.indexes.get("flows")['flow']['start'] if node['id'] == "morrowind"][0])

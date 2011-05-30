from neo4jrestclient import GraphDatabase

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


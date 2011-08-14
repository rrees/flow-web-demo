from neo4jrestclient import GraphDatabase

db = GraphDatabase("http://localhost:7474/db/data/")

def find_flow(id):
	matching_flows = [node for node in db.nodes.indexes.get('flows')['flow']['start'][:] if node['id'] == id]
	
	if len(matching_flows) == 0:
		return None
		
	return matching_flows[0]
	
def find_question(flow_id, question_id):
	flow_start = find_flow(flow_id)
	
	if not flow_start:
		return None
		
	questions = [rel.end for rel in flow_start.relationships.outgoing(['Question']) if rel.end.properties['id'] == question_id]
	
	if len(questions) == 0:
		return None
	
	return questions[0]


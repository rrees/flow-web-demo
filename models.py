class Flow:
	def __init__(self, id, title, description):
		self.id = id
		self.title = title
		self.description = description

class Question:
	def __init__(self, id, text, answers):
		self.id = id
		self.text = text
		self.answers = answers
		
class Answer:
	def __init__(self, id, text, reward_type, reward_value, next = None):
		self.id = id
		self.text = text
		self.reward_type = reward_type
		self.reward_value = reward_value
		self.next = next

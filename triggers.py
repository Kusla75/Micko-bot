import json

triggers = []
cooldown = 360

class Trigger:
	def __init__(self, words, response, epoch_t, count, max_count):
		self.words = words
		self.response = response
		self.epoch_t = epoch_t
		self.count = count
		self.max_count = max_count

	def restart_count(self):
		self.count = self.max_count

# Loading trigger strings from json file
with open('data/triggers.json', 'r') as f:
	json_file = json.load(f)

	for elem in json_file:
		triggers.append(Trigger(
			elem["words"], 
			elem["response"],
			0, 
			elem["max_count"],
			elem["max_count"]
			))

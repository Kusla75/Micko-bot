import json
import os

triggers = []

class Trigger:
	def __init__(self, words, response, count, max_count):
		self.words = words
		self.response = response
		self.count = count
		self.max_count = max_count

with open('data/triggers.json', 'r') as f:
	json_file = json.load(f)

	for elem in json_file:
		triggers.append(Trigger(
			elem["words"], 
			elem["response"], 
			elem["max_count"],
			elem["max_count"]
			))

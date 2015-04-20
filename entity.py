"""
Represents a single instance of an Entity for some Mention
entity_id is the wikipedia id of this entity
prior_prob is the probability that this Entity is linked from its' Mention
	in wikipedia
score can be used to set a score for how good this entity matches
"""
class Entity(object):
	def __init__(self, entity_id, prior_prob, score = 0):
		self.entity_id = entity_id
		self.prior_prob = prior_prob
		self.score = score

	def __str__(self):
		return str(self.entity_id)
"""
Represents a mention, i.e. an interesting substring of a query
link_prob is the probability of the substring being a link in wikipedia
candidate_entities is a list of entities which could potentially be linked to this substring
"""
class Mention(object):
	def __init__(self, substring, link_prob, candidate_entities=[]):
		self.substring = substring
		self.link_prob = link_prob
		self.candidate_entities = candidate_entities
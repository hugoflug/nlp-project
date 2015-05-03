"""
Represents a mention, i.e. an interesting substring of a query
link_prob is the probability of the substring being a link in wikipedia
candidate_entities is a list of entities which could potentially be linked to this substring
"""
class Mention(object):
    def __init__(self, substring, link_prob=1, candidate_entities=[]):
        self.substring = substring
        self.link_prob = link_prob
        self.candidate_entities = candidate_entities

    def __str__(self):
        return self.substring
    def __repr__(self):
        return str(self)

    def equalsRelaxed(self, other):
        return type(other) is Mention and \
            len(other.candidate_entities) == 1 and len(self.candidate_entities) == 1 and \
            other.candidate_entities[0] == self.candidate_entities[0]

    def equalsStrict(self, other):
        return type(other) is Mention and \
            len(other.candidate_entities) == 1 and len(self.candidate_entities) == 1 and \
            other.candidate_entities[0] == self.candidate_entities[0] and \
            other.substring == self.substring
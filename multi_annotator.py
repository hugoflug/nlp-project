from entity import Entity
from mention import Mention
import copy

class MultiAnnotator(object):

    """ Uses multiple annotators to annotate mentions """

    def __init__(self, weights, *annotators):
        self.annotators = annotators
        if weights is None:
            weights = [1/len(annotators)]*len(annotators)
        self.weights = weights

    def annotate(self, mentions):

        """ Weights each prior for each mention using self.weights """

        for m in mentions:
            m.candidate_entities = []

        empty_mentions = copy.deepcopy(mentions)

        for i in range(len(self.annotators)):
            mentions_ = copy.deepcopy(empty_mentions)

            # Annotate all mentions using this annotator
            self.annotators[i].annotate(mentions_)

            # Multiply prior_probs with weight
            for m in mentions_:
                for c in m.candidate_entities:
                    c.prior_prob *= self.weights[i]

            # Add candidates to original mentions object, and check for duplicates
            for mention in mentions:

                print(mention.substring)
                mention_ = [m for m in mentions_ if m.substring == mention.substring]
                if(len(mention_) > 0): # If any entities were found, otherwise the mention is removed
                    mention_ = mention_[0]
                    
                    for c in mention_.candidate_entities:

                        # If duplicate, just add on to prior_prob
                        if(c in mention.candidate_entities):
                            c2 = next(x for x in mention.candidate_entities if x == c)
                            c.prior_prob += c2.prior_prob
                        else:
                            # Else just add the new candidate
                            mention.candidate_entities.append(c)

        to_remove = []
        for mention in mentions:
            if not mention.candidate_entities:
                # Remove mentions where no annotator found any candidates
                to_remove.append(mention)
            else:
                # If any annotator did not find any candidates for a mention, we need to renormalize
                Z = sum([c.prior_prob for c in mention.candidate_entities])
                for c in mention.candidate_entities:
                    c.prior_prob /= Z

        for obj in to_remove:
            mentions.remove(obj)

class DumpAnnotator(object):

    def annotate(self, mentions):
        for m in mentions:
            m.candidate_entities = [Entity(m.substring, 1.0)]

class NoAnnotator(object):

    def annotate(self, mentions):
        """ """


def test_multi_annotator():

    mentions = [Mention("apple"), Mention("iphone")]
    annotator = MultiAnnotator(None, DumpAnnotator(), NoAnnotator())

    annotator.annotate(mentions)

    return mentions

if __name__ == "__main__":
    test_multi_annotator()
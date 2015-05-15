
class CandidateScorer(object):
    """ Score the entity candidates for each mention and chose the ones that score the best"""

    """ Initializes the candidate scorer with link probabilities (dict) and a similarity function"""
    def __init__(self, sim, epsilon = 0.1):

        self.sim = sim
        self.scores = {}
        self.epsilon = epsilon

    def score_candidates(self, mentions):
        """
        Takes a list of Mention objects and sets the 'score' attribute of all candidate entities of each Mention
        """

        for m in mentions: #loop over mentions
            for c in m.candidate_entities: # loop over candidates for each mention
                score = 0

                for m2 in mentions: # loop over all other mentions
                    if m2 == m: continue
                    
                    vote = 0
                    
                    # Compute support/vote from this mention's candidates
                    for c2 in m2.candidate_entities:
                        vote += self.sim(c.entity_id, c2.entity_id)*c2.prior_prob
                    vote /= len(m2.candidate_entities)

                    score += vote

                c.score = score

    def choose_candidates(self, mentions):
        """
        Takes a list of Mention objects and reduces the candidate_entities list to only one entity -- the best one
        """

        for m in mentions: #loop over mentions

            # Choose among the candidates for the mention
            max_score = max(m.candidate_entities, key=lambda c: c.score).score
            m.candidate_entities = filter(lambda c: max_score < c.score + self.epsilon, m.candidate_entities)
            m.candidate_entities = [max(m.candidate_entities, key=lambda c: c.prior_prob)]
        
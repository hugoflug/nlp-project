
class candidate_scorer(object):
    """ Score the entity candidates for each mention and chose the ones that score the best"""

    """ Initializes the candidate scorer with link probabilities (dict) and a similarity function"""
    def __init__(self, sim):

        self.sim = sim

    def score_candidates(self, candidates):

        # Replaces the link probabilities with the scores

        for m in candidates: #loop over mentions
            for c in m[1]: # loop over candidates for each mention
                score = 0

                for m2 in candidates: # loop over all other mentions
                    if(m2 == m): continue
                    
                    vote = 0
                    
                    # Compute support/vote from this mention's candidates
                    for c2 in m2[1]:
                        vote += sim(c[0], c2[0])*c2[1]
                    vote /= len(m2[1])

                    score += vote

                # Set score
                c[1] = score


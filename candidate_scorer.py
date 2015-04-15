
class candidate_scorer(object):
    """ Score the entity candidates for each mention and chose the ones that score the best"""

    """ Initializes the candidate scorer with link probabilities (dict) and a similarity function"""
    def __init__(self, sim):

        self.sim = sim

    def score_candidates(self, candidates):

        for m in candidates: #loop over mentions
            for c in m[1]: # loop over candidates for each mention
                score = 0

                for m2 in candidates: # loop over all other mentions
                    if(m2 == m): continue
                    
                    vote = 0
                    
                    # Compute support/vote from this mention's candidates
                    for c2 in m2[1]:
                        vote += self.sim(c[0], c2[0])*c2[1]
                    vote /= len(m2[1])

                    score += vote

                # Set score
                c.append(score)

    def choose_candidates(self, candidates, epsilon = 0.2):

        for m in candidates: #loop over mentions

            # Choose among the candidates for the mention
            max_score = max(m[1], key=lambda c: c[2])[2]
            m[1] = filter(lambda c: max_score < c[2] + epsilon, m[1])
            m[1] = max(m[1], key=lambda c: c[1])
        
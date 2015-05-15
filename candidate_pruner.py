

class CandidatePruner(object):

    def __init__(self, theta = 0):
        self.theta = theta

    def prune(self, linked_mentions, sim):
        """Prunes entities that should be considered as general conceps rather than entities.
           Takes a list of Mention objects and prunes it.
           The first element in the candidate_entities list is counted as the chosen candidate.
           The rest of the list is ignored"""
        if len(linked_mentions) <= 1: return

        mentions = linked_mentions[:]
       
        for m in mentions:

            coherence = 0
            for m2 in mentions:
                if m2 == m: continue
                coherence += sim(m.candidate_entities[0].entity_id, m2.candidate_entities[0].entity_id)

            coherence /= len(mentions) -1

            if coherence + m.link_prob/2 < self.theta:
                linked_mentions.remove(m)


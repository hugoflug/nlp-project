

class CandidatePruner(object):
    """Pruns entities that should be considered as general conceps rather than entities"""

    def prune(self, linked_mentions, theta, sim):
        if(len(linked_mentions) <= 1): return

        mentions = linked_mentions[:]
       
        for m in mentions:

            coherence = 0
            for m2 in mentions:
                if(m2 == m): continue
                coherence += sim(m[1][0], m2[1][0])

            coherence /= len(mentions) -1

            if(coherence + m[1][1]/2 < theta):
                linked_mentions.remove(m)


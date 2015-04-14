

class lp_annotator(object):
    """Uses a dictionary of link probabilities to come up with candidates to mentions"""

    def __init__(self, link_probs):
        self.link_probs = link_probs

    def annotate(self, mentions):
        annotations = []
        for m in mentions:
            if(m in self.link_probs):
                annotations.append((m, self.link_probs[m]))

        return annotations

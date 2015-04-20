

class LinkProbabilityAnnotator(object):
    """Uses a dictionary of link probabilities to come up with candidates to mentions"""

    def __init__(self):
        self.link_probs = self.get_link_probs("crosswikis-dict-preprocessed-2")

    def get_link_probs(self, path):
        file = open(path, encoding="utf8")
        link_probs = {}
        for line in file:
            match = line.strip("\n").split("\t")
            words = match[0].lower()
            rest = match[1].split(" ")
            prob = float(rest[0])
            entity = rest[1]
            if not words in link_probs:
                link_probs[words] = []
            link_probs[words].append([entity, prob])
        return link_probs

    def annotate(self, mentions):
        annotations = []
        for m in mentions:
            if(m in self.link_probs):
                annotations.append([m, self.link_probs[m]])

        # Prune so there is no overlappings
        annotations_copy = annotations[:]
        for m in annotations_copy:
            for m2 in annotations_copy:
                if(m == m2): continue
                if(m[0] in m2[0] and m2[1] > m[1]): # if another is overlapping that has higher lp, remove this
                    annotations.remove(m)

        return annotations

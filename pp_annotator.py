

class PriorProbabilityAnnotator(object):
    """Uses a dictionary of link probabilities to come up with candidates to mentions"""

    def __init__(self):
        self.prior_probs = self.get_prior_probs("crosswikis-dict-preprocessed-2")

    def get_prior_probs(self, path):
        file = open(path, encoding="utf8")
        prior_probs = {}
        for line in file:
            match = line.strip("\n").split("\t")
            words = match[0].lower()
            rest = match[1].split(" ")
            prob = float(rest[0])
            entity = rest[1]
            if not words in prior_probs:
                prior_probs[words] = []
            prior_probs[words].append([entity, prob])
        return prior_probs

    def annotate(self, mentions):
        annotations = []
        for m in mentions:
            if m in self.prior_probs:
                annotations.append([m, self.prior_probs[m]])

        return annotations

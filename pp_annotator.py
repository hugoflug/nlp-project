from entity import Entity

class PriorProbabilityAnnotator(object):
    """Uses a dictionary of prior probabilities to come up with candidates to mentions
       Prior probability: The probability that a link with a given substring in wikipedia
       links to a certain entity"""

    def __init__(self):
        self.prior_probs = self.get_prior_probs("crosswiki-corrected-entities")

    def get_prior_probs(self, path):
        file = open(path, encoding="utf8")
        prior_probs = {}
        for line in file:
            match = line.strip("\n").split("\t")
            words = match[0].lower()
            rest = match[1].split(" ")
            prob = float(rest[1])

            if prob < 0.01:
                continue

            entity = rest[0]
            if not words in prior_probs:
                prior_probs[words] = []
            prior_probs[words].append(Entity(entity, float(prob)))
        return prior_probs

    def annotate(self, mentions):
        """
        takes a list of Mention objects, fills in their candidate_entities list
        with candidates
        """
        to_remove = []

        for mention in mentions:
            if mention.substring in self.prior_probs:
                mention.candidate_entities = self.prior_probs[mention.substring]
            else:
                to_remove.append(mention)

        for obj in to_remove:
            mentions.remove(obj)
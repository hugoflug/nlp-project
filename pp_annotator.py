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

            if prob < 0.01: #and words in prior_probs:
                continue

            entity = rest[0]
            if not words in prior_probs:
                prior_probs[words] = []
            prior_probs[words].append(Entity(entity, float(prob)))

        # if we only have one candidate and it has prior probability 0,
        # set the prior probability to 1 instead
        #for entity_list in prior_probs.values():
        #    if len(entity_list) == 1 and entity_list[0].prior_prob == 0.0:
        #        entity_list[0].prior_prob = 1

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

                # Normalize pp to 1.0
                s = sum([c.prior_prob for c in mention.candidate_entities])
                if s > 0:
                    for c in mention.candidate_entities:
                        c.prior_prob /= s
            else:
                to_remove.append(mention)

        for obj in to_remove:
            mentions.remove(obj)
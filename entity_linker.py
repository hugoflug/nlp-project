
from ngram_mention_extractor import ngram_mention_extractor
from pp_annotator import PriorProbabilityAnnotator
from multi_annotator import MultiAnnotator
from wiki_annotator import WikipediaAnnotator
from bing_annotator import BingAnnotator
from candidate_scorer import CandidateScorer
from tagme_similarity import TagMeSimilarity
from candidate_pruner import CandidatePruner
from tagme_spotter import TagMeSpotter
from wiki_annotator import WikipediaAnnotator
from multi_annotator import MultiAnnotator

def main():
    print("loading link probabilities...")
    sim = TagMeSimilarity()
    entity_linker = EntityLinker(similarity=sim)

    while True:

        print("enter query: ")
        query = input().strip()

        # Annotate
        entity_linker.annotate(query, True)


class EntityLinker(object):

    def __init__(self, spotter = TagMeSpotter(), \
                     annotator = MultiAnnotator(None, PriorProbabilityAnnotator(), WikipediaAnnotator(), BingAnnotator()), \
                     similarity = TagMeSimilarity(), \
                     scorer = None, \
                     pruner = CandidatePruner() ):

        self.spotter = spotter
        self.annotator = annotator
        self.similarity = similarity
        self.scorer = scorer if not scorer is None else CandidateScorer(similarity.sim)
        self.pruner = pruner

    def annotate(self, query, debug = False):

        query = query.lower()

        # Step 1: Find mentions
        mentions = self.spotter.spot(query)

        # Step 2: Find candidates for the mentions (annotate the mentions)
        self.annotator.annotate(mentions)

        if debug:
            print("\n ---- CANDIDATES FOR ALL MENTIONS -----\n")
            self.print_candidates(mentions)

        # Step 3: Choose the best candidates
        self.similarity.load_similarities(self.get_all_entities(mentions))

        self.scorer.score_candidates(mentions)
        self.scorer.choose_candidates(mentions)

        if debug:
            print(" ---- THE BEST CANDIDATES ------------\n")
            self.print_candidates(mentions)

        # Step 4: Prune
        self.pruner.prune(mentions, 0.1, self.similarity.sim)

        if debug:
            print(" ---- AFTER PRUNING ENTITIES --------\n")
            self.print_candidates(mentions)

        #dict = {}
        #for m in mentions:
        #    dict[m.substring] = m.candidate_entities[0].entity_id

        return mentions

    def get_all_entities(self, mentions):
        all_entities = []
        for m in mentions:
            all_entities.extend(m.candidate_entities)
        return all_entities

    def print_candidates(self, mentions):
        for m in mentions:
            print(m.substring + ":")
            for c in m.candidate_entities:
                print(str(c) + " - " + str(c.prior_prob))
            print()


if __name__ == "__main__":
    main()

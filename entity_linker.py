
from ngram_mention_extractor import ngram_mention_extractor
from pp_annotator import PriorProbabilityAnnotator
from candidate_scorer import CandidateScorer
from tagme_similarity import TagMeSimilarity
from candidate_pruner import CandidatePruner
from tagme_spotter import TagMeSpotter

def main():
    print("loading link probabilities...")
    annotator = PriorProbabilityAnnotator()

    while True:

        print("enter query: ")
        query = input().strip()

        # Annotate
        annotate(query, annotator, True)


def annotate(query, annotator = PriorProbabilityAnnotator(), debug = False):

    # Step 1: Find mentions
    tagme_spotter = TagMeSpotter()
    mentions = tagme_spotter.spot(query)

    # Step 2: Find candidates for the mentions (annotate the mentions)
    annotator.annotate(mentions)

    if debug:
        print("\n ---- CANDIDATES FOR ALL MENTIONS -----\n")
        print_candidates(mentions)

    # Step 3: Choose the best candidates
    similarity = TagMeSimilarity()

    similarity.load_similarities(get_all_entities(mentions))

    scorer = CandidateScorer(similarity.sim)
    scorer.score_candidates(mentions)
    scorer.choose_candidates(mentions)

    if debug:
        print(" ---- THE BEST CANDIDATES ------------\n")
        print_candidates(mentions)

    # Step 4: Prune
    pruner = CandidatePruner()
    pruner.prune(mentions, 0.1, similarity.sim)

    if debug:
        print(" ---- AFTER PRUNING ENTITIES --------\n")
        print_candidates(mentions)

    dict = {}
    for m in mentions:
        dict[m.substring] = m.candidate_entities[0].entity_id

    return dict

def get_all_entities(mentions):
    all_entities = []
    for m in mentions:
        all_entities.extend(m.candidate_entities)
    return all_entities

def print_candidates(mentions):
    for m in mentions:
        print(m.substring + ":")
        for c in m.candidate_entities:
            print(str(c))
        print()


if __name__ == "__main__":
    main()


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
    candidates = annotator.annotate(mentions)

    if debug:
        print("\n ---- CANDIDATES FOR ALL MENTIONS -----\n")
        print_candidates(candidates)

    # Step 3: Choose the best candidates
    similarity = TagMeSimilarity()
    similarity.load_similarities(get_all_entities(candidates))

    scorer = CandidateScorer(similarity.sim)
    scorer.score_candidates(candidates)
    scorer.choose_candidates(candidates)

    if debug:
        print(" ---- THE BEST CANDIDATES ------------\n")
        print_candidates(candidates)

    # Step 4: Prune
    pruner = CandidatePruner()
    pruner.prune(candidates, 0.3, similarity.sim)

    if debug:
        print(" ---- AFTER PRUNING ENTITIES --------\n")
        print_candidates(candidates)

    dict = {}
    for m in candidates:
        dict[m[0]] = m[1][0]

    return dict

def print_candidates(candidates):

    for c in candidates:
        print(c[0])
        print(str(c[1]) + "\n")

def get_all_entities(candidates):
    entities = []
    for m in candidates: # mentions
        for e in m[1]:
            entities.append(e[0])
    return entities

if __name__ == "__main__":
    main()

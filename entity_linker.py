
from ngram_mention_extractor import ngram_mention_extractor
from lp_annotator import lp_annotator
from candidate_scorer import candidate_scorer
from tagme_similarity import tagme_similarity
from candidate_pruner import candidate_pruner

def main():

    print("loading link probabilities...")
    annotator = lp_annotator()

    while True:

        print("enter query: ")
        query = input().strip()

        # Annotate
        annotate(query, annotator)


def annotate(query, annotator = lp_annotator()):

    # Step 1: Find mentions
    mention_extractor = ngram_mention_extractor()
    mentions = mention_extractor.get_mentions(query)

    # Step 2: Find candidates for the mentions (annotate the mentions)
    candidates = annotator.annotate(mentions)

    print("\n ---- CANDIDATES FOR ALL MENTIONS -----\n")
    print_candidates(candidates)

    # Step 3: Choose the best candidates
    similarity = tagme_similarity()
    similarity.load_similarities(get_all_entities(candidates))

    scorer = candidate_scorer(similarity.sim)
    scorer.score_candidates(candidates)
    scorer.choose_candidates(candidates)

    print(" ---- THE BEST CANDIDATES ------------\n")
    print_candidates(candidates)

    # Step 4: Prune
    pruner = candidate_pruner()
    pruner.prune(candidates, 0.3, similarity.sim)

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

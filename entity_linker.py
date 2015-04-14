
from ngram_mention_extractor import ngram_mention_extractor
from lp_annotator import lp_annotator
from candidate_scorer import candidate_scorer
from tagme_similarity import tagme_similarity

def main():

    print("enter query: ")
    query = input().strip()
    
    # Step 1: Find mentions
    mention_extractor = ngram_mention_extractor()
    mentions = mention_extractor.get_mentions(query)

    # Step 2: Find candidates for the mentions (annotate the mentions)
    annotator = lp_annotator()
    candidates = annotator.annotate(mentions)

    print_candidates(candidates)

    # Step 3: Choose the best candidates
    similarity = tagme_similarity()
    similarity.load_similarities(get_all_entities(candidates))

    scorer = candidate_scorer(similarity.sim)
    scorer.score_candidates(candidates)

    print_candidates(candidates)

    # Step 4: Prune

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

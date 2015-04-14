
from ngram_mention_extractor import ngram_mention_extractor
from lp_annotator import lp_annotator

def main():

    # Load lp
    lp = get_link_probs("crosswikis-dict-preprocessed-2")

    print("enter query: ")
    query = input().strip()
    
    # Step 1: Find mentions
    mention_extractor = ngram_mention_extractor()
    mentions = mention_extractor.get_mentions(query)

    # Step 2: Find candidates for the mentions (annotate the mentions)
    annotator = lp_annotator(lp)
    candidates = annotator.annotate(mentions)

    print_candidates(candidates)

    # Step 3: Choose the best candidates


    # Step 4: Prune


def get_link_probs(path):
    file = open(path, encoding="utf-8")
    link_probs = {}
    for line in file:
        match = line.strip("\n").split("\t")
        words = match[0].lower()
        rest = match[1].split(" ")
        prob = float(rest[0])
        entity = rest[1]
        if not words in link_probs:
            link_probs[words] = []
        link_probs[words].append((entity, prob))
    return link_probs

def print_candidates(candidates):

    for c in candidates:
        print(c[0])
        print(str(c[1]) + "\n")

if __name__ == "__main__":
    main()


from ngram_mention_extractor import *

def main():

    print("enter query: ")
    query = input().strip()
    
    # Step 1: Find candidate mentions
    mention_extractor = ngram_mention_extractor()
    candidates = mention_extractor.get_mentions(query)

    # Step 2: Score all candidates
    print(candidates)

    # Step 3: Predict the best candidates

    # Step 4: Prune




if __name__ == "__main__":
    main()

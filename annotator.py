from mention import Mention
from entity import Entity

def main():
    #file not in git repo due to GitHub size restrictions
    dict_file = open("crosswikis-dict-preprocessed-2", encoding="utf-8")
    annotator = Annotator(dict_file)

    print("enter query: ")

    query = raw_input().strip()

    annotations = annotator.annotate(query)

    for key, value in annotations.items():
        print("{} -- {} ({})".format(key, value))

class Annotator:
    def __init__(self, lp_file):
        """
        'lp_file' is a file with link probabilities 
        """
        self.link_probs = self.get_link_probs(lp_file)

    def annotate(self, query):
        """
        annotates 'query' with entities
        returns a dictionary with substrings as keys
        and entity wikilinks as values
        """
        query_words = query.split(" ")

        annotations = []
        self.annotate_with_lp(self.link_probs, query_words, len(query_words), annotations)
        return annotations

    def get_link_probs(self, file):
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

    def annotate_with_lp(self, link_probs, words, index_length, annotations):
        """
        annotates the words in 'words' using the link probabilities in 'link_probs'
        with maximum word length of an annotation being 'index_length' and outputs
        the results as a dictionary of (entity, probability) tuples in 'annotations'
        """

        for length in reversed(range(1, index_length + 1)):
            for start_index in range(0, len(words) - length + 1):
                potential_match = " ".join(words[start_index:start_index+length]).lower()

                if potential_match in link_probs:
                    most_likely_match = link_probs[potential_match][0]
                    annotations.append(Mention(potential_match, candidate_entities=[Entity(most_likely_match[0])]))
                    self.annotate_with_lp(link_probs, words[:start_index], length, annotations)
                    self.annotate_with_lp(link_probs, words[start_index+length:], length, annotations)
                    return

if __name__ == "__main__":
    main()

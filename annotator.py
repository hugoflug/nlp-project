
def main():
    #file not in git repo due to GitHub size restrictions
    dict_file = open("crosswikis-dict-preprocessed-2")
    link_probs = get_link_probs(dict_file)

    print("enter query: ")

    query = input().strip()
    query_words = query.split(" ")
    annotations = {}
    annotate(link_probs, query_words, len(query_words) + 1, annotations)

    for key, value in annotations.items():
        print("{} -- {} ({})".format(key, value[0], value[1]))

def get_link_probs(file):
    link_probs = {}
    for line in file:
        match = line.strip("\n").split("\t")
        words = match[0]
        rest = match[1].split(" ")
        prob = float(rest[0])
        entity = rest[1]
        if not words in link_probs:
            link_probs[words] = []
        link_probs[words].append((entity, prob))
    return link_probs

def annotate(link_probs, words, index_length, annotations):
    """
    annotates the words in 'words' using the link probabilities in 'link_probs'
    with maximum word length of an annotation being 'index_length' and outputs
    the results as a dictionary in 'annotations'
    """
    for length in reversed(range(1, index_length)):  
        for start_index in range(0, len(words) - length + 1):
            potential_match = words[start_index:start_index+length] 
            potential_match = " ".join(potential_match)

            try:
                match = link_probs[potential_match]
                annotations[potential_match] = (match[0][0], match[0][1])
                annotate(link_probs, words[:start_index], length + 1, annotations)
                annotate(link_probs, words[start_index+length:], length + 1, annotations)
                return
            except KeyError: pass

main()
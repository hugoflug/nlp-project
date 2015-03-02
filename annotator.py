
def main():
    #file not in git repo due to GitHub size restrictions
    dict_file = open("crosswikis-dict-preprocessed-2")
    matches = {} 
    for line in dict_file:
        match = line.strip("\n").split("\t")
        words = match[0]
        rest = match[1].split(" ")
        prob = float(rest[0])
        entity = rest[1]
        if not words in matches:
            matches[words] = []
        matches[words].append((entity, prob))

    print("enter query: ")

    query = input().strip()
    query_words = query.split(" ")
    annotate(matches, query_words, len(query_words) + 1)

def annotate(matches, words, index_length):
    for length in reversed(range(1, index_length)):  
        for start_index in range(0, len(words) - length + 1):
            potential_match = words[start_index:start_index+length] 
            potential_match = " ".join(potential_match)

            try:
                match = matches[potential_match]
                print("{} -- {} ({})".format(potential_match, match[0][0], match[0][1]))
                annotate(matches, words[:start_index], length + 1)
                annotate(matches, words[start_index+length:], length + 1)
                return
            except KeyError: pass

main()
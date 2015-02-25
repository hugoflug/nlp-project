
dict_file = open("crosswikis-dict-preprocessed")
matches = {} 
for line in dict_file:
    match = line.split("\t")
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
for length in reversed(range(1, len(query_words) + 1)):  
    for start_index in range(0, len(query_words) - length + 1):
        potential_match = query_words[start_index:start_index+length] 
        potential_match = " ".join(potential_match)
        if matches[potential_match]:
            print("matches:")
            for m in matches[potential_match]:
                print("match: ", m[0])

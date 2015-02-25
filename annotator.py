
dict_file = open("crosswikis-dict-preprocessed")
matches = {} 
for line in dict_file:
    match = line.split("\t")
    words = match[0]
    rest = match[1].split(" ")
    prob = float(rest[0])
    entity = rest[1]
    matches[words] = (entity, prob)

query = input().strip()
query_words = query.split(" ")
for length in reversed(range(1, len(query_words) + 1)):  
    for start_index in range(0, len(query_words) - length + 1):
        potential_match = query_words[start_index:start_index+length] 
        print(potential_match)

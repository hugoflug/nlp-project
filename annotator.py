dict_file = open("crosswikis-dict-preprocessed")
matches = {} 
for line in dict_file:
	match = line.split("\t")
	words = match[0]
	rest = match[1].split(" ")
	prob = float(rest[0])
	entity = rest[1]
	matches[words] = (entity, prob)
	print(words + ", " + str((entity, prob)))
f = open("crosswikis-dict-preprocessed")
f2 = open("crosswikis-dict-preprocessed-2", 'w')
for line in f:
	parts = line.split("\t")
	prob = float(parts[1].split(" ")[0])
	if prob > 0.01:
		f2.write(line)
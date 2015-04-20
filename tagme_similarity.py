import json
import urllib.request
import urllib.parse

class TagMeSimilarity(object):
    """ Utializes the TAGME web api to get pairwise entity similarities"""

    cache = {}

    """ Loads all pairwise similarities between the given entities for fast access later """
    def load_similarities(self, entities):

        cache = {}

        def flush():
            nonlocal buffer
            # Build URL
            url = "http://tagme.di.unipi.it/rel?key=tagme-NLP-ETH-2015&lang=en"
            for pair in buffer:
                tt = {"tt": pair[0] + " " + pair[1]}
                url += "&" + urllib.parse.urlencode(tt) 
            
            response = urllib.request.urlopen(url)
            res = json.loads(response.read().decode())["result"]

            for i in range(len(buffer)):
                if "rel" in res[i]:
                    self.cache[buffer[i]] = float(res[i]["rel"])
                else:
                    self.cache[buffer[i]] = 0

            # Empty buffer
            buffer = []

            return

        buffer = []

        for e1 in entities:
            for e2 in entities:
                #if(e1==e2): continue

                buffer.append((e1, e2))

                # Check if flush is needed
                if len(buffer) == 80 :
                    flush()

        if len(buffer) > 0:
            flush()

    def sim(self, e1, e2):
        return self.cache[(e1, e2)]

if __name__ == "__main__":
    tagme_sim = tagme_similarity()
    test_entities = ["Neil_Armstrong", "IPhone", "War_on_Terror"]
    tagme_sim.load_similarities(test_entities)
    print(tagme_sim.sim("Neil_Armstrong", "War_on_Terror"))
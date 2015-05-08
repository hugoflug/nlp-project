import json
import urllib.request
import urllib.parse
import pickle

class TagMeSimilarity(object):
    """ Utializes the TAGME web api to get pairwise entity similarities"""

    def __init__(self):
        # Load file cache
        self.cache = pickle.load(open('tagme_similarity_cache.pkl', 'rb'))
        self.cache_changed = False

    def load_similarities(self, entities):
        """ Loads all pairwise similarities between the given entities for fast access later.
            Takes a list of Entity objects. """

        #cache = {}

        def flush():
            nonlocal buffer, url_est_len
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
            url_est_len = 60
            self.cache_changed = True

            return

        buffer = []
        url_est_len = 60 # beginning of url: http://tagme......

        for e1 in entities:
            for e2 in entities:
                tuple = (e1.entity_id, e2.entity_id)
                if (not (tuple in self.cache)):
                    buffer.append(tuple)
                    url_est_len += 5 + len(e1.entity_id) + len(e2.entity_id) # len(&tt=_) = 5

                    # Check if flush is needed
                    if len(buffer) == 100 or url_est_len > 1850:
                        flush()

        if len(buffer) > 0:
            flush()

    def sim(self, e1, e2):
        return self.cache[(e1, e2)]

    def save_cache(self):
        if(self.cache_changed):
            output = open('tagme_similarity_cache.pkl', 'wb')
            # Pickle dictionary using protocol 0.
            pickle.dump(self.cache, output)

if __name__ == "__main__":
    tagme_sim = tagme_similarity()
    test_entities = ["Neil_Armstrong", "IPhone", "War_on_Terror"]
    tagme_sim.load_similarities(test_entities)
    print(tagme_sim.sim("Neil_Armstrong", "War_on_Terror"))
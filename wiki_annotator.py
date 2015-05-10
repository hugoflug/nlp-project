from mention import Mention
from entity import Entity
import json
import pickle
import urllib.request
import urllib.parse
import copy

class WikipediaAnnotator(object):

    """ Uses wikipedia API to come up with candidates to mentions """

    MAX_RESULTS = 5

    def __init__(self):
        # Load file cache
        self.cache = pickle.load(open('wikipedia_annotator_cache.pkl', 'rb'))
        self.cache_changed = False

    def wikify(self, title):
        return title.replace(" ", "_")

    def annotate(self, mentions):
        """
        takes a list of Mention objects, fills in their candidate_entities list
        with candidates
        """
        to_remove = []

        for mention in mentions:

            # If mention is in cache

            if (mention.substring in self.cache):
                mention.candidate_entities = copy.deepcopy(self.cache[mention.substring])
            else:

                # Else, go to wikipeda

                url = "http://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srinfo=totalhits%7Csuggestion&srprop=wordcount%7Credirecttitle&srlimit=" + str(self.MAX_RESULTS) + "&"
                url += urllib.parse.urlencode({"srsearch" : mention.substring})

                response = urllib.request.urlopen(url)
                res = json.loads(response.read().decode())

                # Look for suggestions
                #if("suggestion" in res["query"]["searchinfo"]):
                #    url2 = "http://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srinfo=totalhits%7Csuggestion&srprop=wordcount%7Credirecttitle&srlimit=5&"
                #    url2 += urllib.parse.urlencode({"srsearch" : res["query"]["searchinfo"]["suggestion"]})
                #    response2 = urllib.request.urlopen(url2)
                #    res2 = json.loads(response2.read().decode())
                #    res["query"]["search"] = res2["query"]["search"] + res["query"]["search"]

                mention.candidate_entities = []
                Z = len(res["query"]["search"])*(1+len(res["query"]["search"]))/2 # Normalization constant (arithmetic sum)

                i = len(res["query"]["search"])
                for entity_json in res["query"]["search"]:   
                    mention.candidate_entities.append(Entity(self.wikify(entity_json["title"]), i/Z))
                    i -= 1

                if(not mention.candidate_entities): # If wikipedia didnt find anything, remove mention
                    to_remove.append(mention)
                else:
                    self.cache[mention.substring] = copy.deepcopy(mention.candidate_entities)
                    self.cache_changed = True

        for obj in to_remove:
            mentions.remove(obj)

    def save_cache(self):
        if(self.cache_changed):
            output = open('wikipedia_annotator_cache.pkl', 'wb')
            pickle.dump(self.cache, output)
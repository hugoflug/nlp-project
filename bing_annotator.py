from mention import Mention
from entity import Entity
import urllib.parse
import urllib.request
from urllib.request import Request
import re
import pickle
import copy
import os.path

class BingAnnotator(object):

    MAX_RESULS = 5

    def __init__(self, use_cache = True, r = 0.3):
        # Load file cache
        self.cache = pickle.load(open('bing_annotator_cache.pkl', 'rb')) if os.path.exists('bing_annotator_cache.pkl') and use_cache else {}
        self.cache_changed = False
        self.use_cache = use_cache

        self.r = r # prior probability decay ratio

    def urlify(self, title):
        return title.replace(" ", "%20")
    
    def annotate (self, mentions):

        to_remove = []

        for mention in mentions:
            
            # If mention is in cache

            if (mention.substring in self.cache):
                mention.candidate_entities = copy.deepcopy(self.cache[mention.substring])

                # Re-calculate the prior-probabilities
                Z = (1 - self.r**len(mention.candidate_entities))/(1 - self.r) #  Normalization sum (Geometric sum)
                i = 1
                for c in mention.candidate_entities:
                    c.prior_probability = i/Z
                    i *= self.r

            else:

                # Else, go to bing

                p = re.compile('<h2><a href="http://en.wikipedia.org/wiki/[^"]*"')
                title = mention.substring
                request = Request("http://www.bing.com/search?q=" + self.urlify(title) + "+site%3Aen.wikipedia.org", headers={"Accept-Language": "en-US"})
                response = urllib.request.urlopen(request)
                response_text = response.read().decode('utf-8')

                mention.candidate_entries = []
                candidates = []

                i = 0
                for (letters) in p.findall(response_text):
                    if(i<self.MAX_RESULS):
                        candidates.append(letters[42:-1])
                        i += 1
                    else: break

                Z = (1 - self.r**i)/(1 - self.r) #  Normalization sum (Geometric sum)
                i = 1
                for c in candidates:
                    mention.candidate_entities.append(Entity(c, i/Z))
                    i *= self.r
            
                if(not mention.candidate_entities): # If bing didnt find anything, remove mention
                    to_remove.append(mention)
                else:
                    self.cache[mention.substring] = copy.deepcopy(mention.candidate_entities)
                    self.cache_changed = True
            
        for obj in to_remove:
            mentions.remove(obj)


    def save_cache(self):
        if(self.cache_changed and self.use_cache):
            output = open('bing_annotator_cache.pkl', 'wb')
            pickle.dump(self.cache, output)
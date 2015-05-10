from mention import Mention
from entity import Entity
import urllib.parse
import urllib.request
import re
import pickle
import copy

class BingAnnotator(object):

    MAX_RESULS = 5

    def __init__(self):
        # Load file cache
        self.cache = pickle.load(open('bing_annotator_cache.pkl', 'rb'))
        self.cache_changed = False

    def urlify(self, title):
        return title.replace(" ", "%20")
    
    def annotate (self, mentions):

        to_remove = []

        for mention in mentions:
            
            # If mention is in cache

            if (mention.substring in self.cache):
                mention.candidate_entities = copy.deepcopy(self.cache[mention.substring])
            else:

                # Else, go to bing

                p = re.compile('<div class="b_title"><h2><a href="http://en.wikipedia.org/wiki/[^"]*"')
                title = mention.substring
                request = "http://www.bing.com/search?q=" + self.urlify(title) + "+site%3Aen.wikipedia.org"
                response = urllib.request.urlopen(request)

                mention.candidate_entries = []
                candidates = []

                i = 0
                for (letters) in p.findall(response.read().decode('utf-8')):
                    if(i<self.MAX_RESULS):
                        candidates.append(letters[63:-1])
                        i += 1
                    else: break

                Z = len(candidates)*(1+len(candidates))/2 # Normalization constant (arithmetic sum)
                for c in candidates:
                    mention.candidate_entities.append(Entity(c, i/Z))
                    i -= 1
            
                if(not mention.candidate_entities): # If bing didnt find anything, remove mention
                    to_remove.append(mention)
                else:
                    self.cache[mention.substring] = copy.deepcopy(mention.candidate_entities)
                    self.cache_changed = True
            
        for obj in to_remove:
            mentions.remove(obj)


    def save_cache(self):
        if(self.cache_changed):
            output = open('bing_annotator_cache.pkl', 'wb')
            pickle.dump(self.cache, output)
from mention import Mention
from entity import Entity
import urllib.parse
import urllib.request
import re

class BingAnnotator(object):
    def urlify(self, title):
        return title.replace(" ", "%20")
    
    def annotate (self, mentions):
        for mention in mentions:
            p = re.compile('<div class="b_title"><h2><a href="http://en.wikipedia.org/wiki/[^"]*"')
            title = mention.substring
            request = "http://www.bing.com/search?q=" + self.urlify(title) + "+site%3Aen.wikipedia.org"
            response = urllib.request.urlopen(request)
            
            mention.candidate_entries = []
            
            i = 10
            for (letters) in p.findall(response.read().decode('utf-8')):
                mention.candidate_entities.append(Entity(letters[63:-1], i))
                i -= 1
            
    
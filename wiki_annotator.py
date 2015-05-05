from mention import Mention
from entity import Entity
import json
import urllib.request
import urllib.parse

class WikipediaAnnotator(object):

    """ Uses wikipedia API to come up with candidates to mentions """

    def wikify(self, title):
        return title.replace(" ", "_")

    def annotate(self, mentions):
        """
        takes a list of Mention objects, fills in their candidate_entities list
        with candidates
        """
        to_remove = []

        for mention in mentions:

            url = "http://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srprop=wordcount%7Credirecttitle&srlimit=10&"
            url += urllib.parse.urlencode({"srsearch" : mention.substring})

            response = urllib.request.urlopen(url)

            res = json.loads(response.read().decode())

            mention.candidate_entities = []
            Z = len(res["query"]["search"])*(1+len(res["query"]["search"]))/2 # Normalization constant (arithmetic sum)

            i = len(res["query"]["search"])
            for entity_json in res["query"]["search"]:   
                mention.candidate_entities.append(Entity(self.wikify(entity_json["title"]), i/Z))
                i -= 1

            if(not mention.candidate_entities): # If wikipedia didnt find anything, remove mention
                to_remove.append(mention)

        for obj in to_remove:
            mentions.remove(obj)
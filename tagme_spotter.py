import json
import urllib.request
import urllib.parse
from mention import Mention

class TagMeSpotter:

    def spot(self, query):
        """
        spots interesting substrings in a query string by using the TagMe spotting API
        returns a list of Mention objects with no candidate entities
        """

        spots = []

        url = "http://tagme.di.unipi.it/spot?key=tagme-NLP-ETH-2015&lang=en&"
        url += urllib.parse.urlencode({"text" : query})

        response = urllib.request.urlopen(url)

        res = json.loads(response.read().decode()) #should have "result"??
        for spot_info in res["spots"]:
            spots.append(Mention(spot_info["spot"], float(spot_info["lp"])))

        return spots
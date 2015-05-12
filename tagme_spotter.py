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
            spots.append(Mention(spot_info["spot"].lower(), float(spot_info["lp"])))

        # TEMP HACK:
        # if just one word => spot
        if(not spots and len(query.split(" ")) == 1):
            spots.append(Mention(query, 1.0))

        return spots
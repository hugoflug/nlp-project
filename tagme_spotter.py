import json
import urllib.request
import urllib.parse

class TagMeSpotter:

    def spot(self, query):
        spots = []

        url = "http://tagme.di.unipi.it/spot?key=tagme-NLP-ETH-2015&lang=en&"
        url += urllib.parse.urlencode({"text" : query})

        response = urllib.request.urlopen(url)

        res = json.loads(response.read().decode()) #should have "result"??
        for spot_info in res["spots"]:
            spots.append(spot_info["spot"])

        return spots
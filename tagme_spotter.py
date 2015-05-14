import json
import urllib.request
import urllib.parse
from mention import Mention
import os
import copy
import pickle

class TagMeSpotter:

    def __init__(self, use_cache = True):
        # Load file cache
        self.cache = pickle.load(open('tagme_spotter_cache.pkl', 'rb')) if os.path.exists('tagme_spotter_cache.pkl') and use_cache else {}
        self.cache_changed = False
        self.use_cache = use_cache


    def spot(self, query, remove_overlapping=False):
        """
        spots interesting substrings in a query string by using the TagMe spotting API
        returns a list of Mention objects with no candidate entities
        """

        # If query is in cache

        if (query in self.cache):
            spots = copy.deepcopy(self.cache[query])
        else:

            # Else, go to tagme...
            
            spots = []

            url = "http://tagme.di.unipi.it/spot?key=tagme-NLP-ETH-2015&lang=en&"
            url += urllib.parse.urlencode({"text" : query})

            response = urllib.request.urlopen(url)

            res = json.loads(response.read().decode())

            def spotlen(spot):
                return spot["end"] - spot["start"]

            if remove_overlapping:
                processed_spots = []
                last_spot = None
                for spot_info in res["spots"]:
                    # if we have an overlapping spot, remove the shorter one

                    doNotAdd = False
                    if last_spot and spot_info["start"] <= last_spot["end"]:
                        if spotlen(last_spot) < spotlen(spot_info):
                            processed_spots.remove(last_spot)
                        else:
                            doNotAdd = True
                    if not doNotAdd:
                        processed_spots.append(spot_info)
                        last_spot
                    last_spot = spot_info
            else:
                processed_spots = res["spots"]

            for spot_info in processed_spots:
                # if spots overlap, take the longest one
                spots.append(Mention(spot_info["spot"].lower(), float(spot_info["lp"])))
                last_spot = spot_info

            # TEMP HACK:
            # if just one word => spot
            if not spots and len(query.split(" ")) == 1:
                spots.append(Mention(query, 1.0))

            self.cache[query] = spots
            self.cache_changed = True

        return spots

    def save_cache(self):
        if(self.cache_changed and self.use_cache):
            output = open('tagme_spotter_cache.pkl', 'wb')
            pickle.dump(self.cache, output)
import urllib.parse
import urllib.request
import json

def annotate(query):
    """
    Annotates 'query' using the TAGME API
    """
    response = urllib.request.urlopen('http://tagme.di.unipi.it/tag?key=tagme-NLP-ETH-2015&lang=en&text=' + urllib.parse.quote(query))
    info = json.loads(response.read().decode())

    annotations = {}
    for annotation in info["annotations"]:
        annotations[annotation["spot"]] = annotation["title"].replace(" ", "_")

    return annotations
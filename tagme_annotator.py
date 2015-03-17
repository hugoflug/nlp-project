import urllib2
import urllib
import json

def annotate(query):
    response = urllib2.urlopen('http://tagme.di.unipi.it/tag?key=tagme-NLP-ETH-2015&lang=en&text=' + urllib.quote(query))
    info = json.loads(response.read())

    annotations = {}
    for annotation in info["annotations"]:
        annotations[annotation["spot"]] = annotation["title"].replace(" ", "_")

    return annotations
from xml.dom.minidom import parse
import xml.dom.minidom
import sys
import json
import urllib.request
import urllib.parse
from tagme_spotter import TagMeSpotter

def parseQueryDataset(filepath, fun):
    # read out query-set
    # Open XML document using minidom parser
    domtree = xml.dom.minidom.parse(filepath)

    collection = domtree.documentElement

    # Get all the sessions in the collection
    sessions = collection.getElementsByTagName("session")
    
    # Print detail of each session.
    for session in sessions:
        queries = session.getElementsByTagName("query")
        
        for query in queries:
            # Read out query-text and gold-annotations
            text = query.getElementsByTagName("text")[0].firstChild.nodeValue
            annotations_xml = query.getElementsByTagName("annotation")

            annotations = []

            for annotation in annotations_xml:
                if annotation.getAttribute("main") == "true" and \
                    annotation.getElementsByTagName("span").length > 0 and \
                    annotation.getElementsByTagName("target").length > 0:

                    mention = annotation.getElementsByTagName("span")[0].firstChild.nodeValue
                    target = annotation.getElementsByTagName("target")[0].firstChild.nodeValue[29:]

                    annotations.append((mention, target))

            # Run fun for the query
            fun(text, annotations)


noCorrectSpotted = 0
noNotCorrectSpotted = 0

def evaluateTagmeSpotting(query, trueAnnotations):

    global noCorrectSpotted
    global noNotCorrectSpotted

#    url = "http://tagme.di.unipi.it/spot?key=tagme-NLP-ETH-2015&lang=en&" + urllib.parse.urlencode({"text" : query})

#    response = urllib.request.urlopen(url)
#    res = json.loads(response.read().decode())
#    tagmeSpots = [spot["spot"] for spot in res["spots"]]

    spotter = TagMeSpotter()

    tagmeSpots = [m.substring for m in spotter.spot(query)]

    trueMentions = [a[0] for a in trueAnnotations]

    correct = True
    for a in trueMentions:
        # Check if tage also found a
        if a not in tagmeSpots:
            correct = False
            break
    #for a in tagmeSpots:
    #    if(a not in trueMentions):
    #        correct = False
    #        break

    if correct:
        noCorrectSpotted += 1
        s = "Correct:\t" + str(tagmeSpots) + " <-> " + str(trueMentions) + " : " + query
        print(s)
        f.write(s + "\n")
    else:
        noNotCorrectSpotted += 1
        s = "Not correct:\t" + str(tagmeSpots) + " <-> " + str(trueMentions) + " : " + query
        print(s)
        f.write(s + "\n")

f = open('result.txt', 'w')

parseQueryDataset("query-data-dev-set.xml", evaluateTagmeSpotting)

f.close()

print("Ratio: " + str(noCorrectSpotted/(noCorrectSpotted + noNotCorrectSpotted)))

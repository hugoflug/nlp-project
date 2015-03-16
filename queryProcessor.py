from xml.dom.minidom import parse
import xml.dom.minidom
import sys

import annotator

def main():
    # read out query-set
    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse("query-data-train-set.xml")
    collection = DOMTree.documentElement

    # Get all the sessions in the collection
    sessions = collection.getElementsByTagName("session")

    dict_file = open("crosswikis-dict-preprocessed-2", encoding="utf-8")
    link_probs = annotator.get_link_probs(dict_file)

    verbose = True if len(sys.argv) > 1 and sys.argv[1] == "-v" else False

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    # Print detail of each session.
    for session in sessions:
        if session.hasAttribute("id"):

            queries = session.getElementsByTagName("query")
      
            for query in queries:
                # Read out query-text and gold-annotations
                text = query.getElementsByTagName("text")[0]
                annotations = query.getElementsByTagName("annotation")
                
                # Split query to array
                queryArray = text.firstChild.nodeValue.split(" ")
                
                baselineMatches = {}
                annotator.annotate(link_probs, queryArray, len(queryArray), baselineMatches)
                
                gold_entities = set()

                # TODO: Get advanced annotations
                
                # TODO: Compare Baseline, Advanced & Gold standard
            

                if verbose:
                    print("QUERY: {}".format(text.firstChild.nodeValue))
                    print("GOLD:")
                for annotation in annotations:
                    if annotation.getAttribute("main") == "true" and annotation.getElementsByTagName("span").length > 0 and annotation.getElementsByTagName("target").length > 0:
                        span = annotation.getElementsByTagName("span")[0]
                        target = annotation.getElementsByTagName("target")[0]

                        substring = span.firstChild.nodeValue

                        #extract wikipedia-ID from URL
                        entity = target.firstChild.nodeValue.split("/").pop()

                        #add entity to set of gold entities
                        gold_entities.add(entity)

                        if verbose:
                            print("{}: {}".format(substring, entity))

                our_entities = set()
                if len(gold_entities) > 0:
                    for key, value in baselineMatches.items():
                        our_entities.add(value[0])

                if verbose: 
                    print("OUR MATCHES:")

                    for key, value in baselineMatches.items():
                        print("{}: {} ({})".format(key, value[0], value[1]))

                #TODO: Strict evaluation

                for entity in gold_entities:
                    if entity in our_entities:
                        tp += 1
                    if entity not in our_entities:
                        fn += 1

                for entity in our_entities:
                    if entity not in gold_entities:
                        fp += 1

    print("tp: {}".format(tp))
    print("fp: {}".format(fp))
    print("fn: {}".format(fn))

    recall = tp/float(tp+fn)
    precision = tp/float(tp+fp)

    print("recall: {0:.4f}".format(recall))
    print("precision: {0:.4f}".format(precision)) 
    print("f1: {0:.4f}".format(2*precision*recall/(precision + recall)))      
    
main()
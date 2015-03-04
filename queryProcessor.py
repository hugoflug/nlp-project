from xml.dom.minidom import parse
import xml.dom.minidom

import annotator

def main():
    # read out query-set
    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse("query-data-dev-set.xml")
    collection = DOMTree.documentElement

    # Get all the sessions in the collection
    sessions = collection.getElementsByTagName("session")

    dict_file = open("crosswikis-dict-preprocessed-2")
    link_probs = annotator.get_link_probs(dict_file)

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
                
                # TODO: Get Baseline annotations
                baselineMatches = {}
                annotator.annotate(link_probs, queryArray, len(queryArray), baselineMatches)
                
                our_entities = set()

                for key, value in baselineMatches.items():
                    our_entities.add(value[0])

                # TODO: Get advanced annotations
                
                # TODO: Compare Baseline, Advanced & Gold standard
                
                # Print query and gold standard

                gold_entities = set()

                for annotation in annotations:
                    if annotation.getAttribute("main") == "true" and annotation.getElementsByTagName("span").length > 0 and annotation.getElementsByTagName("target").length > 0:
                        span = annotation.getElementsByTagName("span")[0]
                        target = annotation.getElementsByTagName("target")[0]
                        substring = span.firstChild.nodeValue

                        entity = target.firstChild.nodeValue.split("/").pop()
                        gold_entities.add(entity)

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

    print("recall: {0:.4f}".format(tp/float(tp+fn)))
    print("precision: {0:.4f}".format(tp/float(tp+fp)))       
    
main()
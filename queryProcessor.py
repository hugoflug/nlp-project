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

    tp_strict = tp_relaxed = tn_strict = tn_relaxed = fp_strict = fp_relaxed = fn_strict = fn_relaxed = 0

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

                        #extract wikipedia-ID from URL. (query identifier, wikipedia identifier)
                        entity = (span.firstChild.nodeValue, target.firstChild.nodeValue.split("/").pop())

                        #add entity to set of gold entities
                        gold_entities.add(entity)

                        if verbose:
                            print("{}: {}".format(substring, entity))

                our_entities = set()
                if len(gold_entities) > 0:
                    for key, value in baselineMatches.items():
                        our_entities.add((key, value[0]))

                if verbose: 
                    print("OUR MATCHES:")

                    for key, value in baselineMatches.items():
                        print("{}: {} ({})".format(key, value))

                # Strict evaluation
                for entity in gold_entities:
                    if entity in our_entities:
                        tp_strict += 1
                    else:
                        fn_strict += 1

                for entity in our_entities:
                    if entity not in gold_entities:
                        fp_strict += 1

                #  Relaxed eval
                for entity in gold_entities:
                    if len([i for i, v in enumerate(our_entities) if v[1] == entity[1]]) > 0:
                        tp_relaxed += 1
                    else:
                        fn_relaxed += 1

                for entity in our_entities:
                    if len([i for i, v in enumerate(gold_entities) if v[1] == entity[1]]) == 0:
                        fp_relaxed += 1

    print("RELAXED EVALUATION:")

    print("tp: {}".format(tp_relaxed))
    print("fp: {}".format(fp_relaxed))
    print("fn: {}".format(fn_relaxed))

    recall = tp_relaxed/float(tp_relaxed+fn_relaxed)
    precision = tp_relaxed/float(tp_relaxed+fp_relaxed)

    print("recall: {0:.4f}".format(recall))
    print("precision: {0:.4f}".format(precision)) 
    print("f1: {0:.4f}".format(2*precision*recall/(precision + recall)))      

    print("\nSTRICT EVALUATION:")

    print("tp: {}".format(tp_strict))
    print("fp: {}".format(fp_strict))
    print("fn: {}".format(fn_strict))

    recall = tp_strict/float(tp_strict+fn_strict)
    precision = tp_strict/float(tp_strict+fp_strict)

    print("recall: {0:.4f}".format(recall))
    print("precision: {0:.4f}".format(precision)) 
    print("f1: {0:.4f}".format(2*precision*recall/(precision + recall)))   
    
main()
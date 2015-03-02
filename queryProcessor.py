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

    # Print detail of each session.
    for session in sessions:
        if session.hasAttribute("id"):
            print "SESSION: %s" % session.getAttribute("id")
    
            queries = session.getElementsByTagName("query")
      
            for query in queries:
                # Read out query-text and gold-annotations
                text = query.getElementsByTagName("text")[0]
                annotations = query.getElementsByTagName("annotation")
                
                # Split query to array
                queryArray = text.firstChild.nodeValue.split(" ")
                
                # TODO: Get Baseline annotations
                baselineMatches = {}
                # annotate(baselineMatches, queryArray, queryArray.length)
                
                # TODO: Get advanced annotations
                
                # TODO: Compare Baseline, Advanced & Gold standard
                
                # Print query and gold standard
                print "QUERY: '%s'" % text.firstChild.nodeValue
                for annotation in annotations:
                    if annotation.getAttribute("main") == "true" and annotation.getElementsByTagName("span").length > 0 and annotation.getElementsByTagName("target").length > 0:
                        span = annotation.getElementsByTagName("span")[0]
                        target = annotation.getElementsByTagName("target")[0]
                        print "%s: %s" % (span.firstChild.nodeValue, target.firstChild.nodeValue)
    
    
main()
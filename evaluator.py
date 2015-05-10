from xml.dom.minidom import parse
import xml.dom.minidom
from mention import Mention
from entity import Entity
import sys

class Evaluator:

    def for_each_query(self, queries_file, func):

        """ Executes the function func for every query in queries_file

        func(query_text, gold_mentions)
            query_text: the query as a string
            gold_mentions: list of Mention objects each with only one Entity

        """

        # Open XML document using minidom parser
        domtree = xml.dom.minidom.parse(queries_file)
        collection = domtree.documentElement

        # Get all the sessions in the collection
        sessions = collection.getElementsByTagName("session")
        
        # Count queries
        number_of_queries = 0
        for session in sessions:
            queries = session.getElementsByTagName("query")
            for query in queries:
                number_of_queries += 1
                
        query_number = 1
                
        # For each session
        for session in sessions:
            queries = session.getElementsByTagName("query")
      
            # For each query
            for query in queries:

                # Read out query-text
                query_text = query.getElementsByTagName("text")[0].firstChild.nodeValue
                #print("Query " + str(query_number) + " of " + str(number_of_queries) + ": " + query_text)
                query_number += 1
                
                # Read out the gold mentions and their annotations
                gold_mentions = []
                annotations_xml = query.getElementsByTagName("annotation")
                for annotation in annotations_xml:
                    if annotation.getAttribute("main") == "true" and \
                        annotation.getElementsByTagName("span").length > 0 and \
                        annotation.getElementsByTagName("target").length > 0:

                        span = annotation.getElementsByTagName("span")[0]
                        target = annotation.getElementsByTagName("target")[0]

                        entity = Entity(target.firstChild.nodeValue.split("/").pop())
                        mention = Mention(span.firstChild.nodeValue.lower(), candidate_entities=[entity])
                        gold_mentions.append(mention)

                # Run func
                func(query_text, gold_mentions)

    def evaluate(self, annotator_func, queries_file, gold_spotter = None):
        
        """
        evaluates how well the 'annotator_func' function annotates the given 'test_set'
        and prints it to stdout (TODO: return an object with the info instead?)

        'annotator_func' should take as input a query and return a dictionary with (substring, entity)
        key, value pairs
        """
        
        verbose = True if len(sys.argv) > 1 and sys.argv[1] == "-v" else False

        tp_strict = tp_relaxed = tn_strict = tn_relaxed = 0
        fp_strict = fp_relaxed = fn_strict = fn_relaxed = 0

        query_count = 1

        def evaluate_query(query_text, gold_mentions):

            nonlocal tp_strict, tp_relaxed, fp_strict, fp_relaxed, fn_strict, fn_relaxed, query_count

            # HACK:
            if(gold_spotter is not None):
                gold_spotter.set_mentions(gold_mentions)

            # Annotate using our algorithm
            our_mentions = annotator_func(query_text)

            # Relaxed evaluation
            for gold_mention in gold_mentions:
                if len([m for m in our_mentions if gold_mention.equalsRelaxed(m)]) > 0: # If gold entity is also in our set
                    tp_relaxed += 1
                else:
                    fn_relaxed += 1

            for m in our_mentions:
                if len([gold_mention for gold_mention in gold_mentions if m.equalsRelaxed(gold_mention)]) == 0: # If our entity is not in the gold set
                    fp_relaxed += 1

            # Strict evaluation
            for gold_mention in gold_mentions:
                if len([m for m in our_mentions if gold_mention.equalsStrict(m)]) > 0:
                    tp_strict += 1
                else:
                    fn_strict += 1

            for m in our_mentions:
                if len([gold_mention for gold_mention in gold_mentions if m.equalsStrict(gold_mention)]) == 0:
                    fp_strict += 1

            print("Evaluated query: " + str(query_count))
            query_count += 1


        # Loop through all queries in file
        self.for_each_query(queries_file, evaluate_query)

        # Print results
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

    def evaluateSpotting(self, spotter, queries_file):
        
        noCorrectSpotted = 0
        noNotCorrectSpotted = 0

        def evaluate_spot(query_text, gold_mentions):

            nonlocal noCorrectSpotted, noNotCorrectSpotted

            # Spot using spotter
            spots = spotter.spot(query_text)

            # Check 
            correct = True
            for gold_mention in gold_mentions:
                # Check if didn't found gold_mention
                if(not [m for m in spots if m.substring == gold_mention.substring]):
                    correct = False
                    break

            if(correct):
                noCorrectSpotted += 1
                s = "Correct:\t" + str(spots) + " <-> " + str(gold_mentions) + "\t" + query_text
                print(s)
            else:
                noNotCorrectSpotted += 1
                s = "Not correct:\t" + str(spots) + " <-> " + str(gold_mentions) + "\t" + query_text
                print(s)

        # Evaluate each query
        self.for_each_query(queries_file, evaluate_spot)

        # Pring final ratio
        print("Ratio: " + str(noCorrectSpotted/(noCorrectSpotted + noNotCorrectSpotted)))

    def evaluateAnnotatorScorer(self, annotator, scorer, similarity, queries_file):

        presentEntities = 0
        nonPresentEntities = 0
        nonPresentSpot = 0
        
        noQueries = 0
        allEntitiesPresent = 0 # Number of queries where all entities are present

        correctEntities = 0
        notCorrectEntities = 0
        correctAllEntities = 0
        notCorrectAllEntities = 0

        def get_all_entities(mentions):
            all_entities = []
            for m in mentions:
                all_entities.extend(m.candidate_entities)
            return all_entities

        def evaluate_query(query_text, gold_mentions):
            
            # Take the gold standard spots, and annotate them and see how often
            # the correct is present

            nonlocal presentEntities, nonPresentEntities, nonPresentSpot, noQueries, \
                   allEntitiesPresent, correctEntities, notCorrectEntities, \
                   correctAllEntities, notCorrectAllEntities

            #
            # Evaluate annotator
            #

            noQueries += 1
            mentions = [Mention(m.substring) for m in gold_mentions]

            annotator.annotate(mentions)

            _mentions = []
            for i in range(len(gold_mentions)):
                # If the spot was filtered out by annotator
                
                m = [m for m in mentions if m.substring == gold_mentions[i].substring]
                
                if(not m):
                    nonPresentSpot += 1
                    print("Spot unknown: " + str(gold_mentions[i].candidate_entities[0]) + "' for '" + gold_mentions[i].substring + "'")

                elif(gold_mentions[i].candidate_entities[0] in m[0].candidate_entities):
                    # Entity is among candidates!
                    presentEntities += 1
                    _mentions.append(m[0])

                else:
                    nonPresentEntities += 1
                    print("Entity unknown: '" + str(str(gold_mentions[i].candidate_entities[0]).encode(errors='ignore')) + "' for '" + gold_mentions[i].substring + "'")

            #
            # Evaluate scoring
            #

            # Check if we choose correct
            similarity.load_similarities(get_all_entities(mentions))
            scorer.score_candidates(mentions)
            scorer.choose_candidates(mentions)

            if(len(gold_mentions) == len(_mentions)): # If correct entity is present in all mentinos
                allEntitiesPresent += 1

                for i in range(len(gold_mentions)):
                    if(mentions[i].candidate_entities[0] == gold_mentions[i].candidate_entities[0]):
                        correctAllEntities += 1
                    else:
                        notCorrectAllEntities += 1

            for m in _mentions: # For the mentions where the correct entity was pesent
                gold = [gm for gm in gold_mentions if gm.substring.lower() == m.substring.lower()][0]
                if(m.candidate_entities[0] == gold.candidate_entities[0]): # Check if we chose the correct one
                    correctEntities += 1
                else:
                    notCorrectEntities += 1

            print("Evaluated query: " + str(noQueries))

        self.for_each_query(queries_file, evaluate_query)

        # Print results
        print("")
        print("Entity among candidates ratio: " + str(presentEntities/(presentEntities + nonPresentEntities + nonPresentSpot)) + " (" + str(presentEntities) + ")")
        print("No candidates at all ratio: " + str(nonPresentSpot/(presentEntities + nonPresentEntities + nonPresentSpot)) + " (" + str(nonPresentSpot) + ")")
        print("Entity not among candidates ratio: " + str(nonPresentEntities/(presentEntities + nonPresentEntities + nonPresentSpot)) + " (" + str(nonPresentEntities) + ")")
        print("")
        print("All entities present ratio: " + str(allEntitiesPresent/noQueries) + " (" + str(allEntitiesPresent) + ")")
        print("")
        print("Correct chosen ratio (among mentions where the correct entities for all mentions in the query are present): " + str(correctAllEntities/(correctAllEntities + notCorrectAllEntities)))
        print("Correct chosen ratio (among mentions where the correct entity is present): " + str(correctEntities/(correctEntities + notCorrectEntities)))

    def evaluatePruner(self, spotter, annotator, similarity, scorer, pruner, queries_file):

        def evaluateQuery(query_text, gold_mentions): 
            # Step 1: Find mentions
            mentions = spotter.spot(query)

            # Step 2: Find candidates for the mentions (annotate the mentions)
            annotator.annotate(mentions)

            # Step 3: Choose the best candidates
            similarity.load_similarities(get_all_entities(mentions))

            scorer.score_candidates(mentions)
            scorer.choose_candidates(mentions)

            # Find out which mentions should be pruned
            should_prune = []
            for m in mentions:
                # if it is not in gold, we should prune it
                gold = [gm for gm in gold_mentions if gm.substring == m.substring]
                if(m): # if not empty
                    should_prune.append(m[0])

            # Step 4: Prune
            pruner.prune(mentions, 0.1, similarity.sim)

            for m in mentions:
                # Should this mention have been pruned?
                should_be_pruned = len([m2 for m2 in should_prune if m2.substring == m.substring]) >= 0
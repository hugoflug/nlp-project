from xml.dom.minidom import parse
import xml.dom.minidom
import sys

from evaluator import Evaluator
import annotator
import tagme_annotator

from entity_linker import EntityLinker
from tagme_similarity import TagMeSimilarity
from mention import Mention
from bing_annotator import BingAnnotator
from wiki_annotator import WikipediaAnnotator
from multi_annotator import MultiAnnotator
from pp_annotator import PriorProbabilityAnnotator

def main():

    # Create evaluator
    evaluator = Evaluator()

    print("\nOUR ANNOTATOR (DEV-SET):")
    print("***********************\n")
    annot = annotator.Annotator(open("crosswikis-dict-preprocessed-2", encoding="utf-8"))
    evaluator.evaluate(annot.annotate, "query-data-dev-set.xml")
    """
    print("\nOUR ANNOTATOR (TRAIN-SET):")
    print("***********************\n")
    annot = annotator.Annotator(open("crosswikis-dict-preprocessed-2", encoding="utf-8"))
    evaluator.evaluate(annot.annotate, "query-data-train-set.xml")
    """

    print("\nNEW ANNOTATOR (DEV-SET):")
    print("***********************\n")
    bing_annotator = BingAnnotator()
    wiki_annotator = WikipediaAnnotator()
    sim = TagMeSimilarity()
    #spotter = GoldSpotter()
    #pruner = DumbPruner()
    entity_linker = EntityLinker(similarity=sim, annotator=MultiAnnotator(None, wiki_annotator))
    evaluator.evaluate(entity_linker.annotate, "query-data-dev-set.xml")
    sim.save_cache() # save if we have any new similarities to cache on file
    bing_annotator.save_cache()
    wiki_annotator.save_cache()
    
    """
    print("\nTAGME ANNOTATOR (DEV-SET):")
    print("***********************\n")
    evaluator.evaluate(tagme_annotator.annotate, "query-data-dev-set.xml")

    print("\nTAGME ANNOTATOR (TRAIN-SET):")
    print("***********************\n")
    evaluator.evaluate(tagme_annotator.annotate, "query-data-train-set.xml")
    """

class GoldSpotter(object):

    # HACK
    def set_mentions(self, mentions):
        #for m in mentions:
        #    m.candidate_entities = []

        self.mentions_temp = [Mention(m.substring) for m in mentions]

    def spot(self, mentions):
        return self.mentions_temp

class DumbPruner(object):

    def prune(self, mentions, a, b):
        return mentions

if __name__ == "__main__":
    main()
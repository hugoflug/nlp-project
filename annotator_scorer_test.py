
from pp_annotator import PriorProbabilityAnnotator
from evaluator import Evaluator
from candidate_scorer import CandidateScorer
from tagme_similarity import TagMeSimilarity
from wiki_annotator import WikipediaAnnotator
from multi_annotator import MultiAnnotator
from bing_annotator import BingAnnotator

evaluator = Evaluator()

wiki_annotator = WikipediaAnnotator()
bing_annotator = BingAnnotator()
annotator = MultiAnnotator(None, wiki_annotator, bing_annotator)
similarity = TagMeSimilarity()
scorer = CandidateScorer(similarity.sim)

evaluator.evaluateAnnotatorScorer(annotator, scorer, similarity, "query-data-dev-set.xml")

similarity.save_cache()
wiki_annotator.save_cache()
bing_annotator.save_cache()
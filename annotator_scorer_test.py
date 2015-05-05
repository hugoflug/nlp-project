
from pp_annotator import PriorProbabilityAnnotator
from evaluator import Evaluator
from candidate_scorer import CandidateScorer
from tagme_similarity import TagMeSimilarity
from wiki_annotator import WikipediaAnnotator
from multi_annotator import MultiAnnotator

evaluator = Evaluator()

annotator = MultiAnnotator(None, PriorProbabilityAnnotator(), WikipediaAnnotator())
similarity = TagMeSimilarity()
scorer = CandidateScorer(similarity.sim)

evaluator.evaluateAnnotatorScorer(annotator, scorer, similarity, "query-data-dev-set.xml")
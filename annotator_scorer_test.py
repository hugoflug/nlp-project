
from pp_annotator import PriorProbabilityAnnotator
from evaluator import Evaluator
from candidate_scorer import CandidateScorer
from tagme_similarity import TagMeSimilarity


evaluator = Evaluator()

annotator = PriorProbabilityAnnotator()
similarity = TagMeSimilarity()
scorer = CandidateScorer(similarity.sim)

evaluator.evaluateAnnotatorScorer(annotator, scorer, similarity, "query-data-dev-set.xml")

from pp_annotator import PriorProbabilityAnnotator
from evaluator import Evaluator
from candidate_scorer import CandidateScorer
from tagme_similarity import TagMeSimilarity
from wiki_annotator import WikipediaAnnotator
from multi_annotator import MultiAnnotator
from bing_annotator import BingAnnotator
from candidate_pruner import CandidatePruner
from tagme_spotter import TagMeSpotter

evaluator = Evaluator()

spotter = TagMeSpotter()
annotator = MultiAnnotator(None, PriorProbabilityAnnotator(), WikipediaAnnotator(), BingAnnotator())
similarity = TagMeSimilarity()
scorer = CandidateScorer(similarity.sim)
pruner = CandidatePruner()

evaluator.evaluatePruning2(spotter, annotator, scorer, similarity, pruner, "query-data-dev-set.xml")

similarity.save_cache()
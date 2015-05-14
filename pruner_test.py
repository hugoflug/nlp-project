
from evaluator import Evaluator
from wiki_annotator import WikipediaAnnotator
from bing_annotator import BingAnnotator
from multi_annotator import MultiAnnotator
from tagme_similarity import TagMeSimilarity
from candidate_scorer import CandidateScorer
from candidate_pruner import CandidatePruner
from tagme_spotter import TagMeSpotter

evaluator = Evaluator()

spotter = TagMeSpotter()

wiki_annotator = WikipediaAnnotator()
bing_annotator = BingAnnotator()
annotator = MultiAnnotator(None, wiki_annotator, bing_annotator)
similarity = TagMeSimilarity()
scorer = CandidateScorer(similarity.sim)

pruner = CandidatePruner(0.6)

evaluator.evaluatePruner(spotter, annotator, similarity, scorer, pruner, "query-data-dev-set.xml")

similarity.save_cache()
wiki_annotator.save_cache()
bing_annotator.save_cache()


from sklearn.grid_search import ParameterGrid

from evaluator import Evaluator
from tagme_spotter import TagMeSpotter
from multi_annotator import MultiAnnotator
from wiki_annotator import WikipediaAnnotator
from bing_annotator import BingAnnotator
from candidate_scorer import CandidateScorer
from tagme_similarity import TagMeSimilarity
from candidate_pruner import CandidatePruner
from entity_linker import EntityLinker

spotter = TagMeSpotter()
wiki_annotator = WikipediaAnnotator()
bing_annotator = BingAnnotator()
annotator = MultiAnnotator(None, wiki_annotator, bing_annotator)
similarity = TagMeSimilarity()
scorer = CandidateScorer(similarity.sim)
pruner = CandidatePruner()

evaluator = Evaluator()
entity_linker = EntityLinker(spotter, annotator, similarity, scorer, pruner)

param_grid = {'prune_theta': [0, 0.1, 0.2, 0.3], 
              'scorer_epsilon' : [0.1, 0.2, 0.3], 
              'annotator_decay': [0.3, 0.5, 0.7],
              'wiki_bing_weights': [ [1.0, 0.0], [0.8, 0.2], [0.6, 0.4], [0.5, 0.5], [0.4, 0.6], [0.2, 0.8], [0.0, 1.0] ] }

grid = ParameterGrid(param_grid)

best_f1 = 0
best_params = []

for params in grid:

    pruner.theta = params["prune_theta"]
    scorer.epsilon = params["scorer_epsilon"]
    bing_annotator.r = params["annotator_decay"]
    wiki_annotator.r = params["annotator_decay"]
    annotator.weights = params["wiki_bing_weights"]

    print("Running with params:")
    print(params)

    f1 = evaluator.evaluate(entity_linker.annotate, "query-data-dev-set.xml")

    print("f1 = " + str(f1))
    print("")

    if(f1 > best_f1):
        best_f1 = f1
        best_params = params

print("Best f1: " + str(best_f1))
print("Best parameters:")
print(best_params)

spotter.save_cache()
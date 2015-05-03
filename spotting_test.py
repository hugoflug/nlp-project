
from evaluator import Evaluator
from tagme_spotter import TagMeSpotter

evaluator = Evaluator()
spotter = TagMeSpotter()

evaluator.evaluateSpotting(spotter, "query-data-dev-set.xml")

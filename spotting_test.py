
from evaluator import Evaluator
from tagme_spotter import TagMeSpotter
import sys

f = open('out.txt', 'w')
sys.stdout = f
evaluator = Evaluator()
spotter = TagMeSpotter()

evaluator.evaluateSpotting(spotter, "query-data-dev-set.xml")

f.close()
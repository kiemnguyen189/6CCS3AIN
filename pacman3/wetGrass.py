# wetGrass.py
#
# The wet grass Bayesian network in computational form, using pomegranate
#
# Simon Parsons
# October 2018

from pomegranate import *

#
# Set up the model
#

# Variables are Cloudy, Sprinkler, Rain and WetGrass
#
# We have a prior for Cloudy, two values 'c'loudy and c'l'ear:
Cloudy   = DiscreteDistribution({'c': 0.5, 'l': 0.5})

# Conditional distribution relating Cloudy and Sprinkler. Notation for
# the conditional probability table is:
#
# [ 'Cloudy', 'Sprinkler', <probability>]
#
# for the conditional value P(Sprinkler|Cloudy).
#
# Values for Sprinkler are o'n' and o'f'f:
Sprinkler = ConditionalProbabilityTable(
        [['c', 'n', 0.1],
         ['c', 'f', 0.9],
         ['l', 'n', 0.5],
         ['l', 'f', 0.5]], [Cloudy])

# Conditional distribution relating Cloudy and Rain. Notation for the
# conditional probability table is:
#
# [ 'Cloudy', 'Rain', <probability>]
#
# for the conditional value P(Sprinkler|Cloudy).
#
# Values for Rain are 'r'ain and 'n'o rain:
Rain = ConditionalProbabilityTable(
        [['c', 'r', 0.8],
         ['c', 'n', 0.2],
         ['l', 'r', 0.2],
         ['l', 'n', 0.8]], [Cloudy])

# Conditional distribution relating Wet Grass to Sprinkler and
# Rain. Notation for the conditional probability table is:
#
# [ 'Cloudy', 'Rain', <probability>]
#
# for the conditional value P(Sprinkler|Cloudy).
#
# Values for WetGrass are 'w'et and 'd'ry:
WetGrass = ConditionalProbabilityTable(
        [['n', 'r', 'w', 0.99],
         ['n', 'r', 'd', 0.01],
         ['n', 'n', 'w', 0.9],
         ['n', 'n', 'd', 0.1],
         ['f', 'r', 'w', 0.9],
         ['f', 'r', 'd', 0.1],
         ['f', 'n', 'w', 0.01],
         ['f', 'n', 'd', 0.99]], [Sprinkler, Rain])

# After creating the distributions, create a network to capture the
# relationship between the variables. This is as in the slides.
#
# Four nodes:
s1 = Node(Cloudy, name="Cloudy")
s2 = Node(Sprinkler, name="Sprinkler")
s3 = Node(Rain, name="Rain")
s4 = Node(WetGrass, name="Wet Grass")
# Create a network that includes nodes and an edge between them:
model = BayesianNetwork("Wet Grass")
model.add_states(s1, s2, s3, s4)
model.add_edge(s1, s2)
model.add_edge(s1, s3)
model.add_edge(s2, s4)
model.add_edge(s3, s4)
# Fix the model structure
model.bake()

#
# Query the model
#

# Given we see wet grass, what do we think about the other variables:
scenario = [[None, None, None, 'w']]

# A message about the evidence presented.
#
# This is hard-coded to reflect the variables used in the model (see
# below).
msg = ""
if scenario[0][0] == 'c':
    msg += "Sky is clear; "
if scenario[0][0] == 'l':
    msg += "Sky is clear; "
if scenario[0][1] == 'f':
    msg += "Sprinkler is off; "
if scenario[0][1] == 'n':
    msg += "Sprinkler is on; "
if scenario[0][2] == 'r':
    msg += "Rain; "
if scenario[0][2] == 'n':
    msg += "No rain; "
if scenario[0][3] == 'w':
    msg += "Grass is wet."
if scenario[0][3] == 'd':
    msg += "Grass is dry."
   
print "Evidence is: ", msg
print

# model.predict reports the most probable value given the evidence
# provided. Here we ask what the most likely values of the variables
# are if the grass is wet.
#
# model.predict returns a vector of values of the states/nodes in the
# order specified in model.add_states().
prediction =  model.predict(scenario)

# model.predict.proba returns the distribution, wrapped in some
# meta-data. Again the order follows from model.add_states():
predict_proba =  model.predict_proba(scenario)

#  
# Pretty printing the output.
#

# First the most likely value of each variable. I don't know how to
# look up the variable names within the model (the documentation
# suggests that tehre is no way to access them), so these have to be
# hardcoded based on the order of the variables in model.add_states().
print "Here's the prediction:"
msg = ""
if prediction[0][0] == 'c':
    msg = msg + "Cloudy, "
else:
    msg = msg + "Clear, "
    
if prediction[0][1] == 'n':
    msg = msg + "Sprinkler On, "
else:
    msg = msg + "Sprinkler Off, "
    
if prediction[0][2] == 'r':
    msg = msg + "Rain, "
else:
    msg = msg + "No rain, "
    
if prediction[0][3] == 'w':
    msg = msg + "Wet grass."
else:
    msg = msg + "Dry grass"
    
print msg

# Next, the probability distributions for non-evidence variables.
print "And by the numbers:"

for i in range(model.state_count()):
    # Pull out the information about each variable
    dist = predict_proba[0][i]
    # Evidence variable are strings, so we can filter them out
    if isinstance(dist, Distribution):
        # Each element here is a distribution object. Pull out the
        # probabilities
        probs =  dist.items()
        # Now the hard-coded variable names:
        if i == 0:
            msg = "Cloudy: "
        elif i == 1:
            msg = "Sprinkler: "
        elif i == 2:
            msg = "Rain: "
        elif i ==3:
            msg = "Wet Grass: "

        print msg, probs

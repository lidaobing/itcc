# $Id$

"""genetic.lifecycle -- generation and life-cycle management

Just setup genetic.organism and then call run(...) to run a big number of generations !
"""

__revision__ = '$Rev$'


from genetic import organism
import random, string

def couple(organisms):
  """couple([organism1, organism2, ...]) -> (father, mother) -- Get a random couple from a list of organisms."""
  father, mother = None, None
  while father is mother:
    father, mother = random.choice(organisms), random.choice(organisms)
  return father, mother

def make_love(organisms, nb_children):
  """make_love(organisms, nb_children) --> children -- Make the requested number of children, from the given population of organisms."""
  if len(organisms) < 2:
    import sys
    print
    print "Less than 2 organisms ! Cannot continue !"
    sys.exit(1)



  children = []

  for i in xrange(nb_children):
    father, mother = couple(organisms)
    child = organism.multiply(father, mother)
    if child is None or not child.canlive:
      # This child is not OK...
      continue
    children.append(child)

  return children

def life_cycle(organisms, elitism, nb_children, nb_organisms,
               replaceratio = 0.0, neworganismgen = None):
  """life_cycle(organisms, elitism, nb_children, nb_organisms) -> [Organism1, ...] -- Do a life cycle / a generation for the given organisms, and return the new population.
If true, elitism means always keep the better organism.
nb_children is the requested number of children, and nb_organisms the number oOrganismf organisms to retain in the final population.
"""
  if 0.0 < replaceratio <= 1.0 and neworganismgen is not None:
    nb_replace = int(nb_children * replaceratio)
    nb_children -= nb_replace

  children = make_love(organisms, nb_children)
  for i in xrange(nb_replace):
    children.append(neworganismgen())

  if elitism:
    # Add the best organism of the previous generation in the possible candidates for the next one.
    children.append(min(organisms))

  children.sort()

  organisms = []
  for child in children:
    if not child in organisms:
      organisms.append(child)
      if len(organisms) >= nb_organisms: break

  return organisms

def dump(organisms):
  """dump(organisms) -- print the given list of organisms."""
  i = 0
  for organism in organisms:
    print "organism %s :" % i
    print indent(`organism`)
    i = i + 1

def indent(s, indentation = "  "):
  """indent("firstline\nsecondline\n,...") -> "  firstline\n  secondline\n,..." -- Indent the given line of text."""
  return indentation + string.join(s.split("\n"), "\n%s" % indentation)[:-len(indentation)]


def run(organisms, elitism = 1, nb_generation = 10, nb_children = 100, nb_organisms = 10, dump_generation = 0,
        replaceratio = 0.0, neworganismgen = None):
  """run(organisms, elitism = 1, nb_generation = 10, nb_children = 100, nb_organisms = 10, dump_generation = 0) -- Runs the given number of generations, starting with the given population (=sequence) of organisms.
If true, elitism means always keep the better organism.
nb_children is the number of children created per generation, and nb_organisms the number of organisms to retain in the final population, for each generation.
If dump_generation is true, dumps all generation. Else, prints only the final best organisms."""
  for i in xrange(nb_generation):
    print
    print "Generation %s..." % i

    organisms = life_cycle(organisms, elitism, nb_children, nb_organisms,
                           replaceratio, neworganismgen)
    if dump_generation:
      dump(organisms)

  best = organisms[0]
  print
  print "Best organism :"
  print `best`

  return organisms



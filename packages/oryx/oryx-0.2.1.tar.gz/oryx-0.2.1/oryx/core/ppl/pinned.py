"""TODO(sharadmv): DO NOT SUBMIT without one-line documentation for pinned.

TODO(sharadmv): DO NOT SUBMIT without a detailed description of pinned.
"""
from jax import tree_util

from oryx.core import primitive
from oryx.core.interpreters import log_prob
from oryx.core.interpreters.inverse import rules as inverse_rules
from oryx.core.ppl import transformations
from oryx.core.ppl import effect_handler

pin_p = primitive.FlatPrimitive('pin')


@pin_p.def_impl
def pin_impl(left_value, right_value, *, branch):
  if branch == 'left':
    return [left_value]
  elif branch == 'right':
    return [right_value]
  raise ValueError('Branch must be `\'left\'` or `\'right\'`')


@pin_p.def_abstract_eval
def pin_abstract_eval(left_aval, right_aval, *, branch):
  return pin_impl(left_aval, right_aval, branch=branch)


def pin_value(left, right, *, branch):

  def _pin_value(l, r):
    return pin_p.bind(l, r, branch=branch)[0]

  return tree_util.tree_multimap(_pin_value, left, right)


def pin_ildj_rule(incells, outcells, *, branch):
  outcell, = outcells
  if outcell.top():
    return [outcell, outcell], outcells, None
  if branch == 'left':
    return incells, [incells[0]], None
  elif branch == 'right':
    return incells, [incells[1]], None
  return incells, outcells, None


inverse_rules.ildj_registry[pin_p] = pin_ildj_rule


def pin(program, value):

  def wrapped(key, *args, **kwargs):
    output = program(key, *args, **kwargs)
    return pin_value(output, value, branch='right')

  return wrapped

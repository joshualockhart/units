from nose.tools import assert_almost_equal, assert_equal, assert_raises
from units import Term, IncompatibleUnitsError

"""
assert(5*meters == 0.005*kilometers)
assert((60*seconds).to(minutes).value==1)
assert((60*seconds).to(minutes).unit==minutes)

with assert_raises(IncompatibleUnitsError):
    5*meters+2*seconds
"""
def test_equality():
    metres = Term('metres')
    centimetres = Term('centimetres')

    assert_equal((5*metres).equals((500*centimetres)),True)

def test_conversion_value():
    metres = Term('metres')
    centimetres = Term('centimetres')
    assert_equal((5*metres).to(centimetres).value(),500)

def test_conversion_units():
    metres = Term('metres')
    centimetres = Term('centimetres')
    assert_equal((5*metres).to(centimetres).unit(),"centimetres ")
  
def test_incompatibility():
    metres = Term('metres')
    litres = Term('litres')
    with assert_raises(IncompatibleUnitsError):
        5*metres+2*litres
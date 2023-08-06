import pytest

from comlibpy.iter import *
import operator

class TestBasic:

    def test_basic(self):
        a = [1,2,3,4,5]
        assert map( lambda x: x+1, a ).filter(lambda x:x%2==0).reduce(operator.add) == 12

    def test_multi_ite(self):
        a = [1,2,3,4,5]
        b = a
        assert map( lambda x: x+1, a ).filter(lambda x:x%2==0).reduce(operator.add) == 12
        assert map( lambda x: x+1, b ).filter(lambda x:x%2==0).reduce(operator.add) == 12

from numpy import exp, sqrt, log, cos, sin, isnan, isinf, seterr

seterr(over='raise')
def _log(x):
    if x <= 0:
        return 0
    return log(x)

def _exp(x):
    try:
        return exp(x)
    except (FloatingPointError):
        return 1

def _sqrt(x):
    return sqrt(abs(x))

def _cos(x):
    return cos(x)

def _sin(x):
    return sin(x)

def  _div_(x,y):
    if y == 0:
        return 1
    return x / y

def _inv(x):
    if x == 0:
        return 1
    return 1.0 / x

"""
    Code from Nuno Lourenço
    https://github.com/nunolourenco/sge
"""
class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)


_div = Infix(_div_)
# print(8 |_div| 2)
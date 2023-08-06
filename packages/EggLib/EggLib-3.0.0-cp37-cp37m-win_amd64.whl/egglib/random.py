"""
    Copyright 2015-2021 Stephane De Mita, Mathieu Siol

    This file is part of EggLib.

    EggLib is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EggLib is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with EggLib.  If not, see <http://www.gnu.org/licenses/>.
"""

from . import eggwrapper as _eggwrapper

_static_random = _eggwrapper.Random() # use default seed

def boolean():
    """
    Draw a boolean with equal probabilities (*p* = 0.5).

    :return: A boolean.
    """
    return _static_random.brand()

def bernoulli(p):
    """
    Draw a boolean with given probability.

    :param p: probability of returning ``True``.
    :return: A boolean.
    """
    if p < 0 or p > 1: raise ValueError('`p` must be >=0 and <=1')
    return _static_random.uniform() < p

def binomial(n, p):
    """
    Draw a value from a binomial distribution.

    :param n: Number of tests (>=0).
    :param p: Test probability (>=0 and <=1).
    :return: An integer (number of successes).
    """
    if n < 0: raise ValueError('number of tests `n` must be >=0')
    if p < 0 or p > 1: raise ValueError('`p` must be >=0 and <=1')
    return _static_random.binomrand(n, p)

def exponential(expectation):
    """
    Draw a value from an exponential distribution.

    :param expectation: distribution's mean (equal to
        1/:math:`\lambda` , if :math:`\lambda` is the rate
        parameter). Required to be >0.
    :return: An integer.
    """
    if expectation <=0: raise ValueError('`expectation` must be strictly positive')
    return _static_random.erand(expectation)

def geometric(p):
    """
    Draw a value from a geometric distribution.

    :param p: geometric law parameter (>0 and <=1).
    :return: A positive integer.
    """
    if p<=0 or p>1: raise ValueError('`p` must be >0 and <=1')
    return _static_random.grand(p)

def normal():
    """
    Draw a value from the normal distribution. Expectation is 0
    and variance i 1. The expression ``rand.normal() * sd + m`` can be
    used to rescale the drawn value to a normal distribution with
    expectation :math:`m` and standard deviation :math:`sd`.

    :return: A real value.
    """
    return _static_random.nrand()

def normal_bounded(expect, sd, mini, maxi):
    """
    Draw a value from a normal distribution with bounds.

    :params expect: expectation
    :params sd: standard deviation
    :params mini: minimal value (included)
    :params maxi: maximal value (included)

    :return: A real number.
    """
    return _static_random.nrandb()

def poisson(p):
    """
    Draw a value from a Poisson distribution.

    :param p: Poisson distribution parameter (usually noted
        :math:`\lambda`). Required to be >0
    :return: A positive integer.
    """
    if p <= 0: raise ValueError('`p` must be strictly positive')
    return _static_random.prand(p)

def integer(n):
    """
    Draw an integer from a uniform distribution.

    :param n: mumber of possible values). Note that this number is
        excluded and will never be returned. Required to be a
        stricly positive integer.
    :return: An integer in range ``[0, n-1]``.
    """
    if n <=0: raise ValueError('`n` must be strictly positive')
    return _static_random.irand(n)

def integer_32bit():
    """
    Draw a 32-bit random integer.

    :return: An integer in the interval [0, 4294967295] (that
        is in the interval [0, 2^32-1].
    """
    return _static_random.rand_int32()

def uniform():
    """
    Draw a value in the half-open interval [0,1) with default
    32-bit precision. The value 1 is not included.
    """
    return _static_random.uniform()

def uniform_53bit():
    """
    Draw a value in the half-open interval [0,1) with
    increased 53-bit precision. The value 1 is not included.

    The increased precision increases the number of possible values
    (2^53 = 9007199254740992 instead of 2^32 = 4294967296). This
    comes with the cost of increased computing time.
    """
    return _static_random.uniform53()

def uniform_closed():
    """
    Draw a value in the closed interval [0,1]. Standard
    32-bit precision. Both limits are included.
    """
    return _static_random.uniformcl()

def uniform_open():
    """
    Draw a value in the open interval (0,1). Standard
    default 32-bit precision. Both limits are excluded.
    """
    return _static_random.uniformop()

def get_seed():
    """
    Get the seed value.

    :return: An integer.
    """
    return _static_random.get_seed()

def set_seed(seed):
    """
    Reset the random number sequence with a seed value.
    """
    if not isinstance(seed, int): raise TypeError('invalid type for `seed`')
    return _static_random.set_seed(seed)

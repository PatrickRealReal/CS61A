from operator import add, mul, sub

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


HW_SOURCE_FILE=__file__


def product(n, term):
    """Return the product of the first n terms in a sequence.
    n -- a positive integer
    term -- a function that takes one argument to produce the term

    >>> product(3, identity)  # 1 * 2 * 3
    6
    >>> product(5, identity)  # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)    # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)    # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    >>> product(3, increment) # (1+1) * (2+1) * (3+1)
    24
    >>> product(3, triple)    # 1*3 * 2*3 * 3*3
    162
    """
    "*** YOUR CODE HERE ***"
    temp = 1

    for i in range(n):
        temp *= term(i+1)

    return temp



def accumulate(combiner, base, n, term):
    """Return the result of combining the first n terms in a sequence and base.
    The terms to be combined are term(1), term(2), ..., term(n).  combiner is a
    two-argument commutative function.

    >>> accumulate(add, 0, 5, identity)  # 0 + 1 + 2 + 3 + 4 + 5
    15
    >>> accumulate(add, 11, 5, identity) # 11 + 1 + 2 + 3 + 4 + 5
    26
    >>> accumulate(add, 11, 0, identity) # 11
    11
    >>> accumulate(add, 11, 3, square)   # 11 + 1^2 + 2^2 + 3^2
    25
    >>> accumulate(mul, 2, 3, square)    # 2 * 1^2 * 2^2 * 3^2
    72
    >>> accumulate(lambda x, y: x + y + 1, 2, 3, square)
    19
    >>> accumulate(lambda x, y: 2 * (x + y), 2, 3, square) # 1^2 2^2 3^3
    58
    >>> accumulate(lambda x, y: (x + y) % 17, 19, 20, square)
    16
    """
    "*** YOUR CODE HERE ***"
    if n == 0: return base

    res = base

    for i in range(1,n+1):
        res = combiner(res, term(i))

    return res


def summation_using_accumulate(n, term):
    """Returns the sum of term(1) + ... + term(n). The implementation
    uses accumulate.

    >>> summation_using_accumulate(5, square)
    55
    >>> summation_using_accumulate(5, triple)
    45
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'summation_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"

    return accumulate(add, 0, 5, term)

def product_using_accumulate(n, term):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    >>> product_using_accumulate(6, triple)
    524880
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'product_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    return accumulate(mul, 1, n, term)


def compose1(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f
def make_repeater(func, n):
    """Return the function that computes the nth application of func.

    >>> add_three = make_repeater(increment, 3) #increment(increment(increment(5)))
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times!
    5
    """
    "*** YOUR CODE HERE ***"
    def repeat(x):
        res = x
        for _ in range(n):
            res = func(res)
        return res
    return repeat


def zero(f):
    return lambda x: x

def successor(n):
    return lambda f: lambda x: f(n(f)(x))

def one(f):
    """Church numeral 1: same as successor(zero)"""
    "*** YOUR CODE HERE ***"
    def fx(x):
        return f(x)
    return fx

def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    "*** YOUR CODE HERE ***"
    def ffx(x):
        return f(f(x))
    return ffx

three = successor(two)

def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    "*** YOUR CODE HERE ***"
    return n(lambda x: x+1)(0)

def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    "*** YOUR CODE HERE ***"
    return lambda f: lambda x: m(f)(n(f)(x))

def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    "*** YOUR CODE HERE ***"
    return lambda f: lambda x: m(n(f))(x)

def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    "*** YOUR CODE HERE ***"
    return lambda f: lambda x: n(m)(f)(x)


'''
Let's break down the successor function step by step:

python
Copy code
def successor(n):
    return lambda f: lambda x: f(n(f)(x))
Recall that a Church numeral n represents a function that takes another function f and an argument x and applies f to x n times. For example, the Church numeral two would apply the function f two times to x: f(f(x)).

Now let's say we have a Church numeral n and we want to find its successor. To do this, we need to apply the function f one more time to the result of n(f)(x). This is exactly what the successor function does:

python
Copy code
successor(n) = lambda f: lambda x: f(n(f)(x))
Let's take an example to understand how the successor function works. Suppose we have the Church numeral two, which is represented as lambda f: lambda x: f(f(x)). Now, we want to find the successor of two, which is three.

python
Copy code
successor(two)
The successor function returns lambda f: lambda x: f(two(f)(x)). To see the result of this operation, let's represent successor(two) as a Church numeral:

python
Copy code
lambda f: lambda x: f(two(f)(x))
Now let's apply a function f and an argument x to this expression:

python
Copy code
f(two(f)(x))
Recall that two(f)(x) = f(f(x)). Substitute this into the expression above:

python
Copy code
f(f(f(x)))
This is the Church numeral representation of three, as expected.

In summary, the successor function takes a Church numeral n and returns a new Church numeral representing the integer one greater than n. It does this by applying the function f one more time to the result of n(f)(x).

'''

'''
The add_church function indeed applies the function f m + n times to the value x. The key here is that m(f) is not applied to the result of n(f)(x) for m times. Instead, it applies the function f m times to the result of n(f)(x). In other words, it applies the function f n times first, and then it applies the function f m times to the result.

Let's analyze the expression m(f)(n(f)(x)) step by step:

n(f)(x): Apply the function f to the value x n times.
m(f): Returns a new function that applies the function f to its argument m times.
m(f)(n(f)(x)): Apply the function returned by m(f) to the result of n(f)(x). This effectively applies the function f m times to the result of applying the function f n times to x. Hence, the total number of times the function f is applied is m + n.
So, the add_church function does apply the function f m + n times to the value x, and not m * n times.


For the mul_church function, the operation is indeed m * n times.

Here's the code for mul_church:

def mul_church(m, n):
    return lambda f: lambda x: m(n(f))(x)
To understand why this represents m * n times, let's analyze the expression m(n(f))(x) step by step:

n(f): Returns a new function that applies the function f to its argument n times.
m(n(f)): Returns a new function that applies the function returned by n(f) to its argument m times. Since n(f) applies f n times, applying it m times means applying f m * n times.
m(n(f))(x): Apply the function returned by m(n(f)) to the value x. This effectively applies the function f m * n times to x.
So, the mul_church function applies the function f m * n times to the value x.
'''
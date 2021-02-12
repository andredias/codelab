class memoize(dict):

    def __init__(self, func):
        dict.__init__(self)
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


@memoize
def factorial(n):
    if n < 2:
        return n
    else:
        return n * factorial(n - 1)


def combination(n, k):
    return factorial(n) // factorial(n - k)


def permutation(n, k):
    return combination(n, k) // factorial(k)


print(factorial(5), combination(33, 6), permutation(33, 6))

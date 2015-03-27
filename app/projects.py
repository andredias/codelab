from hashlib import md5
from datetime import datetime
from functools import wraps
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from .core import run
from os.path import abspath, join, dirname


def pygmentize(code, language):
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter(linenos='table')
    return highlight(code, lexer, formatter)


LAST_VISITED_KEY = 'last_visited'
MOST_VISITED_KEY = 'most_visited'
MAX_HISTORY = 30


def _visited(cache, key):
    return [get_project(cache, project_id.decode())
            for project_id in cache._client.zrevrange(key, 0, MAX_HISTORY)
            if cache._client.exists(project_id)]


def last_visited(cache, languages):
    return _visited(cache, LAST_VISITED_KEY)


def most_visited(cache, languages):
    return _visited(cache, MOST_VISITED_KEY)


def project_id(source, language, input='', title='', description='', **kwargs):
    s = '{title}{description}{input}{source}{language}'.format(
        title=title, description=description, input=input, source=source, language=language,
    )
    return md5(s.encode('utf-8')).hexdigest()


def get_project(cache, id):
    project = cache.get(id)
    if project:
        redis = cache._client
        visits = redis.zscore(MOST_VISITED_KEY, id)
        visits = int(visits) if visits else 0
        last_visited = redis.zscore(LAST_VISITED_KEY, id)
        last_visited = datetime.fromtimestamp(last_visited) if last_visited else None
        project.update(visits=visits, last_visited=last_visited)
    return project


def cache_project(cache, project, timeout=None):
    if 'id' not in project:
        project['id'] = project_id(**project)
    output = run(project)
    project.update(output, created=datetime.utcnow())
    cache.set(project['id'], project, timeout)
    if not timeout:
        cache._client.persist(project['id'].encode())
    return


class count_visit(object):

    def __init__(self, cache):
        '''
        werkzeug.contrib.cache.RedisCache expected
        '''
        self.cache = cache
        self.redis = cache._client

    def last_visited(self):
        key = LAST_VISITED_KEY
        self.redis.zadd(key, self.project['id'], datetime.utcnow().timestamp())
        return

    def most_visited(self):
        key = MOST_VISITED_KEY
        self.redis.zincrby(key, self.project['id'].encode('utf-8'))
        return

    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # cache counting
            key = kwargs['id']
            if self.redis.exists(key):
                self.project = self.cache.get(key)
                self.last_visited()
                self.most_visited()
            return function(*args, **kwargs)
        return wrapper


def _read_snippet(filename, path=abspath(join(dirname(__file__), 'snippets'))):
    from os.path import join
    with open(join(path, filename)) as f:
        return f.read()

snippets = [

    {'title': 'Hello, world!',
     'language': 'python',
     'source': 'print("Hello, world!")\n', },

    # http://pythonfiddle.com/

    {'title': 'Chaining comparison operators',
     'language': 'python',
     'source': '''x = 5
print(1 < x < 10)
print(10 < x < 20)
print(x < 10 < (x * 10) < 100)
print(10 > x <= 9)
print(5 == x > 4)
''', },

    {'title': 'Decorators',
     'language': 'python',
     'source': '''def print_args(function):
    def wrapper(*args, **kwargs):
        print('Arguments:', args, kwargs)
        return function(*args, **kwargs)
    return wrapper


@print_args
def write(text):
    print(text)

write('foo')
''', },

    {'title': 'Generators',
     'language': 'python',
     'source': '''odds = (n for n in range(1, 20) if n % 2)
for n in odds:
    print(n)
''', },

    {'title': 'Enumerate',
     'language': 'python',
     'source': '''a = ['a', 'b', 'c', 'd', 'e']
for index, item in enumerate(a):
    print(index, item)
''', },

    {'title': 'Array Indexes',
     'language': 'python',
     'source': '''a = [1, 2, 3, 4, 5]
print(a[::2])  # iterate over the whole list in 2-increments
print(a[::-1])  # a useful idiom for 'x reversed'
''', },

    {'title': 'Arguments Unpacking',
     'language': 'python',
     'source': '''def draw_point(x, y):
    print(x, y)

point_foo = (3, 4)
point_bar = {'y': 3, 'x': 2}
draw_point(*point_foo)
draw_point(**point_bar)
''', },

    {'title': 'FizzBuzz',
     'language': 'python',
     'source': '''"""
Write a program that prints the numbers from 1 to 100.
But for multiples of three print "Fizz" instead of the number
and for the multiples of five print "Buzz".
For numbers which are multiples of both three and five print "FizzBuzz".

see: http://blog.codinghorror.com/why-cant-programmers-program/
"""

for x in range(1, 101):
    line = ''
    if x % 3 == 0:
        line += 'Fizz'
    if x % 5 == 0:
        line += 'Buzz'
    if not line:
        line = x
    print(line)
''', },

    {'title': 'Memoize decorator, factorial, combination and permutation',
     'language': 'python',
     'source': '''class memoize(dict):
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
''', },


    {'title': 'Hello, world!',
     'language': 'c',
     'source': r'''#include <stdio.h>

int main() {
    printf("Hello, world!");
    return 0;
}
''', },


    {'title': 'Hello, world!',
     'language': 'c++',
     'source': '''#include <iostream>

int main() {
    std::cout << "Hello, world!";
    return 0;
}
''', },

    {'title': 'Hello, world!',
     'language': 'csharp',
     'source': '''using System;

class Program {

    public static void Main(string[] args) {
        Console.WriteLine("Hello, world!");
    }

}''', },

    {'title': 'Hello, world!',
     'language': 'go',
     'source': '''package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}''', },


    {'title': 'Hello, world!',
     'language': 'java',
     'source': '''public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}''', },

    {'title': 'Hello, world!',
     'language': 'javascript',
     'source': '''console.log('Hello, world!')
''', },

    {'title': 'FizzBuzz',
     'language': 'javascript',
     'source': '''/*
Write a program that prints the numbers from 1 to 100.
But for multiples of three print "Fizz" instead of the number
and for the multiples of five print "Buzz".
For numbers which are multiples of both three and five print "FizzBuzz".

see: http://blog.codinghorror.com/why-cant-programmers-program/
*/

for (var i = 1; i <= 100; i++) {
    var string = '';

    if (i % 3 === 0) {
        string += 'Fizz';
    }

    if (i % 5 === 0) {
        string += 'Buzz';
    }

    // If `string` is empty, `i` is not divisible
    // by 3 or 5, so use the number instead.
    if (string === '') {
        string = parseInt(i);
    }

    console.log(string);
}
''', },

    {'title': 'Hello, world!',
     'language': 'ruby',
     'source': '''puts 'Hello, world!'
''', },

    {'title': 'Faculdade',
     'language': 'sqlite',
     'source': _read_snippet('sqlite.sql'),
     },

    {'title': 'Mercurial Named Branches',
     'description': 'This example shows how Mercurial named branches \
keep a faithful record of the history of a branch.',
     'language': 'bash',
     'source': _read_snippet('ramos_nomeados.sh'),
     },

     {'title': 'Hello, world!',
      'language': 'bash',
      'source': "echo 'Hello, world!'",
      },

]

for project in snippets:
    project['id'] = project_id(**project)


def cache_snippets(cache):
    for project in snippets:
        cache_project(cache, project)
    return

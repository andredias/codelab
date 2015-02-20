from .core import cache_project, project_id

snippets = [

    {'title': 'Hello, world!',
     'language': 'python',
     'source': 'print("Hello world")\n', },

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
    printf("Hello, world!\n");
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

]

for project in snippets:
    project['id'] = project_id(**project)


def cache_snippets(cache):
    for project in snippets:
        cache_project(cache, project)
    return


from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def pygmentize(code, language):
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter(linenos='table')
    return highlight(code, lexer, formatter)

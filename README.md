# OJ – Oliver's JSON Parser

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Based on [Phil Eaton's tutorial](http://notes.eatonphil.com/writing-a-simple-json-parser.html).

## Features

Parsing:
  - [x] nulls
  - [x] booleans
  - [x] numbers
    - [x] integers
    - [x] floats
    - [x] exponents (e.g. 2.4e5)
    - [x] NaN (not in the JSON spec, but supported by Python)
    - [x] +/- Infinity (not in the JSON spec, but supported by Python)
  - [x] strings
    - [x] escape characters
    - [x] hex characters (e.g. "\u00ff")
  - [x] objects
  - [x] lists
Validation:
  - [x] oj.loads raises an exception for an input x iff json.loads does
  - [ ] line and column for exceptions

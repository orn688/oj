# OJ – Oliver's JSON Parser

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Based on [Phil Eaton's tutorial](http://notes.eatonphil.com/writing-a-simple-json-parser.html).

## Features

Parsing:

- [x] nulls
- [x] booleans
- [ ] numbers
  - [ ] exponents (e.g. 2.4e5)
  - [ ] NaN (not in the JSON spec, but supported by Python)
  - [ ] +/- Infinity (not in the JSON spec, but supported by Python)
- [x] strings
  - [x] unicode characters (e.g. "\u00ff")
- [x] objects
- [x] lists

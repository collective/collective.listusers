#!/bin/bash

echo 'Running tests'
bin/test -s collective.listusers

echo '====== Running PyFlakes ======'
bin/pyflakes collective/listusers
bin/pyflakes setup.py

echo '====== Running pep8 =========='
bin/pep8 collective/listusers
bin/pep8 setup.py

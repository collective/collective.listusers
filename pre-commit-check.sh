#!/bin/bash

echo 'Running tests'
bin/test -s collective.listusers

echo '====== Running ZPTLint ======'
for pt in `find collective/listusers/ -name "*.pt"` ; do bin/zptlint $pt; done

echo '====== Running PyFlakes ======'
bin/pyflakes collective/listusers
bin/pyflakes setup.py

echo '====== Running pep8 =========='
bin/pep8 collective/listusers --ignore=E501
bin/pep8 setup.py

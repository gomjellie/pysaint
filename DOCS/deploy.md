
python setup.py build
python setup.py sdist bdist_wheel

twine upload dist/pysaint-1.*.*.tar.gz


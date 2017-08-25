rm -rf dist hyper2web.egg-info
python setup.py sdist
twine upload dist/*
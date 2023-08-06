rm -rf dist
python setup.py sdist bdist_wheel
git add . && git commit -m "$@"
twine check dist/* && cat ../pypi_creds.txt | twine upload dist/*
git push -u origin main

# dlai_tools

A set of tools for the deeplearning organization. 

Deploy setup to test.pypi:

```
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
# Test
python3 -m twine upload --repository testpypi dist/*
# Production
python setup.py sdist upload -r pypi
python3 -m twine upload dist/*
```

Now you must have a entry in the index of https://test.pypi.org/project/dlai-tools/

## Install

```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps dlai_tools
```

## Use

```
from dlai_tools import deploy_assignment

deploy_assignment('example_Dev.ipynb', True)
```
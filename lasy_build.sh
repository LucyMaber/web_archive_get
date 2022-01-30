#!/bin/bash
pip uninstall web_archive_get
python setup.py bdist_wheel
pip install .
# twine upload --skip-existing dist/*
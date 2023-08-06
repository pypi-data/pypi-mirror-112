# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niteru']

package_data = \
{'': ['*']}

install_requires = \
['poetry-version>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'niteru',
    'version': '0.2.0',
    'description': 'A set of similarity metrics to compare html files',
    'long_description': '# niteru\n\n[![PyPI version](https://badge.fury.io/py/niteru.svg)](https://badge.fury.io/py/niteru)\n[![Python CI](https://github.com/ninoseki/niteru/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/niteru/actions/workflows/test.yml)\n[![Coverage Status](https://coveralls.io/repos/github/ninoseki/niteru/badge.svg?branch=main)](https://coveralls.io/github/ninoseki/niteru?branch=main)\n[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://ninoseki.github.io/niteru/)\n\nThis package provides a set of functions to measure the similarity between HTMLs.\n\n**Note**: This is a fork of [html-similarity](https://github.com/matiskay/html-similarity).\n\n## Key differences\n\n- Type hints\n  - All functions have proper type hints\n- Dependency free\n  - Works along with plain Python\n\n## Installation\n\n```bash\npip install niteru\n```\n\n## How it works\n\n### Structural Similarity\n\nUses sequence comparison of the html tags to compute the similarity.\n\nWe do not implement the similarity based on tree edit distance because it is slower than sequence comparison.\n\n### Style Similarity\n\nExtracts CSS classes of each html document and calculates the jaccard similarity of the sets of classes.\n\n### Joint Similarity (Structural Similarity and Style Similarity)\n\nThe joint similarity metric is calculated as::\n\n```python\nk * structural_similarity(html1, html2) + (1 - k) * style_similarity(html1, html2)\n```\n\nAll the similarity metrics take values between 0.0 and 1.0.\n\n### Recommendations for joint similarity\n\nUsing `k=0.3` gives better results. The style similarity gives more information about the similarity rather than the structural similarity.\n\n## Examples\n\nHere is an example:\n\n```python\nhtml1 = \'\'\'\n<h1 class="title">First Document</h1>\n<ul class="menu">\n  <li class="active">Documents</li>\n  <li>Extra</li>\n</ul>\n \'\'\'\n\nhtml2 = \'\'\'\n<h1 class="title">Second document Document</h1>\n<ul class="menu">\n  <li class="active">Extra Documents</li>\n</ul>\n\'\'\'\n\nfrom niteru import style_similarity, structural_similarity, similarity\n\nstyle_similarity(html1, html2) # => 1.0\nstructural_similarity(html1, html2) # => 0.8571428571428571\nsimilarity(html1, html2) # => 0.9285714285714286\n```\n',
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninoseki/niteru',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

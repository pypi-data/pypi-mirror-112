# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfa_identify']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.0.0,<22.0.0',
 'bidict>=0.21.2,<0.22.0',
 'dfa>=2.1.2,<3.0.0',
 'funcy>=1.15,<2.0',
 'networkx>=2.5.1,<3.0.0',
 'python-sat>=0.1.7-alpha.2,<0.2.0']

setup_kwargs = {
    'name': 'dfa-identify',
    'version': '1.0.2',
    'description': 'Python library for identifying (learning) DFAs (automata) from labeled examples.',
    'long_description': '# dfa-identify\nPython library for identifying (learning) DFAs from labeled examples\nby reduction to SAT.\n\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/dfa-identify/status.svg)](https://cloud.drone.io/mvcisback/dfa-identify)\n[![PyPI version](https://badge.fury.io/py/dfa_identify.svg)](https://badge.fury.io/py/dfa_identify)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n<!-- markdown-toc start - Don\'t edit this section. Run M-x markdown-toc-refresh-toc -->\n**Table of Contents**\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [Encoding](#encoding)\n\n<!-- markdown-toc end -->\n\n\n# Installation\n\nIf you just need to use `dfa`, you can just run:\n\n`$ pip install dfa`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\n`dfa_identify` is centered around the `find_dfa` and `find_dfas` function. Both take in\nsequences of accepting and rejecting "words", where are word is a\nsequence of arbitrary python objects. \n\n1. `find_dfas` returns all minimally sized (no `DFA`s exist of size\nsmaller) consistent with the given labeled data.\n\n2. `find_dfa` returns an arbitrary (first) minimally sized `DFA`.\n\nThe returned `DFA` object is from the [dfa](https://github.com/mvcisback/dfa) library.\n\n\n```python\nfrom dfa_identify import find_dfa\n\n\naccepting = [\'a\', \'abaa\', \'bb\']\nrejecting = [\'abb\', \'b\']\n    \nmy_dfa = find_dfa(accepting=accepting, rejecting=rejecting)\n\nassert all(my_dfa.label(x) for x in accepting)\nassert all(not my_dfa.label(x) for x in rejecting)\n```\n\nBecause words are sequences of arbitrary python objects, the\nidentification problem, with `a` ↦ 0 and `b` ↦ 1, is given below:\n\n\n```python\naccepting = [[0], [0, \'z\', 0, 0], [\'z\', \'z\']]\nrejecting = [[0, \'z\', \'z\'], [\'z\']]\n\nmy_dfa = find_dfa(accepting=accepting, rejecting=rejecting)\n```\n\n# Encoding\n\nThis library currently uses the encodings outlined in [Heule, Marijn JH, and Sicco Verwer. "Exact DFA identification using SAT solvers." International Colloquium on Grammatical Inference. Springer, Berlin, Heidelberg, 2010.](https://link.springer.com/chapter/10.1007/978-3-642-15488-1_7) and [Ulyantsev, Vladimir, Ilya Zakirzyanov, and Anatoly Shalyto. "Symmetry Breaking Predicates for SAT-based DFA Identification."](https://arxiv.org/abs/1602.05028).\n\nThe key difference is in the use of the symmetry breaking clauses. Two kinds are exposed.\n\n1. clique (Heule 2010): Partially breaks symmetries by analyzing\n   conflict graph.\n2. bfs (Ulyantsev 2016): Breaks all symmetries so that each model corresponds to a unique DFA.\n',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/dfa-identify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

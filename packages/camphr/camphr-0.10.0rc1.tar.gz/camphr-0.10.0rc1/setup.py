# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camphr',
 'camphr.ner_labels',
 'camphr.tokenizer',
 'camphr.tokenizer.juman',
 'camphr.tokenizer.mecab',
 'camphr.tokenizer.sentencepiece']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'dataclass-utils>=0.7.12,<0.8.0',
 'dataclasses>=0.6,<0.7',
 'more-itertools>=8.8,<9.0',
 'pytextspan>=0.5.0,<1.0',
 'pytokenizations>=0.4.8,<1.0',
 'toolz>=0.10,<0.12',
 'typing-extensions>=3.7.4']

extras_require = \
{'all': ['sentencepiece>=0.1.96,<0.2.0',
         'mojimoji>=0.0.11,<0.0.12',
         'pyknp>=0.4.2,<0.5',
         'mecab-python3>=1.0,<1.1'],
 'juman': ['mojimoji>=0.0.11,<0.0.12', 'pyknp>=0.4.2,<0.5'],
 'mecab': ['mecab-python3>=1.0,<1.1'],
 'sentencepiece': ['sentencepiece>=0.1.96,<0.2.0']}

entry_points = \
{'console_scripts': ['camphr = camphr.cli.__main__:main']}

setup_kwargs = {
    'name': 'camphr',
    'version': '0.10.0rc1',
    'description': 'spaCy plugin for Transformers, Udify, Elmo, etc.',
    'long_description': '<p align="center"><img src="https://raw.githubusercontent.com/PKSHATechnology-Research/camphr/master/img/logoc.svg?sanitize=true" width="200" /></p>\n\n# Camphr - spaCy plugin for Transformers, Udify, Elmo, etc.\n\n[![Documentation Status](https://readthedocs.org/projects/camphr/badge/?version=latest)](https://camphr.readthedocs.io/en/latest/?badge=latest)\n[![Gitter](https://badges.gitter.im/camphr/community.svg)](https://gitter.im/camphr/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n[![PyPI version](https://badge.fury.io/py/camphr.svg)](https://badge.fury.io/py/camphr)\n![test and publish](https://github.com/PKSHATechnology-Research/camphr/workflows/test%20and%20publish/badge.svg)\n![](https://github.com/PKSHATechnology-Research/camphr/workflows/test%20extras/badge.svg)\n![](https://github.com/PKSHATechnology-Research/camphr/workflows/test%20package/badge.svg)\n\nCamphr is a *Natural Language Processing* library that helps in seamless integration for a wide variety of techniques from state-of-the-art to conventional ones.\nYou can use [Transformers](https://huggingface.co/transformers/) ,  [Udify](https://github.com/Hyperparticle/udify), [ELmo](https://allennlp.org/elmo), etc. on [spaCy](https://github.com/explosion/spaCy).\n\nCheck the [documentation](https://camphr.readthedocs.io/en/latest/) for more information.\n\n(For Japanese: https://qiita.com/tamurahey/items/53a1902625ccaac1bb2f)\n\n# Features\n\n- A [spaCy](https://github.com/explosion/spaCy) plugin - Easily integration for a wide variety of methods\n- [Transformers](https://huggingface.co/transformers/) with spaCy - Fine-tuning pretrained model with [Hydra](https://hydra.cc/). Embedding vector\n- [Udify](https://github.com/Hyperparticle/udify) - BERT based multitask model in 75 languages\n- [Elmo](https://allennlp.org/elmo) - Deep contextualized word representations\n- Rule base matching with Aho-Corasick, Regex\n- (for Japanese) KNP\n\n# License\n\nCamphr is licensed under [Apache 2.0](./LICENSE).\n\n',
    'author': 'tamuhey',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PKSHATechnology-Research/camphr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

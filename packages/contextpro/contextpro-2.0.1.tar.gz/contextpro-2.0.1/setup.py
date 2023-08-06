# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextpro']

package_data = \
{'': ['*']}

install_requires = \
['contractions>=0.0.48,<0.0.49',
 'nltk>=3.5,<4.0',
 'pandas>=1.1.5,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'spacy>=3.0.5,<4.0.0',
 'textblob>=0.15.3,<0.16.0',
 'toml>=0.10.2,<0.11.0',
 'wheel>=0.36.2,<0.37.0',
 'word2number>=1.1,<2.0']

setup_kwargs = {
    'name': 'contextpro',
    'version': '2.0.1',
    'description': 'Python library for concurrent text preprocessing',
    'long_description': '# contextpro\n\n[![pipeline status](https://gitlab.com/elzawie/contextpro/badges/master/pipeline.svg)](https://gitlab.com/elzawie/contextpro/-/commits/master)\n[![coverage report](https://gitlab.com/elzawie/contextpro/badges/master/coverage.svg)](https://gitlab.com/elzawie/contextpro/-/commits/master)\n[![License](https://img.shields.io/badge/license-MIT-blue)](https://gitlab.com/elzawie/contextpro/-/blob/master/LICENSE)\n\n\ncontextpro is a Python library for concurrent text preprocessing using functions from some well-known NLP packages including NLTK, spaCy and TextBlob.\n\n- **Documentation:** https://contextpro.readthedocs.io/en/latest/\n- **Source code:** https://gitlab.com/elzawie/contextpro\n\n## Installation\n\n Windows / OS X / Linux:\n\n-  Installation with pip\n\n    ```\n    pip install contextpro\n    python -m spacy download en_core_web_sm\n    ```\n\n- Installation with poetry\n    ```\n    poetry add contextpro\n    python -m spacy download en_core_web_sm\n    ```\n\n## Configuration\n\n- Before using the package, execute the below commands in your virtual environment:\n\n    ```python\n    import nltk\n\n    nltk.download("punkt")\n    nltk.download("stopwords")\n    nltk.download("wordnet")\n    ```\n\n## Usage examples\n```python\nfrom contextpro.normalization import batch_replace_contractions\n\ncorpus = [\n    "I don\'t want to be rude, but you shouldn\'t do this",\n    "Do you think he\'ll pass his driving test?",\n    "I\'ll see you next week",\n    "I\'m going for a walk"\n]\n\nbatch_replace_contractions(corpus)\n\n[\n    "I do not want to be rude, but you should not do this",\n    "Do you think he will pass his driving test?",\n    "I will see you next week",\n    "I am going for a walk",\n]\n```\n```python\nfrom contextpro.normalization import batch_remove_stopwords\n\ncorpus = [\n    [\'My\', \'name\', \'is\', \'Dr\', \'Jekyll\'],\n    [\'His\', \'name\', \'is\', \'Mr\', \'Hyde\'],\n    [\'This\', \'guy\', \'s\', \'name\', \'is\', \'Edward\', \'Scissorhands\'],\n    [\'And\', \'this\', \'is\', \'Tom\', \'Parker\']\n]\n\nbatch_remove_stopwords(corpus)\n\n[\n    [\'My\', \'name\', \'Dr\', \'Jekyll\'],\n    [\'His\', \'name\', \'Mr\', \'Hyde\'],\n    [\'This\', \'guy\', \'name\', \'Edward\', \'Scissorhands\'],\n    [\'And\', \'Tom\', \'Parker\']\n]\n```\n```python\nfrom contextpro.normalization import batch_lemmatize\n\ncorpus =  [\n    ["I", "like", "driving", "a", "car"],\n    ["I", "am", "going", "for", "a", "walk"],\n    ["What", "are", "you", "doing"],\n    ["Where", "are", "you", "coming", "from"]\n]\n\nbatch_lemmatize(corpus, num_workers=2, pos="v")\n\n[\n    [\'I\', \'like\', \'drive\', \'a\', \'car\'],\n    [\'I\', \'be\', \'go\', \'for\', \'a\', \'walk\'],\n    [\'What\', \'be\', \'you\', \'do\'],\n    [\'Where\', \'be\', \'you\', \'come\', \'from\']\n]\n```\n```python\nfrom contextpro.normalization import batch_convert_numerals_to_numbers\n\ncorpus = [\n    "A bunch of five",\n    "A picture is worth a thousand words",\n    "A stitch in time saves nine",\n    "Back to square one",\n    "Behind the eight ball",\n    "Between two stools",\n]\n\nbatch_convert_numerals_to_numbers(corpus, num_workers=2)\n\n[\n    \'A bunch of 5\',\n    \'A picture is worth a 1000 words\',\n    \'A stitch in time saves 9\',\n    \'Back to square 1\',\n    \'Behind the 8 ball\',\n    \'Between 2 stools\',\n]\n```\n```python\nfrom contextpro.statistics import batch_calculate_corpus_statistics\n\ncorpus = [\n    "My name is Dr. Jekyll.",\n    "His name is Mr. Hyde",\n    "This guy\'s name is Edward Scissorhands",\n    "And this is Tom Parker"\n]\n\nbatch_calculate_corpus_statistics(\n    corpus,\n    lowercase=False,\n    remove_stopwords=False,\n    num_workers=2,\n)\n\n    characters  tokens  punctuation_characters  digits  whitespace_characters  \\\n0          22       5                       2       0                      4\n1          20       5                       1       0                      4\n2          38       7                       1       0                      5\n3          22       5                       0       0                      4\n\n        ascii_characters  sentiment_score  subjectivity_score\n0                22              0.0                 0.0\n1                20              0.0                 0.0\n2                38              0.0                 0.0\n3                22              0.0                 0.0\n```\n\n## Release History\n* https://gitlab.com/elzawie/contextpro/-/releases\n\n## Meta\nŁukasz Zawieska – zawieskal@yahoo.com\n\n<a href="https://gitlab.com/elzawie/">Gitlab account</a>\n\n<a href="https://github.com/elzawie/">Github account</a>\n\nDistributed under the MIT license. See <a href="https://gitlab.com/elzawie/contextpro/-/blob/master/LICENSE">LICENSE</a> for more information.\n',
    'author': 'Łukasz Zawieska',
    'author_email': 'zawieskal@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/elzawie/contextpro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

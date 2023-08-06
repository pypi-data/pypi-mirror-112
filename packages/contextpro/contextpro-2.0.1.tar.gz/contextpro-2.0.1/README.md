# contextpro

[![pipeline status](https://gitlab.com/elzawie/contextpro/badges/master/pipeline.svg)](https://gitlab.com/elzawie/contextpro/-/commits/master)
[![coverage report](https://gitlab.com/elzawie/contextpro/badges/master/coverage.svg)](https://gitlab.com/elzawie/contextpro/-/commits/master)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://gitlab.com/elzawie/contextpro/-/blob/master/LICENSE)


contextpro is a Python library for concurrent text preprocessing using functions from some well-known NLP packages including NLTK, spaCy and TextBlob.

- **Documentation:** https://contextpro.readthedocs.io/en/latest/
- **Source code:** https://gitlab.com/elzawie/contextpro

## Installation

 Windows / OS X / Linux:

-  Installation with pip

    ```
    pip install contextpro
    python -m spacy download en_core_web_sm
    ```

- Installation with poetry
    ```
    poetry add contextpro
    python -m spacy download en_core_web_sm
    ```

## Configuration

- Before using the package, execute the below commands in your virtual environment:

    ```python
    import nltk

    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    ```

## Usage examples
```python
from contextpro.normalization import batch_replace_contractions

corpus = [
    "I don't want to be rude, but you shouldn't do this",
    "Do you think he'll pass his driving test?",
    "I'll see you next week",
    "I'm going for a walk"
]

batch_replace_contractions(corpus)

[
    "I do not want to be rude, but you should not do this",
    "Do you think he will pass his driving test?",
    "I will see you next week",
    "I am going for a walk",
]
```
```python
from contextpro.normalization import batch_remove_stopwords

corpus = [
    ['My', 'name', 'is', 'Dr', 'Jekyll'],
    ['His', 'name', 'is', 'Mr', 'Hyde'],
    ['This', 'guy', 's', 'name', 'is', 'Edward', 'Scissorhands'],
    ['And', 'this', 'is', 'Tom', 'Parker']
]

batch_remove_stopwords(corpus)

[
    ['My', 'name', 'Dr', 'Jekyll'],
    ['His', 'name', 'Mr', 'Hyde'],
    ['This', 'guy', 'name', 'Edward', 'Scissorhands'],
    ['And', 'Tom', 'Parker']
]
```
```python
from contextpro.normalization import batch_lemmatize

corpus =  [
    ["I", "like", "driving", "a", "car"],
    ["I", "am", "going", "for", "a", "walk"],
    ["What", "are", "you", "doing"],
    ["Where", "are", "you", "coming", "from"]
]

batch_lemmatize(corpus, num_workers=2, pos="v")

[
    ['I', 'like', 'drive', 'a', 'car'],
    ['I', 'be', 'go', 'for', 'a', 'walk'],
    ['What', 'be', 'you', 'do'],
    ['Where', 'be', 'you', 'come', 'from']
]
```
```python
from contextpro.normalization import batch_convert_numerals_to_numbers

corpus = [
    "A bunch of five",
    "A picture is worth a thousand words",
    "A stitch in time saves nine",
    "Back to square one",
    "Behind the eight ball",
    "Between two stools",
]

batch_convert_numerals_to_numbers(corpus, num_workers=2)

[
    'A bunch of 5',
    'A picture is worth a 1000 words',
    'A stitch in time saves 9',
    'Back to square 1',
    'Behind the 8 ball',
    'Between 2 stools',
]
```
```python
from contextpro.statistics import batch_calculate_corpus_statistics

corpus = [
    "My name is Dr. Jekyll.",
    "His name is Mr. Hyde",
    "This guy's name is Edward Scissorhands",
    "And this is Tom Parker"
]

batch_calculate_corpus_statistics(
    corpus,
    lowercase=False,
    remove_stopwords=False,
    num_workers=2,
)

    characters  tokens  punctuation_characters  digits  whitespace_characters  \
0          22       5                       2       0                      4
1          20       5                       1       0                      4
2          38       7                       1       0                      5
3          22       5                       0       0                      4

        ascii_characters  sentiment_score  subjectivity_score
0                22              0.0                 0.0
1                20              0.0                 0.0
2                38              0.0                 0.0
3                22              0.0                 0.0
```

## Release History
* https://gitlab.com/elzawie/contextpro/-/releases

## Meta
Łukasz Zawieska – zawieskal@yahoo.com

<a href="https://gitlab.com/elzawie/">Gitlab account</a>

<a href="https://github.com/elzawie/">Github account</a>

Distributed under the MIT license. See <a href="https://gitlab.com/elzawie/contextpro/-/blob/master/LICENSE">LICENSE</a> for more information.

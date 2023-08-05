from .parser import Parser

from typing import Union
from pathlib import Path

from itertools import chain
from collections import Counter


class Statist:
    def __init__(self, inputs: Union[str, list]):
        self.corpus: list = self.make_corpus(inputs)
        self.corpus_str: str = ''.join(self.corpus)
        self.parser = Parser()

    def make_corpus(self, inputs: Union[str, list]) -> list:
        if type(inputs) == list:
            corpus = inputs
        elif type(inputs) == str:
            if Path(inputs).exists():
                corpus = Path(inputs).open('r').readlines()
            else:
                corpus = inputs.splitlines()
        else:
            raise TypeError(f'only `str` or `list` type is valid, but {type(inputs)} was given.')

        return corpus

    def all_stats(self, verbose=False) -> dict:
        word_stats = self.calc_word_stats(verbose)
        char_stats = self.calc_char_stats(verbose)

        return dict(
            word_stats=word_stats,
            char_stats=char_stats
        )

    def calc_word_stats(self, verbose=False) -> dict:
        c = Counter(self.parser.get_surfaces(self.corpus_str))

        if verbose:
            print(c)

        return dict(
            num_token=sum(c.values()),
            num_vocab=len(c.keys())
        )

    def calc_char_stats(self, verbose=False) -> dict:
        c = Counter(self.corpus_str)

        if verbose:
            print(c)

        return dict(
            num_token=sum(c.values()),
            num_vocab=len(c.keys())
        )

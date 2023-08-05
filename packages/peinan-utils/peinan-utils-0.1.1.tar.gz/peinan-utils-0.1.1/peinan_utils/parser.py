import re
from typing import List

import MeCab
import ipadic


class Parser:
    def __init__(self) -> None:
        self.feature_columns = [
            '品詞', '品詞細分類1', '品詞細分類2', '品詞細分類3',
            '活用型', '活用形', '基本形', '読み', '発音',
        ]
        self.stopwords = []
        self.content_pos = ['名詞', '動詞', '形容詞', '副詞', '連体詞']
        self.eos = ['。', '？', '！', '．', '\?', '\!']
        self.ptn_eos = re.compile(f'({"|".join(self.eos)})')

        self.mecab_args = ipadic.MECAB_ARGS
        self.tagger = MeCab.Tagger(self.mecab_args)

    def set_args(self, mecab_args: str, is_dict_path: bool = False) -> None:
        """
        Specify the dictionary path

        :param mecab_args:
            Ubuntu Env Example
                IPADic: See https://github.com/polm/ipadic-py#usage
                Neologd: -r/dev/null -d /usr/lib/mecab/dic/mecab-ipadic-neologd
        :param is_dict_path:
            activate if the mecab_args is dict path
        :return:
        """

        if is_dict_path:
            self.mecab_args = '-r/dev/null -d ' + mecab_args

        self.tagger = MeCab.Tagger(self.mecab_args)

    def set_stopwords(self, stopwords: list) -> None:
        self.stopwords = stopwords

    def set_content_pos(self, content_pos: list) -> None:
        self.content_pos = content_pos

    def set_eos(self, eos: list) -> None:
        self.eos = eos

    def parse(self, text: str, only_content_words: bool = False, fit_stopwords: bool = False) -> List[dict]:
        results = []
        for node in self.tagger.parse(text).rstrip('\n').splitlines():
            if node == 'EOS' or node == '':
                continue

            surface, feature = node.split('\t')
            features = feature.split(',')

            if only_content_words:
                if features[0] in self.content_pos:
                    results.append({'surface': surface, 'features': features})
            elif fit_stopwords:
                if surface not in self.stopwords:
                    results.append({'surface': surface, 'features': features})
            else:
                results.append({'surface': surface, 'features': features})

        return results

    def get_surfaces(self, text: str, only_content_words: bool = False, fit_stopwords: bool = False) -> List[str]:
        return [ res['surface'] for res in self.parse(text,
                                                      only_content_words=only_content_words,
                                                      fit_stopwords=fit_stopwords) ]

    def split_to_lines(self, text: str) -> List[str]:
        return re.sub(self.ptn_eos, '\g<1>\n', text.replace('\n', '').rstrip()).splitlines()


if __name__ == '__main__':
    from pathlib import Path
    from icecream import ic
    sample_lines = (Path(__file__).parent / '../sample.txt').open('r').readlines()
    sample_text = 'こんにちは！今日はいい天気ですね。これからどちらへ？すもももももももものうち'

    p = Parser()
    ic(sample_text)
    ic(p.parse(sample_text))
    ic(p.get_surfaces(sample_text))
    ic(p.get_surfaces(sample_text, only_content_words=True))
    ic(p.split_to_lines(sample_text))

    p.set_args('/usr/local/lib/mecab/dic/mecab-ipadic-neologd', is_dict_path=True)
    ic(p.get_surfaces(sample_text))

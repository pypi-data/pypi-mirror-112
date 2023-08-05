# An util package for myself

![](https://img.shields.io/badge/version-0.1.1-green.svg?style=flat-square) ![](https://img.shields.io/badge/python-3.6+-green.svg?style=flat-square) ![](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)

Mostly about NLP.

## Install

```bash
pip install peinan-utils
```

## Usages & Features

### Parser

```python
# sample text
>>> text = 'こんにちは！今日はいい天気ですね。これからどちらへ？'

>>> from peinan_utils import Parser
>>> p = Parser()

# just parse input texts and get information about surfaces and features
>>> p.parse(text)
[{'surface': 'こんにちは',
  'features': ['感動詞', '*', '*', '*', '*', '*', 'こんにちは', 'コンニチハ', 'コンニチワ']},
 {'surface': '！', 'features': ['記号', '一般', '*', '*', '*', '*', '！', '！', '！']},
 {'surface': '今日',
  'features': ['名詞', '副詞可能', '*', '*', '*', '*', '今日', 'キョウ', 'キョー']},
 {'surface': 'は',
  'features': ['助詞', '係助詞', '*', '*', '*', '*', 'は', 'ハ', 'ワ']},
 {'surface': 'いい',
  'features': ['形容詞', '自立', '*', '*', '形容詞・イイ', '基本形', 'いい', 'イイ', 'イイ']},
 {'surface': '天気',
  'features': ['名詞', '一般', '*', '*', '*', '*', '天気', 'テンキ', 'テンキ']},
 {'surface': 'です',
  'features': ['助動詞', '*', '*', '*', '特殊・デス', '基本形', 'です', 'デス', 'デス']},
 {'surface': 'ね',
  'features': ['助詞', '終助詞', '*', '*', '*', '*', 'ね', 'ネ', 'ネ']},
 {'surface': '。', 'features': ['記号', '句点', '*', '*', '*', '*', '。', '。', '。']},
 {'surface': 'これから',
  'features': ['副詞', '助詞類接続', '*', '*', '*', '*', 'これから', 'コレカラ', 'コレカラ']},
 {'surface': 'どちら',
  'features': ['名詞', '代名詞', '一般', '*', '*', '*', 'どちら', 'ドチラ', 'ドチラ']},
 {'surface': 'へ',
  'features': ['助詞', '格助詞', '一般', '*', '*', '*', 'へ', 'ヘ', 'エ']},
 {'surface': '？', 'features': ['記号', '一般', '*', '*', '*', '*', '？', '？', '？']}]

# get surfaces of input text
>>> p.get_surfaces(text)
['こんにちは', '！', '今日', 'は', 'いい', '天気', 'です', 'ね', '。', 'これから', 'どちら', 'へ', '？']

# get only content words of input text
>>> p.get_surfaces(text, only_content_words=True)
['今日', 'いい', '天気', 'これから', 'どちら']

# split input text into lines
>>> p.split_to_lines(text)
['こんにちは！', '今日はいい天気ですね。', 'これからどちらへ？']

# change dictonary path
>>> sumomo = 'すもももももももものうち'
>>> p.get_surfaces(sumomo)
['すもも', 'も', 'もも', 'も', 'もも', 'の', 'うち']

>>> p.set_dict('/usr/local/lib/mecab/dic/mecab-ipadic-neologd', is_dict_path=True)
>>> p.get_surfaces(sumomo)
['すもももももももものうち']
```

### Vectorizer

```python
# sample text
>>> text = '今日はいい天気ですね。これからどちらへ？'

>>> from peinan_utils import Vectorizer
>>> v = Vectorizer()

# make word ngram (the default n is 2)
>>> v.make_word_ngram(text)
[[('今日', 'は'), ('は', 'いい'), ('いい', '天気'), ('天気', 'です'), ('です', 'ね'), ('ね', '。')], [('これから', 'どちら'), ('どちら', 'へ'), ('へ', '？')]]

# specify n
>>> v.make_word_ngram(text, n=3)
[[('今日', 'は', 'いい'), ('は', 'いい', '天気'), ('いい', '天気', 'です'), ('天気', 'です', 'ね'), ('です', 'ね', '。')], [('これから', 'どちら', 'へ'), ('どちら', 'へ', '？')]]

# use BOS and EOS (the default BOS and EOS are '<s>' and </s>, respectively)
>>> v.make_word_ngram(text, n=3, bos=v.BOS, eos=v.EOS)
[[('<s>', '今日', 'は'), ('今日', 'は', 'いい'), ('は', 'いい', '天気'), ('いい', '天気', 'です'), ('天気', 'です', 'ね'), ('です', 'ね', '。'), ('ね', '。', '</s>')], [('<s>', 'これから', 'どちら'), ('これから', 'どちら', 'へ'), ('どちら', 'へ', '？'), ('へ', '？', '</s>')]]

# make character ngram (the default n is 2)
>>> v.make_char_ngram(text, n=2)
[[('今', '日'), ('日', 'は'), ('は', 'い'), ('い', 'い'), ('い', '天'), ('天', '気'), ('気', 'で'), ('で', 'す'), ('す', 'ね'), ('ね', '。')], [('こ', 'れ'), ('れ', 'か'), ('か', 'ら'), ('ら', 'ど'), ('ど', 'ち'), ('ち', 'ら'), ('ら', 'へ'), ('へ', '？')]]
```

### Statist

sample.txt

```
あのイーハトーヴォのすきとおった風、夏でも底に冷たさをもつ青いそら、うつくしい森で飾られたモリーオ市、 郊外のぎらぎらひかる草の波。
またそのなかでいっしょになったたくさんのひとたち、ファゼーロとロザーロ、羊飼のミーロや、顔の赤いこども たち、地主のテーモ、山猫博士のボーガント・デストゥパーゴなど、いまこの暗い巨きな石の建物のなかで考えて いると、みんなむかし風のなつかしい青い幻燈のように思われます。
では、わたくしはいつかの小さなみだしをつけながら、しずかにあの年のイーハトーヴォの五月から十月までを書 きつけましょう。
```

```python
In : from peinan_utils import Statist
In : s = Statist('./sample.txt')
# you can put data directly such as below
# In : s = Statist('あのイーハトーヴォのすきとおった風、夏でも底に冷たさをもつ青いそら、うつくしい森で飾られたモリーオ市、 郊外のぎらぎらひかる草の波。')
# In : s = Statist([
#          'あのイーハトーヴォのすきとおった風、夏でも底に冷たさをもつ青いそら、うつくしい森で飾られたモリーオ市、 郊外のぎらぎらひかる草の波。',
#          'またそのなかでいっしょになったたくさんのひとたち、ファゼーロとロザーロ、羊飼のミーロや、顔の赤いこども たち、地主のテーモ、山猫博士のボーガント・デストゥパーゴなど、いまこの暗い巨きな石の建物のなかで考えて いると、みんなむかし風のなつかしい青い幻燈のように思われます。',
#          'では、わたくしはいつかの小さなみだしをつけながら、しずかにあの年のイーハトーヴォの五月から十月までを書 きつけましょう。'
#      ])

# show all stats
In : s.all_stats()
Out: {'word_stats': {'num_token': 137, 'num_vocab': 90},  # num_token == 延べ語数, num_vocab == 異なり語数
      'char_stats': {'num_token': 260, 'num_vocab': 109}}
 
# show word stats with verbose mode
In : s.calc_word_stats(verbose=True)
Counter({'の': 15, '、': 12, 'で': 5, 'に': 4, 'た': 3, 'を': 3, '。': 3, 'あの': 2, 'イーハトーヴォ': 2, '風': 2, '青い': 2, 'れ': 2, 'なか': 2, 'たち': 2, 'と': 2, 'は': 2, 'すきとおっ': 1, '夏': 1, 'も': 1, '底': 1, '冷た': 1, 'さ': 1, 'もつ': 1, 'そら': 1, 'うつくしい': 1, '森': 1, '飾ら': 1, 'モリーオ': 1, '市': 1, '郊外': 1, 'ぎらぎら': 1, 'ひかる': 1, '草': 1, '波': 1, 'また': 1, 'その': 1, 'いっしょ': 1, 'なっ': 1, 'たくさん': 1, 'ひと': 1, 'ファゼーロ': 1, 'ロザーロ': 1, '羊': 1, '飼': 1, 'ミーロ': 1, 'や': 1, '顔': 1, '赤い': 1, 'こども': 1, '地主': 1, 'テーモ': 1, '山猫': 1, '博士': 1, 'ボーガント・デスト ゥパーゴ': 1, 'など': 1, 'いま': 1, 'この': 1, '暗い': 1, '巨': 1, 'き': 1, 'な': 1, '石': 1, '建物': 1, '考え': 1, 'て': 1, 'いる': 1, 'みんな': 1, 'むかし': 1, 'なつかしい': 1, '幻': 1, '燈': 1, 'よう': 1, '思わ': 1, 'ます': 1, 'わたくし': 1, 'いつか': 1, '小さな': 1, 'み': 1, 'だし': 1, 'つけ': 1, 'ながら': 1, 'しずか': 1, '年': 1, '五月': 1, 'から': 1, '十月': 1, 'まで': 1, '書きつけ': 1, 'ましょ': 1, 'う': 1})
Out: {'num_token': 137, 'num_vocab': 90}
```

### Matplotlib Utils

```python
# just import this package and then you can plot with Japanese font
>>> import matplotlib.pyplot as plt
>>> import peinan_utils

# set background face color
>>> fig = plt.figure()
>>> fig.patch.set_facecolor('white')

# plot with Japanese labels
>>> plt.plot([1,2,3], [1,2,3])
>>> plt.xlabel('x軸')
>>> plt.ylabel('y軸')
>>> plt.show()
```

![](https://raw.githubusercontent.com/peinan/peinan-utils-py/master/images/plot_result.png)

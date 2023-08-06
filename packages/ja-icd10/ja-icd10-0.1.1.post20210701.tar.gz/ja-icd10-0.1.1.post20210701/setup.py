# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icd10']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'ja-icd10',
    'version': '0.1.1.post20210701',
    'description': 'ICD-10 国際疾病分類の日本語情報を扱うためのパッケージ',
    'long_description': '# ja-ICD10\nICD-10 国際疾病分類の日本語情報を扱うためのパッケージ\n\n## インストール\n\n\n## 使い方\nまず、ICDクラスのインスタンスを作成します。\n\n```python\nfrom icd10 import icd\n\nicd = icd.ICD()\n```\n\n### ICD-10のカテゴリー情報を取得する\nICD-10のカテゴリー名から情報を取得します。ICD-10のカテゴリー表記は、`A000`,`A00.0`どちらも可能です。\n\n```python\nIn []: print(icd["A000"])\n<ICD Category:[A00.0] コレラ菌によるコレラ>\n\nIn []: icd["A000"].name\nOut[]: \'コレラ菌によるコレラ\'\n\nIn []: icd["A000"].code\nOut[]: \'A00.0\'\n```\n\nまた、登録されているカテゴリーの中分類であれば、範囲指定も可能です。\n\n```python\nIn []: icd["A00-A09"]\nOut[]: <ICD Category:[A00-A09] 腸管感染症>\n\nIn []: icd["A00-A09"].is_block\nOut[]: True\n\nIn []: icd["A00-B99"]\nOut[]: <ICD Category:[A00-B99] 感染症及び寄生虫症>\n\nIn []: icd["A00-B99"].is_chapter\nOut[]: True\n```\n\n### 名称からICD-10カテゴリーを探す\n索引を元にカテゴリーを検索します。\n\n```python\nIn []: icd.find_categories_by_name("頭痛")\nOut[]: [<ICD Category:[R51] 頭痛>]\n\nIn []: icd.find_categories_by_name("吐き気")\nOut[]: [<ICD Category:[R11] 悪心及び嘔吐>]\n```\n\n`partial_match=True`を指定することで、すべてのカテゴリー名からの部分検索ができます。\n\n```python\nIn []: icd.find_categories_by_name("頭痛", partial_match=True)\nOut[]:\n[<ICD Category:[G43] 片頭痛>,\n <ICD Category:[G43.0] 前兆＜アウラ＞を伴わない片頭痛［普通型片頭痛］>,\n <ICD Category:[G43.1] 前兆＜アウラ＞を伴う片頭痛［古典型片頭痛］>,\n <ICD Category:[G43.2] 片頭痛発作重積状態>,\n <ICD Category:[G43.3] 合併症を伴う片頭痛>,\n <ICD Category:[G43.8] その他の片頭痛>,\n <ICD Category:[G43.9] 片頭痛，詳細不明>,\n <ICD Category:[G44] その他の頭痛症候群>,\n <ICD Category:[G44.0] 群発頭痛症候群>,\n <ICD Category:[G44.1] 血管性頭痛，他に分類されないもの>,\n <ICD Category:[G44.2] 緊張性頭痛>,\n <ICD Category:[G44.3] 慢性外傷後頭痛>,\n <ICD Category:[G44.4] 薬物誘発性頭痛，他に分類されないもの>,\n <ICD Category:[G44.8] その他の明示された頭痛症候群>,\n <ICD Category:[O29.4] 妊娠中の脊髄又は硬膜外麻酔誘発性頭痛>,\n <ICD Category:[O74.5] 分娩における脊髄麻酔及び硬膜外麻酔誘発性頭痛>,\n <ICD Category:[O89.4] 産じょく＜褥＞における脊髄麻酔及び硬膜外麻酔誘発性頭痛>,\n <ICD Category:[R51] 頭痛>]\n```\n\n### 傷病情報を取得する\n病名管理番号から傷病名を検索します。\n\n```python\nIn []: icd.get_disease_by_byomei_id("20088330").name\nOut[]: \'外傷性横隔膜ヘルニア・胸腔に達する開放創合併あり\'\n\nIn []: icd.get_disease_by_byomei_id("20088330").code\nOut[]: \'S2781\'\n\nIn []: icd.get_disease_by_byomei_id("20088330").name_kana\nOut[]: \'ガイショウセイオウカクマクヘルニア・キョウクウニタッスルカイホウソウガッペイアリ\'\n\nIn []: icd.get_disease_by_byomei_id("20088330").name_abbrev\nOut[]: \'外傷性横隔膜ヘルニア・胸腔開放創あり\'\n```\n\n\n### カテゴリーの下の階層の傷病を取得する\n指定したICD-10のカテゴリーの階層下にある傷病をすべて取得します。\n\n\n```python\nIn []: print(icd.get_diseases_by_code("A000"))\n[<Disease:[A00.0][20050788] アジアコレラ>,\n<Disease:[A00.0][20065915] 真性コレラ>]\n\nIn []: print(icd.get_diseases_by_code("A00"))\n[<Disease:[A00.0][20050788] アジアコレラ>,\n <Disease:[A00.0][20065915] 真性コレラ>,\n <Disease:[A00.1][20051356] エルトールコレラ>,\n <Disease:[A00.9][20051879] コレラ>,\n <Disease:[A00.9][20058027] 偽性コレラ>]\n```\n\n### カテゴリー以下の階層のカテゴリーと傷病を取得する\n指定したICD-10のカテゴリーの階層下にあるカテゴリーと傷病をすべて取得します。\n\n```python\nIn []: icd.get_diseases_and_categories_by_code("A000")\nOut[]:\n[<ICD Category:[A00.0] コレラ菌によるコレラ>,\n <Disease:[A00.0][20050788] アジアコレラ>,\n <Disease:[A00.0][20065915] 真性コレラ>]\n\nIn []: icd.get_diseases_and_categories_by_code("A00")\nOut[]:\n[<ICD Category:[A00] コレラ>,\n <ICD Category:[A00.0] コレラ菌によるコレラ>,\n <Disease:[A00.0][20050788] アジアコレラ>,\n <Disease:[A00.0][20065915] 真性コレラ>,\n <ICD Category:[A00.1] エルトールコレラ菌によるコレラ>,\n <Disease:[A00.1][20051356] エルトールコレラ>,\n <ICD Category:[A00.9] コレラ，詳細不明>,\n <Disease:[A00.9][20051879] コレラ>,\n <Disease:[A00.9][20058027] 偽性コレラ>] \n```\n\n## 情報元\n本レポジトリで利用しているデータは、下記ウェブサイトで公開されているものを利用しています。\n\n- [ICD10対応標準病名マスター\u3000トップページ](https://www2.medis.or.jp/stdcd/byomei/index.html)\n- [標準病名マスター作業班\u3000運用補助マスター](http://www.byomei.org/accessorytables/index.html)\n',
    'author': 'Yuki Okuda',
    'author_email': 'y.okuda@dr-ubie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

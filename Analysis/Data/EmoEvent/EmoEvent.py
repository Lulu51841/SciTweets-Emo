# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""EmoEvent dataset"""


import csv
import os

from datasets.tasks import TextClassification

import datasets

_DESCRIPTION = """\
EmoEvent is a multilingual emotion dataset of tweets based on different events that took place in April 2019. 
Three annotators labeled the tweets following the six Ekman’s basic emotion model (anger, fear, sadness, joy, disgust, surprise) plus the “neutral or other emotions” category.
"""

_CITATION = """\
@inproceedings{plaza-del-arco-etal-2020-emoevent, 
title = "{{E}mo{E}vent: A Multilingual Emotion Corpus based on different Events}", 
author = "{Plaza-del-Arco}, {Flor Miriam} and Strapparava, Carlo and {Ure{~n}a-L{\’o}pez}, L. Alfonso and {Mart{\’i}n-Valdivia}, M. Teresa", 
booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference", month = may, year = "2020", address = "Marseille, France", publisher = "European Language Resources Association", 
url = "https://www.aclweb.org/anthology/2020.lrec-1.186", 
pages = "1492--1498", 
language = "English", 
ISBN = "979-10-95546-34-4" }
"""

_CLASS_NAMES = ["anger", "fear", "sadness", "joy", "disgust", "surprise", "others"]

_HOMEPAGE = "https://github.com/fmplaza/EmoEvent/blob/master/"

_URLS = {
    "es": "https://raw.githubusercontent.com/fmplaza/EmoEvent/master/splits/es",
    "en": "https://raw.githubusercontent.com/fmplaza/EmoEvent/master/splits/en",
}


class EmoEvent(datasets.GeneratorBasedBuilder):
    """EmoEvent classification dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="es", version=VERSION, description="This part of my dataset covers the english version"
        ),
        datasets.BuilderConfig(
            name="en", version=VERSION, description="This part of my dataset covers the spanish version"
        ),
    ]

    DEFAULT_CONFIG_NAME = "es"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "event": datasets.Value("string"),
                    "tweet": datasets.Value("string"),
                    "offensive": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=["anger", "fear", "sadness", "joy", "disgust", "surprise", "others"]
                    ),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="tweet", label_column="label")],
        )

    def _split_generators(self, dl_manager):

        urls = _URLS[self.config.name]
        _TRAIN_DOWNLOAD_URL = os.path.join(urls, "train.tsv")
        _DEV_DOWNLOAD_URL = os.path.join(urls, "dev.tsv")
        _TEST_DOWNLOAD_URL = os.path.join(urls, "test.tsv")

        print(_TRAIN_DOWNLOAD_URL)

        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        dev_path = dl_manager.download_and_extract(_DEV_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": dev_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate AG News examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                id_tweet, event, tweet, offensive, label = row
                yield id_, {"id": id_tweet, "event": event, "tweet": tweet, "offensive": offensive, "label": label}

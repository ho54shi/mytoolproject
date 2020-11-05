#!/usr/bin/env python
# -*- coding:utf-8 -*-

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import os
import sys

from tokens import *
from vocabulary import Vocabulary
from util import fill
from util_feature import NgramFeatures
import ner


# predict tags
def test(
    model,
    word_vocab: Vocabulary,
    char_vocab: Vocabulary,
    tag_vocab: Vocabulary,
    sentences: list,
    feat_handler,
    to_stdout: bool = True,
):
    device = torch.device(model._device)

    ret = []
    for words in sentences:

        if len(words) <= 0:
            ret.append([])
            continue

        # create tensor for char embedding
        chars = torch.LongTensor(
            fill(
                [char_vocab.tokens2ids(list(w)) for w in words],
                [len(w) for w in words],
                char_vocab.t2i[EOS],
            )
        ).to(device)

        # create features if necessary
        if feat_handler:
            features = feat_handler.calcFeaturesBatch([words])
            features = features.to(device)
        else:
            features = None

        words = torch.LongTensor(
            word_vocab.tokens2ids(words)).view(1, -1).to(device)
        score, path = model.viterbi(
            words, chars, features, tag_vocab, None, None)

        path = [tag_vocab.i2t[i] for i in path]

        if to_stdout:
            print(" ".join(path))

        ret.append(path)

    return ret


if __name__ == "__main__":
    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model_path", type=str,
                        default=None, help="model path")
    parser.add_argument("-t", "--test_path", type=str,
                        default=None, help="test path")
    parser.add_argument("-v", "--vocab_path", type=str,
                        default=None,    help="vocabulary path")
    parser.add_argument("-g", "--gpu", type=int, default=-
                        1,    help="use GPU if gpu >= 0")

    parser.add_argument("--dict_path", type=str,
                        default=None, help="feature path")
    parser.add_argument("--feature_n", type=int, default=0,
                        help="maximum number of ngrams")

    parser.add_argument("--hidden_word_size", type=int,
                        default=256, help="hidden size")
    parser.add_argument("--hidden_char_size", type=int,
                        default=64, help="hidden size")

    parser.add_argument("--text_path", type=str,
                        default=None, help="text path")

    args = parser.parse_args()

    for loc in (args.test_path, args.vocab_path, args.model_path):
        if loc is None:
            raise Exception("{} is None".format(loc))

    word_vocab, char_vocab, tag_vocab = pickle.load(
        open(args.vocab_path, "rb"))

    model = ner.BiLSTMCRF(
        len(word_vocab.t2i.keys()),
        len(char_vocab.t2i.keys()),
        args.hidden_word_size,
        args.hidden_char_size,
        len(tag_vocab.t2i.keys()),
        args.feature_n,
    )

    model.load_state_dict(torch.load(
        args.model_path, map_location=lambda x, loc: x))
    model._device = "cuda:{}".format(args.gpu) if args.gpu >= 0 else "cpu"
    model = model.to(model._device)
    model.eval()

    if args.dict_path and args.feature_n > 0:
        feat_handler = NgramFeatures(
            args.dict_path,
            args.feature_n,
        )
    else:
        feat_handler = None

    with torch.no_grad():

        words_list = []
        ref_list = []

        for line in open(args.test_path).readlines():

            line = [c.split("/") for c in line.rstrip().split(" ")]

            words_list += [[c[0] for c in line]]
            ref_list += [[c[1] for c in line]]

# ----------------------------------------
        my_words_list = []

        for line in open(args.text_path).readlines():

            line = [c for c in line.rstrip().split("　")]  # 半角空白から全角空白に変更
            my_words_list += [[c for c in line]]

# ----------------------------------------
        hyp_list = test(
            model,
            word_vocab,
            char_vocab,
            tag_vocab,
            # words_list,
            my_words_list,
            feat_handler,
            to_stdout=False,
        )

        for words, hyp in zip(my_words_list, hyp_list):

            print(" ".join(
                [
                    "/".join([w, t])
                    for w, t in zip(words, hyp)
                ]
            ))

#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

def to_unicode(text):
    if isinstance(text, str):
        return text.decode('utf-8')
    return text

def to_utf8(text):
    if isinstance(text, unicode):
        return text.encode('utf-8')
    return text

class BITokenizer(object):
    def __init__(self):
        pass

    @classmethod
    def tokenize(self, text):
        tu8 = to_unicode(text)
        rarray = []
        for idx, sy in enumerate(tu8):
            if sy == " ":
                continue
            tag = "B"
            if (idx>0 and tu8[idx-1] != " "):
                tag = "I"
            rarray.append("%s/%s" % (tag, sy))
        return to_utf8(" ".join(rarray))

    @classmethod
    def detokenize(self, text):
        array = text.split(" ")
        rarray = []
        for idx, sy in enumerate(array):
            tag = sy[0:1]
            ch = sy[2:]
            if idx != 0 and tag == "B":
                rarray.append(" ")
            rarray.append(ch)
        return "".join(rarray)

if __name__ == "__main__":
    text = "오늘 날씨가 정말 좋네요"
    tokenizer = BITokenizer()
    tokens = tokenizer.tokenize(text)
    detokens = tokenizer.detokenize(tokens)

    print text
    print tokens
    print detokens

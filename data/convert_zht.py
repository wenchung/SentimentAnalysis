#! /bin/env python3
# -*- coding: utf-8 -*-

from langconv import Converter

def to_zht(fn):
    fn2="n_%s"%fn
    print "%s -> %s"%(fn,fn2)
    with open(fn2, "w") as n:
        with open(fn, "r") as p:
            for line in p.readlines():
                sentence = line
                line = Converter('zh-hant').convert(sentence.decode('utf-8'))
                line = line.encode('utf-8')
                n.write(line)

to_zht("pos.csv")
to_zht("neg.csv")
to_zht("neutral.csv")

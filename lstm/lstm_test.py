#! /bin/env python
# -*- coding: utf-8 -*-
"""
預測
"""
#ImportError: DLL load failed: 找不到指定的模組。
import pandas as pd 
import numpy as np 
import jieba
import multiprocessing

from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
from langconv import Converter

import yaml
from keras.models import model_from_yaml
np.random.seed(1337)  # For Reproducibility
import sys
sys.setrecursionlimit(1000000)

# define parameters
maxlen = 100

def create_dictionaries(model=None,
                        combined=None):
    ''' Function does are number of Jobs:
        1- Creates a word to index mapping
        2- Creates a word to vector mapping
        3- Transforms the Training and Testing Dictionaries

    '''
    if (combined is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(list(model.wv.vocab.keys()),
                            allow_update=True)
        #  freqxiao10->0 所以k+1
        w2indx = {v: k+1 for k, v in list(gensim_dict.items())}#所有頻數超過10的詞語的索引,(k->v)=>(v->k)
        #DeprecationWarning: Call to deprecated `__getitem__` (Method will be removed in 4.0.0, use self.wv.__getitem__() instead).
        w2vec = {word: model.wv[word] for word in list(w2indx.keys())}#所有頻數超過10的詞語的詞向量, (word->model(word))

        def parse_dataset(combined): # 閉包-->臨時使用
            ''' Words become integers
            '''
            data=[]
            for sentence in combined:
                new_txt = []
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0) # freqxiao10->0
                data.append(new_txt)
            return data # word=>index
        combined=parse_dataset(combined)
        combined= sequence.pad_sequences(combined, maxlen=maxlen)#每個句子所含詞語對應的索引，所以句子中含有頻數小於10的詞語，索引爲0
        return w2indx, w2vec,combined
    else:
        print('No data provided...')


def input_transform(string):
    words=jieba.lcut(string)
    words=np.array(words).reshape(1,-1)
    #model=Word2Vec.load('../model/Word2vec_model.pkl')
    model=Word2Vec.load('../lstm_data_test/Word2vec_model.pkl')
    _,_,combined=create_dictionaries(model,words)
    return combined


def lstm_predict(strings):
    print('loading model......')
    yaml.warnings({'YAMLLoadWarning': False})
    with open('../model/lstm.yml', 'r') as f:
        #YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
        yaml_string = yaml.load(f, Loader=yaml.FullLoader)
    model = model_from_yaml(yaml_string)

    print('loading weights......')
    model.load_weights('../model/lstm.h5')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    for string in strings:
        line = Converter('zh-hant').convert(string.encode().decode('utf-8'))
        string0 = line.encode('utf-8')
        print("="*20)
        data=input_transform(string0)
        data.reshape(1,-1)
        #print data
        result=model.predict_classes(data)
        print(result) # [[1]]
        if result[0]==1:
            print(string,' positive')
        elif result[0]==0:
            print(string,' neural')
        else:
            print(string,' negative')

if __name__=='__main__':
    strings=[
        "不錯不錯",
        "真的一般，沒什麼可以學習的",
        '酒店的環境非常好，價格也便宜，值得推薦',
        '手機質量太差了，傻逼店家，賺黑心錢，以後再也不會買了',
        "這是我看過文字寫得很糟糕的書，因爲買了，還是耐着性子看完了，但是總體來說不好，文字、內容、結構都不好",
        "雖說是職場指導書，但是寫的有點乾澀，我讀一半就看不下去了！",
        "書的質量還好，但是內容實在沒意思。本以爲會側重心理方面的分析，但實際上是婚外戀內容。",
        "不是太好",
    ]
    
    lstm_predict(strings)

#! /bin/env python
# -*- coding: utf-8 -*-
"""
預測
"""
import jieba
import numpy as np
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence

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
        w2vec = {word: model[word] for word in list(w2indx.keys())}#所有頻數超過10的詞語的詞向量, (word->model(word))

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
    model=Word2Vec.load('../model/Word2vec_model.pkl')
    _,_,combined=create_dictionaries(model,words)
    return combined


def lstm_predict(string):
    print('loading model......')
    with open('../model/lstm.yml', 'r') as f:
        yaml_string = yaml.load(f)
    model = model_from_yaml(yaml_string)

    print('loading weights......')
    model.load_weights('../model/lstm.h5')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    data=input_transform(string)
    data.reshape(1,-1)
    #print data
    result=model.predict_classes(data)
    # print result # [[1]]
    if result[0]==1:
        print(string,' positive')
    elif result[0]==0:
        print(string,' neural')
    else:
        print(string,' negative')


if __name__=='__main__':
    # string='酒店的環境非常好，價格也便宜，值得推薦'
    # string='手機質量太差了，傻逼店家，賺黑心錢，以後再也不會買了'
    # string = "這是我看過文字寫得很糟糕的書，因爲買了，還是耐着性子看完了，但是總體來說不好，文字、內容、結構都不好"
    # string = "雖說是職場指導書，但是寫的有點乾澀，我讀一半就看不下去了！"
    # string = "書的質量還好，但是內容實在沒意思。本以爲會側重心理方面的分析，但實際上是婚外戀內容。"
    # string = "不是太好"
    # string = "不錯不錯"
    string = "真的一般，沒什麼可以學習的"
    
    lstm_predict(string)
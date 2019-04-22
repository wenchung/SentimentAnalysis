+++ issue
----
  File "/usr/local/lib/python3.6/dist-packages/gensim/utils.py", line 912, in unpickle
    return _pickle.loads(f.read())
UnicodeDecodeError: 'ascii' codec can't decode byte 0xd1 in position 0: ordinal not in range(128)
----
sudo pip3 install -U gensim

+++ issue
----
AttributeError: 'Word2Vec' object has no attribute 'vocab'
----
https://stackoverflow.com/questions/42517435/gensim-word2vec-in-python3-missing-vocab
Are you using the same version of gensim in both places? Gensim 1.0.0 moves vocab to a helper object, so whereas in pre-1.0.0 versions of gensim (in Python 2 or 3), you can use:
model.vocab
...in gensim 1.0.0+ you should instead use (in Python 2 or 3)...
model.wv.vocab


+++ Python 中簡轉繁、繁轉簡
http://xken831.pixnet.net/blog/post/463639202-%5Bpython%5D-python-%E7%B0%A1%E8%BD%89%E7%B9%81%E3%80%81%E7%B9%81%E8%BD%89%E7%B0%A1
cd data/
git clone https://github.com/skydark/nstools
cp nstools/zhtools/zh_wiki.py .
cp nstools/zhtools/langconv.py .
python2 convert_zht.py

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

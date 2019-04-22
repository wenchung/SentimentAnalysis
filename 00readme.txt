+++ issue: python3 lstm_train.py
----
  File "/usr/local/lib/python3.6/dist-packages/gensim/utils.py", line 912, in unpickle
    return _pickle.loads(f.read())
UnicodeDecodeError: 'ascii' codec can't decode byte 0xd1 in position 0: ordinal not in range(128)
----
sudo pip3 install -U gensim

+++ issue: python3 lstm_test.py
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


+++ issue: python3 lstm_train.py
----
  File "lstm_train.py", line 109, in word2vec_train
    model.train(combined)
  File "/usr/local/lib/python3.6/dist-packages/gensim/models/word2vec.py", line 910, in train
    queue_factor=queue_factor, report_delay=report_delay, compute_loss=compute_loss, callbacks=callbacks)
  File "/usr/local/lib/python3.6/dist-packages/gensim/models/base_any2vec.py", line 1081, in train
    **kwargs)
  File "/usr/local/lib/python3.6/dist-packages/gensim/models/base_any2vec.py", line 536, in train
    total_words=total_words, **kwargs)
  File "/usr/local/lib/python3.6/dist-packages/gensim/models/base_any2vec.py", line 1200, in _check_training_sanity
    "You must specify either total_examples or total_words, for proper job parameters updation"
ValueError: You must specify either total_examples or total_words, for proper job parameters updationand progress calculations. The usual value is total_examples=model.corpus_count.
----
-    model.train(combined)
+    model.train(combined, total_examples=model.corpus_count, epochs=model.iter)


+++ OpenCC 簡轉繁
# https://blog.darkthread.net/blog/opencc-notes-1/
opencc -i lstm_test.py -o xx.py -c s2t.json
mv xx.py lstm_test.py

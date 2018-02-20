'''
Created on Dec 2, 2017

@author: ruiwang
Note: This code is a modified version based on the original implementation on https://github.com/tensorflow/nmt
'''


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os
import re
import tensorflow as tf
import argparse
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from tensorflow.python.platform import gfile

# Special vocabulary symbols - we always put them at the start.
UNK = "<unk>"
SOS = "<s>"
EOS = "</s>"
UNK_ID = 0

_START_VOCAB = [UNK, SOS, EOS]




# Regular expressions used to tokenize.
_WORD_SPLIT = re.compile(b"([.,!?\"':;)(])")
_DIGIT_RE = re.compile(br"\d")






def basic_tokenizer(sentence):
  """Very basic tokenizer: split the sentence into a list of tokens."""
  words = []
  for space_separated_fragment in sentence.strip().split():
    words.extend(_WORD_SPLIT.split(space_separated_fragment))
  return [w for w in words if w]


def create_vocabulary(vocabulary_path, data_path, max_vocabulary_size,
                      tokenizer=None, normalize_digits=True):
  """Create vocabulary file (if it does not exist yet) from data file.
  Data file is assumed to contain one sentence per line. Each sentence is
  tokenized and digits are normalized (if normalize_digits is set).
  Vocabulary contains the most-frequent tokens up to max_vocabulary_size.
  We write it to vocabulary_path in a one-token-per-line format, so that later
  token in the first line gets id=0, second line gets id=1, and so on.
  Args:
    vocabulary_path: path where the vocabulary will be created.
    data_path: data file that will be used to create vocabulary.
    max_vocabulary_size: limit on the size of the created vocabulary.
    tokenizer: a function to use to tokenize each data sentence;
      if None, basic_tokenizer will be used.
    normalize_digits: Boolean; if true, all digits are replaced by 0s.
  """

  if True:

    print("Creating vocabulary %s from data %s" % (vocabulary_path, data_path))
    vocab = {}
    with gfile.GFile(data_path, mode="rb") as f:
      print("reading input file")
      counter = 0
      for line in f:
        counter += 1
        if counter % 100000 == 0:
          print("  processing line %d" % counter)
        tokens = tokenizer(line) if tokenizer else basic_tokenizer(line)
        for w in tokens:
          word = _DIGIT_RE.sub(b"0", w) if normalize_digits else w
          if word in vocab:
            vocab[word] += 1
          else:
            vocab[word] = 1
      vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
      if len(vocab_list) > max_vocabulary_size:
        vocab_list = vocab_list[:max_vocabulary_size]
      with gfile.GFile(vocabulary_path, mode="wb") as vocab_file:
        for w in vocab_list:
          vocab_file.write(w + b"\n")


def initialize_vocabulary(vocabulary_path):
  """Initialize vocabulary from file.
  We assume the vocabulary is stored one-item-per-line, so a file:
    dog
    cat
  will result in a vocabulary {"dog": 0, "cat": 1}, and this function will
  also return the reversed-vocabulary ["dog", "cat"].
  Args:
    vocabulary_path: path to the file containing the vocabulary.
  Returns:
    a pair: the vocabulary (a dictionary mapping string to integers), and
    the reversed vocabulary (a list, which reverses the vocabulary mapping).
  Raises:
    ValueError: if the provided vocabulary_path does not exist.
  """
  if gfile.Exists(vocabulary_path):
    rev_vocab = []
    with gfile.GFile(vocabulary_path, mode="rb") as f:
      rev_vocab.extend(f.readlines())
    rev_vocab = [line.strip() for line in rev_vocab]
    vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
    return vocab, rev_vocab
  else:
    raise ValueError("Vocabulary file %s not found.", vocabulary_path)


def sentence_to_token_ids(sentence, vocabulary,
                          tokenizer=None, normalize_digits=True):
  """Convert a string to list of integers representing token-ids.
  For example, a sentence "I have a dog" may become tokenized into
  ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
  "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].
  Args:
    sentence: the sentence in bytes format to convert to token-ids.
    vocabulary: a dictionary mapping tokens to integers.
    tokenizer: a function to use to tokenize each sentence;
      if None, basic_tokenizer will be used.
    normalize_digits: Boolean; if true, all digits are replaced by 0s.
  Returns:
    a list of integers, the token-ids for the sentence.
  """

  if tokenizer:
    words = tokenizer(sentence)
  else:
    words = basic_tokenizer(sentence)
  if not normalize_digits:
    return [vocabulary.get(w, UNK_ID) for w in words]
  # Normalize digits by 0 before looking words up in the vocabulary.
  return [vocabulary.get(_DIGIT_RE.sub(b"0", w), UNK_ID) for w in words]


def data_to_token_ids(data_path, target_path, vocabulary_path,
                      tokenizer=None, normalize_digits=True):
  """Tokenize data file and turn into token-ids using given vocabulary file.
  This function loads data line-by-line from data_path, calls the above
  sentence_to_token_ids, and saves the result to target_path. See comment
  for sentence_to_token_ids on the details of token-ids format.
  Args:
    data_path: path to the data file in one-sentence-per-line format.
    target_path: path where the file with token-ids will be created.
    vocabulary_path: path to the vocabulary file.
    tokenizer: a function to use to tokenize each sentence;
      if None, basic_tokenizer will be used.
    normalize_digits: Boolean; if true, all digits are replaced by 0s.
  """
  if not gfile.Exists(target_path):
    print("Tokenizing data in %s" % data_path)
    vocab, _ = initialize_vocabulary(vocabulary_path)
    with gfile.GFile(data_path, mode="rb") as data_file:
      with gfile.GFile(target_path, mode="w") as tokens_file:
        counter = 0
        for line in data_file:
          counter += 1
          if counter % 100000 == 0:
            print("  tokenizing line %d" % counter)
          token_ids = sentence_to_token_ids(line, vocab, tokenizer,
                                            normalize_digits)
          tokens_file.write(" ".join([str(tok) for tok in token_ids]) + "\n")


def prepare_wmt_data(en_vocab_path, fr_vocab_path, 
                     train_source, train_traget,
                     en_vocabulary_size, fr_vocabulary_size, tokenizer=None):
  """Get WMT data into data_dir, create vocabularies and tokenize data.
  Args:
    data_dir: directory in which the data sets will be stored.
    en_vocabulary_size: size of the English vocabulary to create and use.
    fr_vocabulary_size: size of the French vocabulary to create and use.
    tokenizer: a function to use to tokenize each data sentence;
      if None, basic_tokenizer will be used.
  Returns:
    A tuple of 6 elements:
      (1) path to the token-ids for English training data-set,
      (2) path to the token-ids for French training data-set,
      (3) path to the token-ids for English development data-set,
      (4) path to the token-ids for French development data-set,
      (5) path to the English vocabulary file,
      (6) path to the French vocabulary file.
  """
  # Get wmt data to the specified directory.
  #train_path = get_wmt_enfr_train_set(data_dir)
  #dev_path = get_wmt_enfr_dev_set(data_dir)

  # Create vocabularies of the appropriate sizes.
  #fr_vocab_path = os.path.join(data_dir, "vocab%d.fr" % fr_vocabulary_size)
  #en_vocab_path = os.path.join(data_dir, "vocab%d.en" % en_vocabulary_size)
  create_vocabulary(fr_vocab_path, train_traget, fr_vocabulary_size, tokenizer)
  create_vocabulary(en_vocab_path, train_source, en_vocabulary_size, tokenizer)

  # Create token ids for the training data.
  #fr_train_ids_path = train_path + (".ids%d.fr" % fr_vocabulary_size)
  #en_train_ids_path = train_path + (".ids%d.en" % en_vocabulary_size)
  #data_to_token_ids(train_path + ".fr", fr_train_ids_path, fr_vocab_path, tokenizer)
  #data_to_token_ids(train_path + ".en", en_train_ids_path, en_vocab_path, tokenizer)

  # Create token ids for the development data.
  #fr_dev_ids_path = dev_path + (".ids%d.fr" % fr_vocabulary_size)
  #en_dev_ids_path = dev_path + (".ids%d.en" % en_vocabulary_size)
  #data_to_token_ids(dev_path + ".fr", fr_dev_ids_path, fr_vocab_path, tokenizer)
  #data_to_token_ids(dev_path + ".en", en_dev_ids_path, en_vocab_path, tokenizer)

  return (en_vocab_path, fr_vocab_path)





def arguments():
    parser = argparse.ArgumentParser(description="Segments the text input into separate sentences")

    parser.add_argument('--train_source', required=True, action="store", type=str, help="input training file in the source language")
    parser.add_argument('--train_target', required=True, action="store", type=str, help="input text file in the target language")
    
    parser.add_argument('--max_vocab_source', required=True, action="store", type=int, help="max vocab in the source language")
    parser.add_argument('--max_vocab_target', required=True, action="store", type=int, help="max vocab in the target language")

    parser.add_argument('--out_vocab_source', required=True, action="store", type=str, help="output vocab file in the source language")
    parser.add_argument('--out_vocab_target', required=True, action="store", type=str, help="output vocab file in the target language")

    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = arguments()
    #stem_file(args.input, args.stopword, args.number, args.top, args.output)
    #FreqCounter.py --train_source $input1 --train_target $input2 --max_vocab_source $input3 --max_vocab_target $input4 --out_vocab_source $tab_file1 --out_vocab_target $tab_file2
    train_source = args.train_source
    train_traget = args.train_target
    
    en_vocabulary_size = args.max_vocab_source
    fr_vocabulary_size = args.max_vocab_target
    
    en_vocab_path = args.out_vocab_source
    fr_vocab_path = args.out_vocab_target
    
    print(train_source)
    print(train_traget)
    print(en_vocabulary_size)
    print(fr_vocabulary_size)
    print(en_vocab_path)
    print(fr_vocab_path)

    
    prepare_wmt_data(en_vocab_path, fr_vocab_path, 
                     train_source, train_traget,
                     en_vocabulary_size, fr_vocabulary_size)
    
    #os.remove(fr_vocab_path)
    
    #from shutil import copyfile
    #copyfile(en_vocab_path, fr_vocab_path)
    

    #file_path = "/my/directory/filename.txt"
    #directory = "/home/ruiwang/galaxy/database/files/000/mydir"
    
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    #    print(directory)

    
    

































  
'''
Created on 13Dec.,2016

@author: ruiwang
'''
import sys
import os
import nltk
from nltk.stem import *
import argparse
import matplotlib;
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import time


#test the freqcounter
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def arguments():
    parser = argparse.ArgumentParser(description="Segments the text input into separate sentences")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--stopword', required=True, action="store", type=bool, help="input text file")
    parser.add_argument('--number', required=True, action="store", type=bool, help="input text file")
    parser.add_argument('--top', required=True, action="store", type=int, help="input text file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    args = parser.parse_args()
    return args


def stem_file(in_file, exclude_stopw, exclude_num, top_words, out_file):

    stopwords = nltk.corpus.stopwords.words('english')
    print(in_file)
    files = in_file.split(",")

    texts = ""
    for f in files:
        t = open(f, 'r') 
        texts += t.read() + " "
   

      
    words = nltk.word_tokenize(texts)

    
    if exclude_stopw:
        words = [w for w in words if w not in stopwords]
    
    if exclude_num:
        words = [w for w in words if not w.isdigit()]


    fdist = nltk.FreqDist(words)
    
    counts = []
    for w, f in fdist.most_common(top_words):
        counts.append((w,f))
        
    freq_words = [x[0] for x in counts]
    values = [int(x[1]) for x in counts]
    plt.figure(figsize=(15,10))
    matplotlib.rcParams.update({'font.size': 8})
    bar_width = 0.4
    mybar = plt.bar(range(len(freq_words)), values, color='blue', alpha=bar_width)

    plt.xlabel('Word Index')
    plt.ylabel('Frequency')
    plt.title('Word Frequency Histogram')
    plt.xticks(np.arange(len(freq_words)), freq_words)

    png_out = out_file + '.png' 
    plt.savefig(png_out)
    data = file(png_out, 'rb').read() 
    fp = open(out_file, 'wb')
    fp.write(data)
    fp.close()
    os.remove(png_out)
    '''
    #with tf.device("/cpu:0"):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    c = tf.matmul(a, b)
    # Creates a session with log_device_placement set to True.
    sess = tf.Session()
    # Runs the op.
    print(sess.run(c))
    '''
if __name__ == '__main__':
    args = arguments()
    stem_file(args.input, args.stopword, args.number, args.top, args.output)
    
    
    
    
    
    
    
    
    
    
    
    
    
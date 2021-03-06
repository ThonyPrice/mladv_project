#!/usr/bin/env python
# encoding: utf-8


import itertools
import numpy as np
import os

from collections import Counter
from math import floor
from math import log
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

'''
    This class provides conversion of text documents into a gram matrix
    to be used in an SVM for text classification purposes.

    To receive gram matrix, initialize class and call gram_matrix with
    a list of strings which are to be classified:

    >>> WK_kernel = WK()
    >>> WK_kernel.gram_matrix([text1, text2,...])

    To receive a vectorized input from string, one must first have made a
    gram matrix as above, then:

    >>> WK_kernel.vectorize(text)
'''

class WK(object):

    def __init__(self, docs):
        self.docs = docs
        self.n = len(docs)
        all_text = Counter(word_tokenize(" ".join(docs)))
        all_words = self.filterFewOccurences(all_text, 3)
        self.df = self.document_frequency(all_words, docs)
        self.unique_words = self.df

    def gram_matrix(self, docs):
        self.docs, docs = docs, docs
        self.n, n = len(docs), len(docs)
        # Join all text to find unique words and word frequency
        all_words = Counter(word_tokenize(" ".join(docs)))
        all_words = self.filterFewOccurences(all_words, 3)
        self.df = self.document_frequency(all_words, docs)
        self.unique_words = [word for word in self.df.keys()]
        # Calculate feature vector and use these to calc gram matrix
        # feature_vectors = self.featureVectors(docs, self.unique_words, self.df, n)
        # m = np.zeros((n, n))
        # for idx, (doc1, doc2) in enumerate(itertools.product(feature_vectors, feature_vectors)):
        #     m[floor(idx/n)][idx%n] = np.dot(doc1, doc2) / \
        #         ( np.dot(doc1, doc1) * np.dot(doc2, doc2) )**0.5
        # return m

    def kernel(self, doc1, doc2):
        v = self.vectorize(doc1)
        w = self.vectorize(doc2)
        normalize = ( np.dot(v, v) * np.dot(w, w) )**0.5
        if normalize != 0:
            return np.dot(v, w) / ( np.dot(v, v) * np.dot(w, w) )**0.5
        return np.dot(v, w)

    def vectorize(self, text):
        v = self.featureVectors([text], self.unique_words, self.df, self.n)[0]
        return v

    def filterFewOccurences(self, words, limit):
        for key, count in itertools.dropwhile(lambda key_count:
                key_count[1] > limit, words.most_common()):
            del words[key]
        return words

    def document_frequency(self, words, docs):
        for word in words.keys():
            words[word] = sum([1 for doc in docs if word in doc])
        return words

    def featureVectors(self, docs, unique_words, df, n):
        vectors = []
        # print("DF: ", self.df)
        # print("********************************")
        # print("UW: ", self.unique_words)
        for doc in docs:
            doc_count = Counter(word_tokenize(doc))
            v = [
                log( 1 + doc_count[word] ) *
                log( n / self.df[word] )
                for word in unique_words.keys()
                if self.df[word] > 0
            ]
            vectors.append(np.asarray(v))
        return vectors


# ___ This code if for testing purposes! ___

# Comment out main() when done with testing.
def main():
    docs = [
        "So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.",
        "The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.",
        "There were doors all round the hall, but they were all locked; and when Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again."
    ]
    text = "There were doors all round the hall, but they were all locked; and when Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again."
    WK_kernel = WK(docs)
    print("DF: ", WK_kernel.df)
    print("UW: ", WK_kernel.unique_words)
#     print('Gram matrix:\n', WK_kernel.gram_matrix(indata))
#     print('Feature vector:\n', WK_kernel.vectorize(text))
    print('~*~ End Of Word Kernel ~*~')
#
if __name__ == '__main__':
    main()

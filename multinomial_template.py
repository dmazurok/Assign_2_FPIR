#! /usr/bin/python
# -*- coding: utf-8 -*-


"""MLE for the multinomial distribution."""
import operator
from argparse import ArgumentParser
from scipy.stats import multinomial

from numpy import mean, var, sqrt


def get_top_k_words(words, stopwords, k):
    """Return the k most frequent words as a list."""
    # create dict of unique words to count them down
    un_words = {}
    for x in words:
        if x not in stopwords:
            if not un_words.__contains__(x):
                un_words[x] = 1
            else:
                un_words[x] += 1
    un_words = sorted(un_words.items(), key=operator.itemgetter(1), reverse=True)
    #top_k_words = []
    #for x in un_words[0:k]:     # convert list into an array of words only
    #    top_k_words.append(x[1])
    return un_words[0:k]

def get_words(file_path):
    """Return a list of words from a file, converted to lower case."""
    with open(file_path, encoding='utf-8') as hfile:
        return hfile.read().lower().split()

def my_var (wordlist, m, k):
    res = 0
    for x in wordlist:
        res = res + pow((x-m),2)
    res = res/k
    return  res

def likel(x, m, vari):
    return (1/(sqrt(2*3.14 * vari*vari)) * pow(2.71, (-(pow((x-m), 2))/(2*pow(vari, 2)))))

def get_probabilities(words, stopwords, k):

    top_k_words = (get_top_k_words(words, stopwords, k))
    res = {}
    summa = 0
    for x in top_k_words:
        summa = summa + x[1]

    for x in top_k_words:
        res[x[0]] = x[1]/summa
    # print(top_k_words)
    # print(mean(top_k_words))
    # print(var(top_k_words, ddof=0))
    # print(my_var(top_k_words,mean(top_k_words), k))
    #
    #
    # print(likel(top_k_words[0], mean(top_k_words), var(top_k_words, ddof=0)))


    #for x in top_k_words:


    """
    Create a multinomial probability distribution from a list of words:
        1. Find the top-k most frequent words.
        2. For every one of the most frequent words, calculate its probability according to MLE.

    Return a dictionary of size k that maps the words to their probabilities.
    """
    # TODO
    return res


def multinomial_pmf(sample, probabilities):
    #from scipy.stats import multinomial

    #rv = multinomial(1,probabilities)
    print ("")
    """
    The multinomial probability mass function.
    Inputs:
        * sample: dictionary, maps words (X_i) to observed frequencies (x_i)
        * probabilities: dictionary, maps words to their probabilities (p_i)

    Return the probability of observing the sample, i.e. P(X_1=x_1, ..., X_k=x_k).
    """
    # TODO
    return 0


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('INPUT_FILE', help='A file containing whitespace-delimited words')
    arg_parser.add_argument('SW_FILE', help='A file containing whitespace-delimited stopwords')
    arg_parser.add_argument('-k', type=int, default=10,
                            help='How many of the most frequent words to consider')
    args = arg_parser.parse_args()
    words = get_words(args.INPUT_FILE)
    stopwords = set(get_words(args.SW_FILE))

    probabilities = get_probabilities(words, stopwords, args.k)


    # we should have k probabilities
    assert len(probabilities) == args.k

    # check if all p_i sum to 1 (accounting for some rounding error)
    assert 1 - 1e-12 <= sum(probabilities.values()) <= 1 + 1e-12


    # check if p_i >= 0
    assert not any(p < 0 for p in probabilities.values())

    # print estimated probabilities
    print('estimated probabilities:')
    i = 1
    for word, prob in probabilities.items():
        print('p_{}\t{}\t{:.5f}'.format(i, word, prob))
        i += 1

    # read inputs for x_i
    print('\nenter sample:')
    sample = {}
    i = 1
    for word in probabilities:
        sample[word] = int(input('X_{}='.format(i)))
        i += 1

    # print P(X_1=x_1, ..., X_k=x_k)
    print('\nresult: {}'.format(multinomial_pmf(sample, probabilities)))


if __name__ == '__main__':
    main()

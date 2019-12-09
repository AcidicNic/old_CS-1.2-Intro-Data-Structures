import re
from random import randrange, randint, shuffle, sample
from sys import argv
from operator import itemgetter
from sys import exit
from re import sub, split


def frequency(histogram, word):
    ''' finds the count for one word '''
    if not isinstance(histogram, dict):
        histogram = dict(histogram)
    try:
        return histogram[word]
    except:
        # Word not found
        return 0

def bulk_frequency(histogram, num):
    ''' finds all words that have the specified count '''
    print(f"All words with the count {num}:")
    count = 0
    words = []
    for word, freq in dict(histogram).items():
        if freq == num:
            count += 1
            print(f"{count}.| {word}")
            words.append(word)
    if count == 0:
        print(f"No words found.")
        return None
    return words

def unique_words(histogram):
    ''' this function is totally useless, since len() is shorter,
        but i guess this is more clear about what it's doing '''
    return len(histogram)

def get_total_tokens(histogram):
    if isinstance(histogram, dict):
        return sum(histogram.values())
    else:
        tokens = 0
        for i in range(len(histogram)):
            tokens += histogram[i][1]
        return tokens

def top_count(histogram, top_num=0):
    ''' convert dict to list of tuples (still ordered by highest to lowest frequency)
            prints the top {top_num} words and their frequencies. '''
    '''
    USE THIS TO OPTIMIZE:
    >>> d = {'a': 1, 'b': 2}
    >>> dki = d.iterkeys()
    >>> dki.next()
    'a'
    >>> dki.next()
    'b'
    >>> dki.next()
    Traceback (most recent call last):
      File "<interactive input>", line 1, in <module>
    StopIteration
    '''

    try:
        temp_histogram = list(histogram.items())
        print(f"Top {top_num} words:")
        if 0 < top_num < len(temp_histogram):
            for i in range(top_num):
                print(f"{i+1}.| {temp_histogram[i][0]}: {frequency(histogram, temp_histogram[i][0])}")
        else:
            for i in range(len(temp_histogram)):
                print(f"{i + 1}.| {temp_histogram[i][0]}: {frequency(histogram, temp_histogram[i][0])}")
    except Exception as e:
        print(e)
        print("*** Invalid histogram ***")
        exit()

# if __name__ == '__main__':
    # test = Histogram('source_text', 'f')
    #
    # sentences = bulk_sentences(test.markov_chain, 10)
    # for sentence in sentences:
    #     print(sentence)
    #     print()

#     ''' py frequency.py                   | to use default filename (test.txt)
#         py frequency.py <filename>        | to specify your source text file
#         py frequency.py <raw source text> | to pass in your own source text
#     '''
#
#     if len(argv) == 2:
#         # if filename is passed in
#         main_histogram = Histogram(argv[1], 'f')
#     elif len(argv) > 2:
#         # if words are passed in
#         main_histogram = Histogram(" ".join(argv[1:]))
#     else:
#         fish_text = 'one fish two fish red fish blue fish'
#         fishogram = Histogram(fish_text)
#         print()
#         woodchuck_text = ('how much wood would a wood chuck chuck'
#                           ' if a wood chuck could chuck wood')
#         woodogram = Histogram(woodchuck_text)
    #
    # _word_list = []
    # for i in range(10000):
    #     _word_list.append(sample_by_frequency(main_histogram))
    # next_histogram = get_histogram(_word_list)
    # top_count(next_histogram)
    #
    # top_count(main_histogram, 10)


    # print(f"Total words: {unique_words(main_histogram)}")
    #
    # # print(f'"the" is found {str(frequency(histogram, 'the'))} times')
    # # print(f'"fakkkeworddd" is found {str(frequency(histogram, 'fakkkeworddd'))} times')
    # print(main_histogram)
    # top_count(main_histogram, 20)
    # # bulk_frequency(histogram, 7)
    # print(f'Sample by Frequency: {sample_by_frequency(main_histogram)}')

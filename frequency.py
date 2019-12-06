import re
from random import randrange, shuffle, sample
from sys import argv
from operator import itemgetter
from sys import exit
from re import sub, split


class Histogram():
    def __init__(self, source_text, flag=''):
        self.word_list = None

        # set the flag to 'F' to load text from a file
        if flag.lower() == 'f':
            source_text = histogram_file(source_text)

        # To load from a word_list or string, don't pass in a flag.
        self.word_list = get_word_list(source_text)

        self.histogram = get_histogram(self.word_list)

        self.total_tokens = get_total_tokens(self.histogram)
        self.total_types = unique_words(self.histogram)

        self.markov_chain = markov(self.word_list)

def get_word_list(source_text):
    ''' Splits text_str into a list of lowercase words
        Creates an empty dictionary.
        For every word in the list that was passed in:
            If it's already in the dictionary, increase it's value by one.
            Otherwise, add it to the dictionary and set it's value to one.
        Sorts freq_dict by it's values (word count) in descending order,
        then returns an ordered list of tuples.
    '''
    if isinstance(source_text, str):
        word_list = source_text.split()
    elif isinstance(source_text, list):
        word_list = source_text
    else:
        print("*** invalid source text ***")
        exit()
    remove = []
    # r = re.compile(r"[^a-zA-Z0-9-,.?!()]+")

    for i in reversed(range(len(word_list))):
        # remove any character that isn't a-z or 0-9 at the beginning or end of each string
        # word_list[i] = sub(r'^\W+|$\W+', '', word_list[i])
        # r.sub("", word_list[i])
        # remove from word list if it's an empty string.
        if word_list[i] == '':
            word_list.pop(i)
    return word_list

def get_histogram(word_list, type="SD", freq_dict=None):
    if freq_dict is None:
        freq_dict = dict()
    for word in word_list:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1

    sorted_tuples = sorted(freq_dict.items(), key=itemgetter(1), reverse=True)
    if type == "SD":
        # sorted dictionary
        return dict(sorted_tuples)
    if type == "SL":
        # sorted 2d list
        return list(sorted_tuples)
    if type == "ST":
        # sorted list of tuples.
        return sorted_tuples

def histogram_file(file_dir):
    ''' Opens the file containing text and converts it to a list of words. '''
    try:
        with open(file_dir, 'r') as file:
            text_str = file.read()
    except Exception as e:
        print(e)
        exit()
    return text_str

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

def frequency(histogram, word):
    ''' finds the count for one word '''
    try:
        return histogram[word]
    except:
        # Word not found
        return 0

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

def sample_by_frequency(histogram, tokens):
    ''' Select a word based on frequency '''
    # TODO: optimize. for loop to count total range (to pick random number) and for loop that returns when it's in range
    words = []
    if isinstance(histogram, dict):
        if len(histogram) > 1:
            selection = randrange(0, tokens)
            total = 0
            for word, count in histogram.items():
                total += count
                if selection <= total:
                    if word is not None:
                        return word
                    else:
                        return 0
        else:
            return list(histogram)[0][0]
    else:
        if len(histogram) > 1:
            selection = randrange(0, tokens)
            total = 0
            for i in range(len(histogram)):
                total += histogram[i][1]
                if selection <= total:
                    if histogram[i][0] is not None:
                        words.append(histogram[i][0])
                        break
                    else:
                        return 0
        else:
            return histogram[0][0]
    if len(words) > 1:
        return words
    return words[0]

def bulk_sample(histogram, tokens, limit):
    result = []
    for _ in range(limit):
        result.append(sample_by_frequency(histogram, tokens))
    return result

def markov(word_list):
    word_pairs = {}
    word_pairs['__start__'] = [word_list[0]]
    word_pairs[word_list[-1]] = ['__end__']

    for i in range(1, len(word_list)):
        if word_list[i-1] in word_pairs.keys():
            # if self.word_list[i] in word_pairs[self.word_list[i-1]]:
            #     pass
            # else:
            word_pairs[word_list[i-1]].append(word_list[i])
        else:
            word_pairs[word_list[i-1]] = [word_list[i]]
    for word in word_pairs.keys():
        word_pairs[word] = get_histogram(word_pairs[word], 'SL')
    return word_pairs

def random_sentence(markov, min=4, max=20):
    sentence = []
    sentence.append(sample_by_frequency(markov['__start__'], get_total_tokens(markov['__start__'])))
    while True:
        next_word = sample_by_frequency(markov[sentence[-1]], get_total_tokens(markov[sentence[-1]]))
        print(next_word)
        if next_word == '__end__' and len(sentence) >= min or len(sentence) >= max:
            return sentence
        elif not next_word == '__end__':
            sentence.append(next_word)

# if __name__ == '__main__':
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

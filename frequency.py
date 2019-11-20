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
            source_text = self.histogram_file(source_text)

        # To load from a word_list or string, don't pass in a flag.
        self.word_list = self.get_word_list(source_text)

        self.histogram = self.get_histogram()

        self.total_tokens = self.get_total_tokens()
        self.total_types = self.unique_words()

        self.markov_chain = self.markov()

    def get_word_list(self, source_text):
        ''' Splits text_str into a list of lowercase words
            Creates an empty dictionary.
            For every word in the list that was passed in:
                If it's already in the dictionary, increase it's value by one.
                Otherwise, add it to the dictionary and set it's value to one.
            Sorts freq_dict by it's values (word count) in descending order,
            then returns an ordered list of tuples.
        '''
        if isinstance(source_text, str):
            source_text = source_text.replace("-", " ").lower()
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

    def get_histogram(self, word_list=None, type="SD", freq_dict=None):
        if word_list is None:
            word_list = self.word_list
        if freq_dict is None:
            freq_dict = {}
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

    def histogram_file(self, file_dir='test.txt'):
        ''' Opens the file containing text and converts it to a list of words. '''
        try:
            with open(file_dir, 'r') as file:
                text_str = file.read()
        except Exception as e:
            print(e)
            exit()
        return text_str

    def unique_words(self):
        ''' this function is totally useless, since len() is shorter,
            but i guess this is more clear about what it's doing '''
        return len(self.histogram)

    def get_total_tokens(self):
        return sum(self.histogram.values())

    def frequency(self, word):
        ''' finds the count for one word '''
        try:
            return self.histogram[word]
        except:
            # Word not found
            return 0

    def top_count(self, top_num=0):
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
            temp_histogram = list(self.histogram.items())
            print(f"Top {top_num} words:")
            if 0 < top_num < len(temp_histogram):
                for i in range(top_num):
                    print(f"{i+1}.| {temp_histogram[i][0]}: {self.frequency(temp_histogram[i][0])}")
            else:
                for i in range(len(temp_histogram)):
                    print(f"{i + 1}.| {temp_histogram[i][0]}: {self.frequency(temp_histogram[i][0])}")
        except Exception as e:
            print(e)
            print("*** Invalid histogram ***")
            exit()

    def bulk_frequency(self, num):
        ''' finds all words that have the specified count '''
        print(f"All words with the count {num}:")
        count = 0
        words = []
        for word, freq in dict(self.histogram).items():
            if freq == num:
                count += 1
                print(f"{count}.| {word}")
                words.append(word)
        if count == 0:
            print(f"No words found.")
            return None
        return words

    def sample_by_frequency(self, selection=None):
        ''' Select a word based on frequency '''
        # TODO: optimize. for loop to count total range (to pick random number) and for loop that returns when it's in range
        if selection is None:
            selection = randrange(0, self.total_tokens)
        total = 0
        for word, count in self.histogram.items():
            total += count
            if selection <= total:
                if word is not None:
                    return word
                else:
                    self.sample_by_frequency()

    def markov(self):
        word_pairs = {}
        word_pairs['__start__'] = [self.word_list[0]]
        word_pairs['__end__'] = [self.word_list[-1]]
        
        for i in range(1, len(self.word_list)):
            if self.word_list[i-1] in word_pairs.keys():
                # if self.word_list[i] in word_pairs[self.word_list[i-1]]:
                #     pass
                # else:
                word_pairs[self.word_list[i-1]].append(self.word_list[i])
            else:
                word_pairs[self.word_list[i-1]] = [self.word_list[i]]

        for word in word_pairs.keys():
            word_pairs[word] = self.get_histogram(word_pairs[word], 'SL')
        print(word_pairs)
        return word_pairs

if __name__ == '__main__':
    ''' py frequency.py                   | to use default filename (test.txt)
        py frequency.py <filename>        | to specify your source text file 
        py frequency.py <raw source text> | to pass in your own source text
    '''

    if len(argv) == 2:
        # if filename is passed in
        main_histogram = Histogram(argv[1], 'f')
    elif len(argv) > 2:
        # if words are passed in
        main_histogram = Histogram(" ".join(argv[1:]))
    else:
        fish_text = 'one fish two fish red fish blue fish'
        fishogram = Histogram(fish_text)
        print()
        woodchuck_text = ('how much wood would a wood chuck chuck'
                          ' if a wood chuck could chuck wood')
        woodogram = Histogram(woodchuck_text)
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

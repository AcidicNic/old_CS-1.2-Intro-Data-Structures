from random import randrange, shuffle, sample
from sys import argv
from operator import itemgetter
from sys import exit
from re import sub, split


class Frequency():
    def __init__(self, source_text, flag=None):
        # set the flag to 'F' to load text from a file
        if flag.lower() == 'f':
            self.histogram = self.histogram_file()
        # To load from a word_list or string, don't pass in a flag.
        else:
            self.histogram = self.get_histogram(source_text)

        self.total_tokens = self.total_tokens(self.histogram)


    def get_histogram(self, source_text, type="SD"):
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
            word_list = split(r"[ -_]|\n", source_text)
        elif isinstance(source_text, list):
            word_list = source_text
        else:
            print("*** invalid source text ***")
            exit()
        remove = []
        for i in range(len(word_list)):
            # remove any character that isn't a-z or 0-9 at the beginning or end of each string
            word_list[i] = sub(r'^\W+|$\W+', '', word_list[i])
            # remove from word list if it's an empty string.
            if word_list[i] == '':
                remove.append(i)
        for i in remove[::-1]:
            word_list.pop(i)
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
        return get_histogram(text_str)


def unique_words(histogram):
    ''' this function is totally useless, since len() is shorter,
        but i guess this is more clear about what it's doing '''
    return len(histogram)


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
    for word, freq in dict(histogram).items():
        if freq == num:
            count += 1
            print(f"{count}.| {word}")
    if count == 0:
        print(f"No words found.")


def get_weight():
    pass


def total_tokens(histogram):
    return sum(histogram.values())


def sample_by_frequency(histogram, total_tokens, selection=None):
    ''' Select a word based on frequency '''
    # TODO: optimize. for loop to count total range (to pick random number) and for loop that returns when it's in range
    if selection is None:
        selection = randrange(0, total_tokens)
    total = 0
    for word, count in histogram.items():
        total += count
        if selection <= total:
            if word is not None:
                return word
            else:
                sample_by_frequency(histogram)


if __name__ == '__main__':
    ''' py frequency.py                   | to use default filename (test.txt)
        py frequency.py <filename>        | to specify your source text file 
        py frequency.py <raw source text> | to pass in your own source text
    '''
    if len(argv) == 2:
        # if filename is passed in
        main_histogram = histogram_file(argv[1])
    elif len(argv) > 2:
        # if words are passed in
        main_histogram = get_histogram(" ".join(argv[1:]))
    else:
        # else, use default filename
        main_histogram = histogram_file()

    _word_list = []
    for i in range(10000):
        _word_list.append(sample_by_frequency(main_histogram))
    next_histogram = get_histogram(_word_list)
    top_count(next_histogram)

    top_count(main_histogram, 10)


    # print(f"Total words: {unique_words(main_histogram)}")
    #
    # # print(f'"the" is found {str(frequency(histogram, 'the'))} times')
    # # print(f'"fakkkeworddd" is found {str(frequency(histogram, 'fakkkeworddd'))} times')
    # print(main_histogram)
    # top_count(main_histogram, 20)
    # # bulk_frequency(histogram, 7)
    # print(f'Sample by Frequency: {sample_by_frequency(main_histogram)}')

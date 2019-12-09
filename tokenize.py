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
        return None
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


def histogram_file(file_dir):
    ''' Opens the file containing text and converts it to a list of words. '''
    try:
        with open(file_dir, 'r') as file:
            text_str = file.read()
    except Exception as e:
        print(e)
        exit()
    return text_str


# if __name__ == '__main__':
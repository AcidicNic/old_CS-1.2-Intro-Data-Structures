from operator import itemgetter


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


if __name__ == '__main__':
    pass
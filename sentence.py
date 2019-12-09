def markov(word_list, word_pairs={}):
    word_pairs['__start__'] = [word_list[0]]
    # word_pairs['__end__'] = [word_list[-1]]
    __end__ = [word_list[-1]]

    for i in range(1, len(word_list)):
        if word_list[i-1][-1] in ['.', '?', '!', '"']:
            __end__.append(word_list[i-1])
            word_pairs['__start__'].append(word_list[i])

        if word_list[i-1] in word_pairs.keys():
            word_pairs[word_list[i-1]].append(word_list[i])
        else:
            word_pairs[word_list[i-1]] = [word_list[i]]
    for word in word_pairs.keys():
        word_pairs[word] = get_histogram(word_pairs[word], 'SL')
    word_pairs['__end__'] = __end__
    return word_pairs


def random_sentence(markov, min=4):
    sentence = [sample_by_frequency(markov['__start__'], get_total_tokens(markov['__start__']))]
    try:
        while True:
            next_word = sample_by_frequency(markov[sentence[-1]], get_total_tokens(markov[sentence[-1]]))
            sentence.append(next_word)
            if next_word in markov['__end__'] and len(sentence) >= min:
                return " ".join(sentence)
    except Exception as e:
        # print("Error: "+ repr(e))
        pass


def bulk_sentences(markov, max):
    count = 0
    results = []
    while count < max:
        rand_sentence = random_sentence(markov)
        if rand_sentence is not None:
            results.append(rand_sentence)
            count += 1
    return results

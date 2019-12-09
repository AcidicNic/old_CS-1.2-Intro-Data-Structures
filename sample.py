def sample_by_frequency(histogram, tokens):
    ''' Select a word based on frequency '''
    if isinstance(histogram, dict):
        if len(histogram) > 1:
            selection = randint(0, tokens)
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
            selection = randint(0, tokens)
            total = 0
            for i in range(len(histogram)):
                total += histogram[i][1]
                if selection <= total:
                    if histogram[i][0] is not None:
                        return histogram[i][0]
                    else:
                        return 0
        else:
            return histogram[0][0]


def bulk_sample(histogram, tokens, limit):
    result = []
    for _ in range(limit):
        result.append(sample_by_frequency(histogram, tokens))
    return result


if __name__ == '__main__':
    pass
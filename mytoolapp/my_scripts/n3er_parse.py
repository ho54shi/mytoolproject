
def tasu(a, b):
    print(a+b)


def parse(n3ered_text):
    temp_words_list = []
    temp_refs_list = []
    line = [c.split('/') for c in n3ered_text.rstrip().split(' ')]

    temp_words_list += [c[0] for c in line]
    temp_refs_list += [c[1] for c in line]

    words_list = []
    refs_list = []
    indices = []
    for id, (word, ref) in enumerate(zip(temp_words_list, temp_refs_list)):
        if ref != 'O':
            indices += [id]
            words_list += [word]
            refs_list += [ref]
    return indices, words_list, refs_list

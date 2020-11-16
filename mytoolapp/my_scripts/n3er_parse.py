
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
            ref = ref.split('-')[0]
            indices += [id]
            words_list += [word]
            refs_list += [ref]
    return indices, words_list, refs_list


def display_text(n3ered_text):
    words_list = []
    line = [c.split('/') for c in n3ered_text.rstrip().split(' ')]
    words_list += [c[0] for c in line]
    display_text = "　".join(words_list)  # 全角空白
    return display_text


def new_parse(n3ered_text):
    temp_words_list = []
    temp_refs_list = []
    line = [c.split('/') for c in n3ered_text.rstrip().split(' ')]

    print("line::")
    print(line)

    temp_words_list += [c[0] for c in line]
    temp_refs_list += [c[1] for c in line]

    words_list = []
    refs_list = []
    indices = []
    prev_words = []
    prev_label = ""
    for id, (word, ref) in enumerate(zip(temp_words_list, temp_refs_list)):
        if ref != 'O':

            cur_label = ref.split('-')[0]  # B or I
            BorI = ref.split('-')[1]
            if(BorI == 'B'):
                if(len(prev_words) < 1):  # i.g.) O B
                    prev_label = cur_label
                    prev_word = word
                    prev_words += [prev_word]
                elif(len(prev_words) > 0):  # B B と，Bが連続したエラーのとき
                    words_list += [prev_word]
                    refs_list += [prev_label]
                    prev_word = word
                    prev_label = cur_label
            elif(BorI == 'I'):
                if(len(prev_words) < 1):  # O I I B
                    BorI = 'B'
                    prev_word = word
                    words_list += [word]
                    refs_list += [cur_label]
                # O B I I ...
                elif(len(prev_words) > 0):
                    prev_word = word
                    prev_words += [word]
                    prev_label = cur_label

        elif(len(prev_words) > 0):

            words_list += ["　".join(prev_words)]
            refs_list += [prev_label]
            indices += [id]
            prev_words = []
        elif(ref == 'O'):
            words_list += [word]
            refs_list += ['0']

    return words_list, refs_list

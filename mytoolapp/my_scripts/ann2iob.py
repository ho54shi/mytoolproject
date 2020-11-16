
start_idx = 2  # fixed
end_idx = 3  # fixed
label_idx = 4  # fixed


def train_parse(queryset, save_path):
    IOBs = []
    for data in queryset:
        text = data.text
        anns = data.anns
        iob_text = ann_detail(text, anns)

        IOBs += [iob_text]
    with open(save_path, mode="w") as f:
        for iob in IOBs:
            f.write(iob + '\n')


def ann_detail(text, anns):
    IOBs = []

    text = text.rstrip("\n")
    anns = anns.rstrip("\n")
    words = text.split('　')
    refs = anns.split('\t')
    list_refs = []
    for ref in refs:
        ref = ref.split(',')
        ref[start_idx] = int(ref[start_idx])  # str2int
        ref[end_idx] = int(ref[end_idx])  # str2int
        list_refs += [ref]
    list_refs.sort(key=lambda x: int(x[2]))

    charsum = 0
    ref_idx = 0  # ite

    label_idx = 4  # fixed
    between_flag = False
    refs_empty = False
    parsed_ann = ""

    for word in words:
        parsed_ann = word + "/O"  # initialization
        if(refs_empty == False):
            ref_start_offset = list_refs[ref_idx][start_idx]
            ref_end_offset = list_refs[ref_idx][end_idx]
            ref_labelname = list_refs[ref_idx][label_idx]
            if(charsum == ref_start_offset):
                if(charsum + len(word) == ref_end_offset):  # only one word
                    ref_idx += 1
                    between_flag = False
                else:  # begin
                    between_flag = True
                parsed_ann = word + "/" + ref_labelname + "-B"

            elif(between_flag):
                if(charsum + len(word) == ref_end_offset):  # end
                    ref_idx += 1
                    between_flag = False

                    # else => between
                parsed_ann = word + "/" + ref_labelname + "-I"

            charsum += len(word) + 1  # double-byte blank
            if(ref_idx == len(list_refs)):  # 終了
                refs_empty = True

        iob = parsed_ann
        IOBs += [iob]

    return " ".join(IOBs)  # 半角でないとassertionError in util.py :line 26


def file_merge(file1_path, file2_path, output_path):
    with open(file1_path) as f:
        lines1 = f.readlines()

    with open(file2_path) as f:
        lines2 = f.readlines()

        allLines = []
        allLines.extend(lines1)
        allLines.extend(lines2)

    with open(output_path, mode="w") as f:
        for line in allLines:
            f.write(line)

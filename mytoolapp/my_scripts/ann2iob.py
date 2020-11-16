
start_idx = 2  # fixed
end_idx = 3  # fixed
label_idx = 4  # fixed


def func(text_lines, anns_lines, save_path):
    IOBs = []
    for text, anns in zip(text_lines, anns_lines):
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
        parsed_ann = ""
        parsed_anns = []

        for word in words:
            parsed_ann = word + "/O"  # initialization
            ref_start_offset = list_refs[ref_idx][start_idx]
            ref_end_offset = list_refs[ref_idx][end_idx]
            ref_labelname = list_refs[ref_idx][label_idx]
            if(charsum == ref_start_offset):
                if(charsum + len(word) == ref_end_offset):  # only one word
                    ref_idx += 1
                    between_flag = False
                else:  # begin
                    between_flag = True
                    seq_label = ref_labelname
                parsed_ann = word + "/B-" + ref_labelname

            elif(between_flag):
                if(charsum + len(word) == ref_end_offset):  # end
                    ref_idx += 1
                    between_flag = False
                    # else => between
                parsed_ann = word + "/I-" + ref_labelname

            parsed_anns += [parsed_ann]
            charsum += len(word) + 1  # double-byte blank
            if(ref_idx == len(list_refs)):
                break

        iob = " ".join(parsed_anns)
        IOBs += [iob]

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
                parsed_ann = word + "/B-" + ref_labelname

            elif(between_flag):
                if(charsum + len(word) == ref_end_offset):  # end
                    ref_idx += 1
                    between_flag = False

                    # else => between
                parsed_ann = word + "/I-" + ref_labelname

            charsum += len(word) + 1  # double-byte blank
            if(ref_idx == len(list_refs)):  # 終了
                refs_empty = True

        iob = parsed_ann
        IOBs += [iob]

    #print("IOBs: ", end="")
    # print("　".join(IOBs))
    return "　".join(IOBs)

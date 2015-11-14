import sys

"""
    This script is used to transform these phonemes in lexicon to indice
    These indice are always defined in data/lang/phones.txt



"""

def parse_arguments(arg_elements):
    args = {}
    arg_num = len(arg_elements) / 2
    for i in xrange(arg_num):
        key = arg_elements[2*i].replace("--","").replace("-", "_")
        args[key] = arg_elements[2*i+1]
    return args

def parse_phoneme_index(phoneme_to_index):
    phoneme_dict = {}
    phoneme_fread = open(phoneme_to_index, mode='r')
    for every_phonome in phoneme_fread.readlines():
        units = every_phonome.strip().split(sep=' ')
        phoneme_dict[units[0]] = units[1]
    phoneme_fread.close()
    return phoneme_dict


def getIDDictFromFile(file_name):
    id_dict = {}
    if len(file_name) == 0:
        return id_dict

    fread = open(file_name, mode='r')
    for entry in fread.readlines():
        scp_id = entry.split(' ')
        scp_id = scp_id.strip()
        id_dict[scp_id] = 1
    fread.close()
    return id_dict


if __name__ == '__main__':
    arg_elements = [sys.argv[i] for i in range(1, len(sys.argv))]
    arguments = parse_arguments(arg_elements)

    all_data_scp = str(arguments['hkust-data-scp'])
    subset_ids = str(arguments['subset-ids'])
    scp_id_dict = getIDDictFromFile(subset_ids)
    data_fread = open(all_data_scp, mode='r')
    for entry in data_fread.readlines():
        clean_entry = entry.strip()
        char_pron = clean_entry.split(sep=' ')
        index_arr = ''
        for phoneme in char_pron[1:]:
            if phoneme_dict.has_key(phoneme):
                index_arr += phoneme_dict[phoneme] + " "
        char_pron = char_pron[0] + ' ' + index_arr
        print(char_pron)
    data_fread.close()

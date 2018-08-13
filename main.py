import os
import collections
import hashlib


def get_all_files(dir):
    file_list = []
    for (path, dirs, files) in os.walk(dir):
        for file in files:
            file_path = os.path.join(path, file)
            if not os.path.exists(file_path):
                print(file_path + 'not exists')
            else:
                file_list.append(file_path)
    return file_list


def get_file_md5(file_path, block_size=1024):
    md5_value = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5_value.update(data)
    return md5_value.hexdigest()


def get_file_size(file_path):
    return os.path.getsize(file_path)


def get_file_suffix(file_path):
    return file_path.split('.')[-1].lower()


def get_duplicated_md5(md5_list):
    md5_set = set()
    duplicated_md5_set = set()
    for item in md5_list:
        if item not in md5_set:
            md5_set.add(item)
        else:
            duplicated_md5_set.add(item)

    return list(duplicated_md5_set)


def get_file_by_md5(file_list, md5_list):
    ret_file_list = []
    if not md5_list or not file_list:
        return None
    for md5 in md5_list:
        for file in file_list:
            if file['md5'] == md5:
                ret_file_list.append(file)

    return ret_file_list


def main():
    # test_path = '/Users/CJ/study/test'
    test_path = '/Users/CJ/Documents/KindleBooks/'
    file_list = []
    md5_dict = collections.defaultdict(int)
    for file_path in get_all_files(test_path):
        md5 = get_file_md5(file_path)
        file_dict = {'path': file_path,
                     'suffix': get_file_suffix(file_path),
                     'size': get_file_size(file_path),
                     'md5': md5,

                     }
        if md5 not in md5_dict:
            md5_dict[md5] = 1
        else:
            md5_dict[md5] += 1
        file_dict['index'] = md5_dict[md5]
        file_list.append(file_dict)

    duplicated_md5_list = [k for k, v in md5_dict.items() if v > 1]
    duplicated_file_list = get_file_by_md5(file_list, duplicated_md5_list)

    for file in duplicated_file_list:
        print(file)


if __name__ == '__main__':
    main()

#! /usr/bin/python3
import os
import sys
import hashlib


def addToDict(dictionary, k, value):
    if k not in dictionary.keys():
        dictionary[k] = []
    if isinstance(value,list):
        for v in list(value):
            dictionary[k].append(v)
    else:
        dictionary[k].append(value)


def generator(directory):
    directory = os.path.join(os.getcwd(), directory)
    dir_list = os.listdir(directory)
    result = {}
    for x in dir_list:
        pom = os.path.join(directory, x)
        if os.path.isdir(pom):
            files = generator(os.path.join(directory, x))
            for k, v in files.items():
                addToDict(result, k, v)
        elif os.path.isfile(pom):
            try:
                hash_md5 = hashlib.md5()
                with open(pom, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                created_key = (hash_md5.hexdigest(), os.stat(pom).st_size)
                addToDict(result, created_key, pom)
            except PermissionError:
                pass
    return result


if __name__ == "__main__":
    try:
        table = [x for x in generator(sys.argv[1]).values() if len(x) >1]
        for group in table:
            print('\n'.join(group),end='\n'+'-'*80+'\n')
    except (IndexError, FileNotFoundError):
        print("Type valid directory")

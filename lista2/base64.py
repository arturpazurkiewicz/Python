#! /usr/bin/python3
import sys

TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def encode(text):
    bit_str = ""
    result = ""

    for char in text:
        bit_str += bin(char).lstrip("0b").zfill(8)

    brackets = [bit_str[x:x + 6] for x in range(0, len(bit_str), 6)]

    for bracket in brackets:
        if len(bracket) < 6:
            bracket = bracket + (6 - len(bracket)) * "0"
        result += TABLE[int(bracket, 2)]

    return result


def decode(text):
    bit_str = ""
    result = ""

    for char in text:
        if char in TABLE:
            bit_str += bin(TABLE.index(char)).lstrip("0b").zfill(6)

    brackets = [bit_str[x:x + 8] for x in range(0, len(bit_str), 8)]

    for bracket in brackets:
        result += chr(int(bracket, 2))
    return result.encode("latin-1")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--encode":
            r = open(sys.argv[3], "w")
            with open(sys.argv[2], "rb") as f:
                data = f.read()
                r.write(encode(data))
            r.close()
        elif sys.argv[1] == "--decode":
            r = open(sys.argv[3], "wb")
            with open(sys.argv[2], "r") as f:
                data = f.read()
            r.write(decode(data))
            r.close()
        else:
            print("Type --encode or --decode")
            exit(0)

    except FileNotFoundError:
        print("File does not exist")
    except IndexError:
        print("Write:\n", "--encode/--decode", "[file]", "[resultFile]")

#! /usr/bin/python3


def transpose(matrix):
    return [' '.join([matrix[y].split()[x] for y in range(len(matrix))]) for x in range(len(matrix[0].split()))]


if __name__ == "__main__":
    t = ["a b c", "d e f", "g h i", "j k l"]
    transposed = transpose(t)
    print(transposed)
    print(transpose(transposed))

    t = ["1.1 2.2 3.3", "4.4 5.5 6.6", "7.7 8.8 9.9"]
    transposed = transpose(t)
    print(transposed)
    print(transpose(transposed))

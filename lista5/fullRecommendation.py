#!/usr/bin/python3
import argparse
import numpy as np
from scipy.sparse import *
from scipy.sparse.linalg import norm


def divide_sparse_matrix(x, y):
    return x @ diags(1 / y)


def get_suggestions(y, x, x_t):
    z = x.dot(y.transpose() / norm(y, ord=1))
    q = csr_matrix.dot(x_t, (z / norm(z, ord=1)).toarray())
    result = [(q[g][0], g) for g in range(len(q))]
    result.sort(reverse=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-rat", "--ratings", help="type filename with ratings",
                        default="ratings.csv")
    parser.add_argument("-mov", "--movies", help="type filename with movies",
                        default="movies.csv")
    parser.add_argument("-s", "--suggestions",
                        help="type the number of suggestions", default="3")
    parser.add_argument("-t", "--test", help="enable testing mode",
                        action="store_true")

    args = parser.parse_args()
    args.suggestions = int(args.suggestions)

    np.seterr(divide='ignore', invalid='ignore')
    try:
        with open(args.movies, "r") as f:
            f.readline()
            from_movie_id = {}
            to_movie_id = {}
            counter = 0
            for x_data in f.read().splitlines():
                y = x_data.split(',')
                from_movie_id[int(y[0])] = counter
                if len(y) == 3:
                    to_movie_id[counter] = (y[1], int(y[0]))
                else:
                    to_movie_id[counter] = (x_data.split('"')[1], int(y[0]))
                counter += 1
    except FileNotFoundError:
        print("Type valid file with movies")
        exit(0)
    try:
        with open(args.ratings, "r") as f:
            f.readline()
            ratings = ([], ([], []))
            from_user_id = {}
            to_user_id = {}
            counter = 0
            for x_data in f.read().splitlines():
                y = x_data.split(',')
                u = int(y[0])
                if from_user_id.get(u) is None:
                    from_user_id[u] = counter
                    to_user_id[counter] = u
                    counter += 1
                ratings[0].append(float(y[2]))
                ratings[1][0].append(from_user_id.get(u))
                ratings[1][1].append(from_movie_id.get(int(y[1])))
    except FileNotFoundError:
        print("Type valid file with ratings")
        exit(0)
    movies_counter = len(from_movie_id)

    x_data = csr_matrix(ratings)
    x1 = divide_sparse_matrix(x_data, norm(x_data, axis=0))
    x1_t = x1.transpose()
    print("Data loaded")
    if args.test:
        test_y = np.zeros((movies_counter, 1))
        test_y[from_movie_id.get(2571)] = 5  # patrz movies.csv  2571 - Matrix
        test_y[from_movie_id.get(32)] = 4  # 32 - Twelve Monkeys
        test_y[from_movie_id.get(260)] = 5  # 260 - Star Wars IV
        test_y[from_movie_id.get(1097)] = 4
        y = csr_matrix(test_y).transpose()
        for x in get_suggestions(y, x1, x1_t):
            print(x[0], to_movie_id.get(x[1])[1])
    else:
        for i in range(len(to_user_id)):
            y = x_data.getrow(i)
            result = get_suggestions(y, x1, x1_t)
            print('User ID', to_user_id[i], 'propositions:')
            j = 0
            s = 0
            non_zero = y.nonzero()[1]
            while j < movies_counter and args.suggestions > s:
                if j not in non_zero:
                    print('    ', to_movie_id.get(result[j][1])[0])
                    s += 1
                j += 1

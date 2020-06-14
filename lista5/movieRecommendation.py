#!/usr/bin/python3
import argparse
import numpy as np


def get_suggestions(y, x, x_t):
    z = x.dot(y / np.linalg.norm(y))
    q = np.dot(x_t, z / np.linalg.norm(z))
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

    try:
        with open(args.movies, "r") as f:
            f.readline()
            movies_data = f.read()
            from_movie_id = {}
            to_movie_id = {}
            counter = 0
            for x_data in movies_data.splitlines():
                y = x_data.split(',')
                if int(y[0]) < 10000:
                    from_movie_id[int(y[0])] = counter
                    if len(y) == 3:
                        to_movie_id[counter] = (y[1], int(y[0]))
                    else:
                        to_movie_id[counter] = (
                            x_data.split('"')[1], int(y[0]))
                    counter += 1
    except FileNotFoundError:
        print("Type valid file with movies")
        exit(0)
    try:
        with open(args.ratings, "r") as f:
            f.readline()
            ratings_data = f.read()
            ratings = []
            from_user_id = {}
            to_user_id = {}
            counter = 0
            for x_data in ratings_data.splitlines():
                y = x_data.split(',')
                u = int(y[0])
                m = int(y[1])
                if m < 10000:
                    if from_user_id.get(u) is None:
                        from_user_id[u] = counter
                        to_user_id[counter] = u
                        counter += 1
                    ratings.append([u, m, float(y[2])])
    except FileNotFoundError:
        print("Type valid file with ratings")
        exit(0)
    x_data = np.zeros((len(from_user_id), len(from_movie_id)))
    movies_counter = len(from_movie_id)

    for rating in ratings:
        y = from_movie_id.get(rating[1])
        x_data[from_user_id.get(rating[0])][y] = rating[2]
    a = np.linalg.norm(x_data, axis=0)
    x1 = np.nan_to_num(np.divide(x_data, a, where=a != 0))
    x1_t = x1.transpose()

    if args.test:
        y = np.zeros((movies_counter, 1))
        y[from_movie_id.get(2571)] = 5  # patrz movies.csv  2571 - Matrix
        y[from_movie_id.get(32)] = 4  # 32 - Twelve Monkeys
        y[from_movie_id.get(260)] = 5  # 260 - Star Wars IV
        y[from_movie_id.get(1097)] = 4
        y.transpose()
        for x in get_suggestions(y, x1, x1_t):
            print(x[0], to_movie_id.get(x[1])[1])
    else:
        for i in range(len(to_user_id)):
            y = x_data[i].reshape((-1, 1))
            result = get_suggestions(y, x1, x1_t)
            print('User ID', to_user_id[i], 'propositions:')
            j = 0
            s = 0
            while j < movies_counter and args.suggestions > s:
                if x_data[i][result[j][1]] == 0:
                    print('    ', to_movie_id.get(result[j][1])[0])
                    s += 1
                j += 1

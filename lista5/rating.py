#!/usr/bin/python3
import argparse
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-rat", "--ratings", help="type filename with ratings",
                        default="ratings.csv")
    parser.add_argument("-mov", "--movies", help="type filename with movies",
                        default="movies.csv")
    parser.add_argument("-e", "--exercise", help="choose working mode 1 or 2",
                        default='1', choices=['1', '2'])
    parser.add_argument("-i", "--test_set", help="Type test set",
                        default='200')

    args = parser.parse_args()
    args.test_set = int(args.test_set)
    try:
        with open(args.movies, "r") as f:
            f.readline()
            movies_data = f.read()
            movies = {}
            for x in movies_data.splitlines():
                y = x.split(',')
                if len(y) == 3:
                    movies[int(y[0])] = y[1]
                else:
                    movies[int(y[0])] = x.split('"')[1]
            for x in range(len(movies)):
                if movies.get(x) == "Toy Story (1995)":
                    main_id = x
                    break
            if main_id is None:
                print("Could not find: Toy Story (1995)")
                exit(0)
    except FileNotFoundError:
        print("Type valid file with movies")
        exit(0)
    try:
        with open(args.ratings, "r") as f:
            f.readline()
            ratings_data = f.read()
            ratings = []
            for x in ratings_data.splitlines():
                y = x.split(',')
                ratings.append([int(y[0]), int(y[1]), float(y[2])])
    except FileNotFoundError:
        print("Type valid file with ratings")
        exit(0)

    users_dict = {}
    data_y = []
    counter = 0
    for u in ratings:
        if u[1] == main_id:
            users_dict[u[0]] = counter
            data_y.append(u[2])
            counter += 1
    data_y = np.reshape(data_y, (-1, 1))
    data_x = np.zeros((len(data_y), 10000))
    for rating in ratings:
        if rating[0] in users_dict and rating[1] <= 10000 + 1 \
                and rating[1] != main_id:
            data_x[((users_dict.get(rating[0])), rating[1] - 2)] = rating[2]

    if args.exercise == '1':
        for m in [10, 1000, 10000]:
            x = data_x[:, :m]
            lr = LinearRegression().fit(x, data_y)
            y_pred = lr.predict(x)
            plt.plot(x, 'o', color='blue')
            plt.plot(y_pred, 'o', color='red')
            plt.title(
                'm = ' + str(m) + ', accuracy = ' + str(lr.score(x, data_y)))
            plt.show()
    else:
        y = data_y[:args.test_set]
        y_test = data_y[args.test_set:]
        x = data_x[:args.test_set]
        x_test = data_x[args.test_set:]
        for m in [10, 100, 200, 500, 1000, 10000]:
            x1 = x[:, :m]
            x_t = x_test[:, :m]
            lr = LinearRegression().fit(x1, y)
            y_pred = lr.predict(x_t)
            plt.plot(y_test, 'o', color='blue', label='real data')
            plt.plot(y_pred, 'o', color='red', label='prediction')
            plt.title('m = ' + str(m) + ', test set = ' + str(
                args.test_set) + ', accuracy = ' + str(
                lr.score(data_x[:, :m], data_y)))
            plt.legend()
            plt.show()

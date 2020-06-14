#! /usr/bin/python3
import math
import sys
import random


def miller_rabin_test(n, rounds):
    if n != int(n):
        return False
    n = int(n)
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False
    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(rounds):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
    return True


def get_prime(size):
    number = 0
    while not miller_rabin_test(number, 20):
        number = random.randrange(10 ** size, 10 ** (size + 1) - 1, 1)
    return number


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


def quick_power_with_mod(base, power, mod):
    result = 1
    base = base % mod
    while power > 0:
        if power % 2 == 1:
            result = (result * base) % mod
        power = int(power) >> 1
        base = (base * base) % mod
    return result


def encrypt(n, e, text):
    cipher = ""
    for char in text:
        cipher += str(quick_power_with_mod(ord(char), e, n)) + " "
    cipher = cipher[:-1]
    return cipher


def decrypt(n, d, text):
    words = text.split()
    result = ""
    for word in words:
        result += chr(quick_power_with_mod(int(word), d, n))
    return result


if __name__ == "__main__":
    try:
        order = sys.argv[1]

        if order == "--gen-keys":
            size = int(sys.argv[2])
            size = int(math.log(2) / math.log(10) * size)
            p = get_prime(size)
            q = get_prime(size)
            n = p * q
            euler = (p - 1) * (q - 1)
            e = 2
            while not math.gcd(e, euler) == 1:
                e = random.randrange(2, euler, 1)
            d = multiplicative_inverse(e, euler)

            with open("key.pub", "w") as f:
                f.write(str(n)+" "+str(e))
            with open("key.prv", "w") as f:
                f.write(str(n)+" "+str(d))

        elif order == "--encrypt":
            text = str(sys.argv[2])
            with open("key.pub", "r") as f:
                words = f.read().split()
                n = int(words[0])
                e = int(words[1])
            try:
                with open(text, "r") as f:
                    text = encrypt(n, e, f.read())
            except FileNotFoundError:
                text = (encrypt(n, e, text))
            try:
                with open(sys.argv[3], "w") as f:
                    f.write(text)
            except IndexError:
                print(text)

        elif order == "--decrypt":
            try:
                with open(sys.argv[2], "r") as f:
                    text = f.read()
            except (FileNotFoundError, OSError):
                text = sys.argv[2]
            with open("key.prv", "r") as f:
                lines = f.read().split()
                n = int(lines[0])
                d = int(lines[1])
            try:
                with open(sys.argv[3], "w") as f:
                    f.write(decrypt(n, d, text))
            except IndexError:
                print(decrypt(n, d, text))
        else:
            raise IndexError
    except IndexError:
        print("Type:", "--gen-keys [size]", "--encrypt [file/string] [to file]", "--decrypt [file/string]", sep="\n    ")

    except FileNotFoundError:
        print("Make sure that key file exists")
    except:
        print("Błędne klucze")
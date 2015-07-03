#!/usr/bin/env python3

import irc
import random


def add_words(cache, words):
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i + 1], words[i + 2]
        except IndexError:
            break
        key = (first, second)
        if key not in cache:
            cache[key] = []
        cache[key].append(third)


def generate_sentence(cache):
    key = random.choice([key for key in cache.keys()])

    sentence = list()
    first, second = key
    sentence.extend(key)

    while key in cache:
        third = random.choice(cache[key])
        sentence.append(third)
        key = (second, third)
        second = third

    return ' '.join(sentence)


def main():
    cache = dict()
    while True:
        words = input('>').split()
        add_words(cache, words)
        print(generate_sentence(cache))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# import irc
import random


class Markov:

    def __init__(self):
        self.cache = dict()

    def add_words(self, words):
        for i, word in enumerate(words):
            try:
                first, second, third = words[i], words[i + 1], words[i + 2]
            except IndexError:
                break
            key = (first, second)
            if key not in self.cache:
                self.cache[key] = []
            self.cache[key].append(third)

    def generate_sentence(self):
        key = random.choice([key for key in self.cache.keys()])

        sentence = list()
        first, second = key
        sentence.extend(key)

        while key in self.cache:
            third = random.choice(self.cache[key])
            sentence.append(third)
            key = (second, third)
            second = third

        return ' '.join(sentence)


def main():
    m = Markov()

    while True:
        words = input('>').split()
        m.add_words(words)
        print(m.generate_sentence())

if __name__ == '__main__':
    main()

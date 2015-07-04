#!/usr/bin/env python3

import markov
import pickle
import sys


class Feeder(markov.Markov):

    def __init__(self):
        self.cache = dict()


def main():
    if len(sys.argv) != 3:
        sys.exit('usage: python3 %s <in> <out>' % sys.argv[0])

    mc = Feeder()

    with open(sys.argv[1], 'r') as log:
        for line in log:
            mc.add_words(line.split())

    with open(sys.argv[2], 'wb') as db:
        pickle.dump(mc.cache, db)

if __name__ == '__main__':
    main()

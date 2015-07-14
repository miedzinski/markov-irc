#!/usr/bin/env python3

import configparser
import markov
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit(
            'usage: python3 {} <config-file> <log-file>'.format(sys.argv[0]))

    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    mc = markov.Markov(config['redis'])

    with open(sys.argv[2], 'r') as log:
        for line in log:
            mc.add_words(line.split())

if __name__ == '__main__':
    main()

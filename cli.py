import configparser
import markov
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python3 {} <config-file>'.format(sys.argv[0]))

    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    mc = markov.Markov(config['redis'])

    while True:
        inp = input('>> ').split()
        mc.add_words(inp)
        print(mc.generate_relevant_sentence(inp))

if __name__ == '__main__':
    main()

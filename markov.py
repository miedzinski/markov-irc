#!/usr/bin/env python3

import irc.bot
import pickle
import random
import time

DB_PATH = 'db'
HOST = 'irc.freenode.net'
PORT = 6667
NICK = ''
REALNAME = ''
CHANNEL = '#'
CHATTINES = 0.05  # chance of bot talking, 0 - 1.00
DELAY = 299  # frequency of how often bot has a chance to randomly speak


class Markov:

    def __init__(self):
        with open(DB_PATH, 'rb') as f:
            self.cache = pickle.load(f)

    def add_words(self, words):
        words.append('\n')
        for i, word in enumerate(words):
            try:
                first, second, third = words[i], words[i + 1], words[i + 2]
            except IndexError:
                break
            key = (first, second)
            if key not in self.cache:
                self.cache[key] = []
            self.cache[key].append(third)

    def dump_db(self):
        with open(DB_PATH, 'wb') as f:
            pickle.dump(self.cache, f)

    def generate_sentence(self):
        key = random.choice([key for key in self.cache.keys()
                             if '\n' not in key])

        sentence = list()
        first, second = key
        sentence.extend(key)

        while key in self.cache:
            third = random.choice(self.cache[key])
            key = (second, third)
            second = third
            if third != '\n':
                sentence.append(third)

        return ' '.join(sentence)


class MarkovBot(irc.bot.SingleServerIRCBot):

    def __init__(self, markov):
        irc.client.ServerConnection.buffer_class.errors = 'replace'
        irc.bot.SingleServerIRCBot.__init__(self,
                                            [(HOST, PORT)],
                                            NICK,
                                            REALNAME)
        self.markov = markov
        self.connection.execute_every(DELAY, self.say)

    def on_welcome(self, c, e):
        c.join(CHANNEL)

    def on_kick(self, c, e):
        time.sleep(3)
        c.join(e.target)

    def on_pubmsg(self, c, e):
        self.markov.add_words(e.arguments[0].split())
        self.markov.dump_db()
        if c.nickname in e.arguments[0]:
            c.privmsg(e.target, self.markov.generate_sentence())

    def say(self):
        if self.connection.connected and random.random() <= CHATTINES:
            self.connection.privmsg(CHANNEL, self.markov.generate_sentence())


def main():
    mc = Markov()
    bot = MarkovBot(mc)
    bot.start()

if __name__ == '__main__':
    main()

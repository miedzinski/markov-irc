#!/usr/bin/env python3

import configparser
import irc.bot
import random
import redis
import sys
import time


class Markov:

    def __init__(self, config):
        self.client = redis.StrictRedis(host=config['host'],
                                        port=config['port'],
                                        db=config['db'],
                                        password=config['password'])

    def add_words(self, words):
        words.append('\n')
        for i, word in enumerate(words):
            try:
                key, completion = (words[i], words[i + 1]), words[i + 2]
            except IndexError:
                break
            key = ' '.join(key)
            self.client.zincrby(key, completion)

    def generate_sentence(self):
        key = self.client.randomkey().decode()
        sentence = [key]

        while self.client.exists(key):
            zset = self.client.zrevrange(key, 0, -1, withscores=True)
            completions = [[c[0].decode()] * int(c[1]) for c in zset]
            # let's flatten our list
            completions = [item for sublist in completions for item in sublist]
            completion = random.choice(completions)
            if completion != '\n':
                sentence.append(completion)
            key = '{} {}'.format(key.split()[1], completion)

        return ' '.join(sentence)


class MarkovBot(irc.bot.SingleServerIRCBot):

    def __init__(self, markov, config):
        irc.client.ServerConnection.buffer_class.errors = 'replace'
        irc.bot.SingleServerIRCBot.__init__(self,
                                            [(config['host'],
                                              int(config['port']))],
                                            config['nick'],
                                            config['realname'])
        self.markov = markov
        self.channel = config['channel']
        self.chattines = float(config['chattines'])
        self.blacklist = config['blacklist'].split(',')

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_kick(self, c, e):
        time.sleep(3)
        c.join(e.target)

    def on_pubmsg(self, c, e):
        if e.source.nick not in self.blacklist:
            self.markov.add_words(e.arguments[0].split())
        if c.nickname in e.arguments[0]:
            c.privmsg(e.target, self.markov.generate_sentence())

    def say(self):
        connection = self.connection
        if connection.connected and random.random() <= self.chattines:
            connection.privmsg(self.channel, self.markov.generate_sentence())


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python3 {} <config-file>'.format(sys.argv[0]))
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    mc = Markov(config['redis'])
    bot = MarkovBot(mc, config['irc'])
    bot.start()

if __name__ == '__main__':
    main()

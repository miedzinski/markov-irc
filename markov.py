#!/usr/bin/env python3

import random
import redis


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

    def _generate_sentence(self, start):
        key = start
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

    def generate_random_sentence(self):
        try:
            key = self.client.randomkey().decode()
            return self._generate_sentence(key)
        except AttributeError:
            return ''

    def generate_relevant_sentence(self, words):
        client = self.client
        random.shuffle(words)

        keys = []

        for word in words:
            keys += [key.decode() for key in client.keys('{} *'.format(word))]
            keys += [key.decode() for key in client.keys('* {}'.format(word))]

            if keys:
                break
        else:
            try:
                keys.append(client.randomkey().decode())
            except AttributeError:
                return ''

        return self._generate_sentence(random.choice(keys))

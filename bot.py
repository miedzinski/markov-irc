import configparser
import irc.bot
import markov
import time
import random
import sys


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
        self.hilight = config.getboolean('hilight')

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_kick(self, c, e):
        time.sleep(3)
        c.join(e.target)

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]

        if e.source.nick not in self.blacklist:
            hilighted = msg.startswith(c.nickname)
            if not hilighted or (hilighted and not self.hilight):
                self.markov.add_words(msg.split())

        if c.nickname in msg:
            words = msg.split()
            if words[0].startswith(c.nickname):
                del words[0]
            c.privmsg(e.target, self.markov.generate_relevant_sentence(words))
        elif random.random() <= self.chattines:
            c.privmsg(e.target, self.markov.generate_relevant_sentence(words))


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python3 {} <config-file>'.format(sys.argv[0]))

    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    mc = markov.Markov(config['redis'])
    bot = MarkovBot(mc, config['irc'])
    bot.start()

if __name__ == '__main__':
    main()

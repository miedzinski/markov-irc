# markov-irc #

IRC bot with text generation based on Markov property. A Redis database is used to store words.


## Installation ##

Requires Python 3 and Redis server.

	$ pyvenv venv
	$ source venv/bin/activate
	$ git clone https://github.com/miedzinski/markov-irc.git
	$ cd markov-irc
	$ pip install requirements.txt

Edit config.ini.


## Usage ##

For irc:

	$ python3 bot.py <config-file>

For cli:

	$ python3 cli.py <config-file>

## Provided tools ##

markov-irc comes with learning script. It works on sentences separated by new line feeds.

Usage:

	$ python3 feed.py <config-file> <log-file>

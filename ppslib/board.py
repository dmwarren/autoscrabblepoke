
'''
 auto-scrabblepoke - board.py
 Return useful pixiepit.co.uk Scrabble board and player data.

 Scrabble is a registered trademark of J. W. Spear & Son PLC and Hasbro Inc.
 This project is for personal use and is not affiliated with any trademark holders.
'''

from bs4 import BeautifulSoup
import re
import requests
import time
from . import conf, log

def get_players_dict(in_str=None):
    ''' IN: e.g., http://server/p2/r25/crossword.pl?board=playername1_and_name2
        OUT: {1: {'name': 'playername1'},
              2: {'name': 'name2'}}
    '''
    players = {}
    pnames = re.sub('^.*board=', '', in_str)
    p1name = re.sub('_and_.*$', '', pnames)
    p2name = re.sub('^.*_and_', '', pnames)
    players[1] = {'name': p1name}
    players[2] = {'name': p2name}
    log.m.debug('Found player1:{0}, player2:{1}'.format(p1name, p2name))
    return players


def next_player_name(in_soup):
    # Screen-scrape and return the name of the next player.
    waiting_for = ''

    for chunk in in_soup.get_text().split("\n"):
        if re.match('Waiting for.*', chunk):
            waiting_for = chunk

    if len(waiting_for) < 10:
        log.m.critical("ERROR: Can't find player names. Dying.")
        exit(1)

    next_player = re.sub('Waiting for ', '', waiting_for)
    next_player = re.sub(' to play.*', '', next_player)
    #next_player = next_player.encode('ascii', 'xmlcharrefreplace')
    next_player = str(next_player)
    #log.m.debug('next_player: ' + next_player)
    return next_player


def get_player_num(players_dict=None, next_player_name=None):
    for player_num, player_d in players_dict.items():
        if player_d['name'] == next_player_name:
            log.m.debug('next_player: {0}/{1}'.format(player_num,
                                                      next_player_name))
            return player_num
    return


def get_board_soup(game_url=None):
    # Return soupified board HTML
    start_time = time.time()
    req = requests.get(conf.c['game_url'])
    elapsed_time = time.time() - start_time

    log_msg = 'get_board_html: HTTP {0}, {1} bytes, {2:1.2f} seconds'.format(
        req.status_code,
        len(req.text),
        elapsed_time)
    log.m.debug(log_msg)

    if req.status_code != 200:
        log.m.critical('ERROR: HTTP {0} fetching board'.format(req.status_code))
        exit(1)
    soup = BeautifulSoup(req.text, 'lxml', from_encoding='ISO-8859-1')
    return soup

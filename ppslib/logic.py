
'''
 auto-scrabblepoke - logic.py

 Scrabble is a registered trademark of J. W. Spear & Son PLC and Hasbro Inc.
 This project is for personal use and is not affiliated with any trademark holders.
'''
import argparse
from pprint import pprint
import random
from . import board, conf, log


def do_it():
    args = get_cli_args()
    pprint(args)

    # roll here to avoid unnecessary HTTP get
    if args['force'] is not True:
        random_factor = roll_dice()  # returns true or exits

    if len(conf.c['game_url']) < 7:  # http:// == 7 chars
        raise Exception('ERROR: game_url empty. Please populate scrabbug.conf.')
    players_dict = board.get_players_dict(conf.c['game_url'])
    board_soup = board.get_board_soup(conf.c['game_url'])
    next_player_name = board.next_player_name(board_soup)  # 1 or 2?

    # a little roundabout, but safer to latch onto a long string than just "p1/2"
    next_player_num = board.get_player_num(players_dict, next_player_name)
    next_player_email = get_player_email(next_player_num)
    next_player_url = get_player_url(next_player_num)

    dispatch_alert(next_player_email, next_player_url)
    return


def roll_dice():
    rand = random.random()
    rand = round(rand, 2)
    pct_chance = float(conf.c['percentage_chance'])
    log.m.info('dice: {0:1.2f}/{1:1.2f}'.format(rand, pct_chance))
    if rand > pct_chance:
        log.m.info('dice: proceeding')
        return True
    else:
        log.m.info('dice: exiting')
        exit(0)


def get_player_email(next_player_num=None):
    if next_player_num == 1:
        return conf.c['player1_email']
    else:
        return conf.c['player2_email']


def get_player_url(next_player_num=None):
    out_str = '{0}&pass={1}'
    if next_player_num == 1:
        return out_str.format(conf.c['game_url'],
                              conf.c['player1_pass'])
    else:
        return out_str.format(conf.c['game_url'],
                              conf.c['player2_pass'])


def dispatch_alert(to_addr=None, url=None):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib, mimetypes, email, email.mime.application
    import time
    naglist = (to_addr,)

    html = conf.c['mail_tmpl']
    html = html.format(url)
    part_html = email.mime.text.MIMEText(html, 'html')

    # Create a text/plain message
    msg = MIMEMultipart()
    msg['Subject'] = conf.c['mail_subject']
    msg['From'] = conf.c['mail_from']
    msg['To'] = to_addr

    # mail body is just another attachment
    msg.attach(part_html)

    # let's DO THIS THING
    start_time = time.time()
    server = smtplib.SMTP(conf.c['smtp_server'], port=conf.c['smtp_port'])
    server.starttls()
    server.login(conf.c['smtp_username'], conf.c['smtp_password'])
    server.sendmail(msg['From'],msg['to'],msg.as_string())
    server.quit()
    elapsed_time = time.time() - start_time
    log_msg = 'dispatch_alert: sent mail in {0:1.2f} seconds'.format(elapsed_time)
    log.m.debug(log_msg)
    return


def get_cli_args():
    p = argparse.ArgumentParser(
        prog='autoscrabblepoke',
        description='Automatic Pixie Pit Scrabblepoker, v0.4')
    p.add_argument('-V', '--version',
                   action='version',
                   version='autoscrabblepoke 0.4, 05-Oct-2017')
    p.add_argument('-f', '--force',
                   dest='force',
                   action='store_true',
                   help='send e-mail regardless of dice roll')
    return vars(p.parse_args())

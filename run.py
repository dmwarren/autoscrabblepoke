#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  autoscrabblepoke
  Automatically send e-mail reminders to whoever's holding up your Scrabble game at thepixiepit.co.uk.

  v0.4 - 05-Oct-2017 - first public release

  Scrabble is a registered trademark of J. W. Spear & Son PLC and Hasbro Inc.
  This project is for personal use and is not affiliated with any trademark holders.
'''

from ppslib import log, logic

def main(args=None):
    log.m.debug('START')
    logic.do_it()
    log.m.debug('FINISH')
    return

if __name__ == "__main__":
    main()

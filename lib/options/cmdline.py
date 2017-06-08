#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

def cmdLineParser():
    parser = argparse.ArgumentParser(description='',
                                     usage='python star.py -api bing -query "inurl:php?id=1" -thread 20\n       save txt in output/ floder, name is date.',
                                     add_help=False)

    parser.add_argument('-api', dest="api", default="baidu", choices=['baidu', 'bing', 'google'],
                        help='search api interface,default baidu.')

    parser.add_argument('-query', dest="query", default=False,
                        help='search keywords and support search method.')

    parser.add_argument('-thread', dest="threadNum", type=int, default=10,
                        help='num of threads/concurrent, 10 by default..')
    
    parser.add_argument('--max-page', dest="pages", type=int, default=5,
                        help='all result pages,5 by default.')

    parser.add_argument('-infile', dest="inFile", default=False,
                        help='read all urls in Txt.')

    parser.add_argument('--show', default=False, action='store_true',
                        help='show ten lastest results.')

    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit.')
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args

#tmp = cmdLineParser()
#print tmp.show
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as ServerHttpDenied
from lib.httplib2 import Http, ProxyInfo
from socket import error as SocketError
from lib.tool import getConfig, filterU

def _initHttpClient():
    GOOGLE_PROXY = getConfig('google', 'proxy')
    if GOOGLE_PROXY:
        proxy_str = GOOGLE_PROXY
    else:
        proxy_str = None

    if not proxy_str:
        return Http()

    proxy = proxy_str.strip().split(' ')
    if len(proxy) != 3:
        msg = 'SyntaxError in GoogleProxy string, Please check your args or config file.'
        sys.exit(msg)
    if proxy[0].lower() == 'http':
        type = 3
    elif proxy[0].lower() == 'sock5':
        type = 2
    elif proxy[0].lower() == 'sock4':
        type = 1
    else:
        msg = 'Invalid proxy-type in GoogleProxy string, Please check your args or config file.'
        sys.exit(msg)
    try:
        port = int(proxy[2])
    except ValueError:
        msg = 'Invalid port in GoogleProxy string, Please check your args or config file.'
        sys.exit(msg)
    else:
        http_client = Http(proxy_info=ProxyInfo(type, proxy[1], port))
    return http_client


def GoogleSearch(query, limit):
    key = getConfig('google', 'apikey')
    engine = getConfig('google', 'search_engine')
    if not key or not engine:
        sys.exit()
    try:
        service = build("customsearch", "v1", http=_initHttpClient(), developerKey=key)

        result_info = service.cse().list(q=query, cx=engine).execute()
        #msg = 'Max query results: %s' % str(result_info['searchInformation']['totalResults'])
        #print msg
        ans = []
        for i in range(0, limit):
            result = service.cse().list(q=query, cx=engine, num=10, start=i * 10 + 1).execute()
            if 'items' in result:
                for url in result['items']:
                    if filterU(url['link']):
                        ans.append(url['link'])
        return ans
    except SocketError:
        sys.exit('Unable to connect Google, maybe agent/proxy error.')
    except ServerHttpDenied, e:
        pass

#coding:utf-8

'''
从搜索引擎获取结果,这里只是引擎搜到的结果
'''

from lib.api.bing import bing
from lib.api.baidu import baidu
from lib.api.google import GoogleSearch

def getEngineResult(api, query, pages):
	if api == 'bing':
		bingResult = bing(query, pages)
		return bingResult
	if api == 'baidu':
		baiduResult = baidu(query, pages)
		return baiduResult
	if api == 'google':
		googleResult = GoogleSearch(query, pages)
		return googleResult
		
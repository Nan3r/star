#coding:utf-8
import requests
from bs4 import BeautifulSoup
from lib.tool import getHtml
from lib.tool import filterU,getRdirect

def getResultUrl(html):
	soup = BeautifulSoup(html, 'lxml')
	aSign = soup.find_all('a', {'class':'c-showurl'})
	result = []
	for url in aSign:
		rUrl = getRdirect(url['href'])
		if rUrl and filterU(rUrl):
			result.append(filterU(rUrl))
	return result

def baidu(query, pages):
	result = []
	for page in range(1, pages):
		html = getHtml('http://www.baidu.com/s?cl=3&rn=10&ie=utf-8&wd='+query + '&pn='+str(10*(page-1))) #利用query的语句显示前page页的结果数据
		if html:
			url = getResultUrl(html)
			for rurl in url:
				result.append(rurl)
	return result

if __name__ == '__main__':
	query = 'site:cuit.edu.cn php'
	url = 'http://www.baidu.com/s?cl=3&rn=10&ie=utf-8&wd='+query#&pn=30
	html = getResultUrl(getHtml(url))
	print html
	
#coding:utf-8
#url:http://cn.bing.com/search?q=
import requests
from bs4 import BeautifulSoup
from lib.tool import getHtml
from lib.tool import filterU


def delHtml(url):
	if url.find('strong') != -1:
		return url.replace('<strong>', '').replace('</strong>', '')
	return url

def fromHtmlGetUrl(html):
	soup = BeautifulSoup(html,'lxml')
	cite = soup.find_all('cite')
	result = []
	tmp = ''
	for url in cite:
		#print type(url.contents)
		for i in url.contents:
			tmp += delHtml(str(i))

		filterUrl = filterU(tmp)
		if filterUrl:
			result.append(filterUrl)
		tmp = ''
	return result

def bing(query, pages):
	result = []
	for page in range(1, pages):
		html = getHtml('http://cn.bing.com/search?q='+query + '&first='+str(10*(page-1))) #利用query的语句显示前page页的结果数据
		if html:
			url = fromHtmlGetUrl(html)
			for rurl in url:
				result.append(rurl)
	return result

if __name__ == '__main__':
	query = 'site:cuit.edu.cn php'
	#query = '职业技术学院'
	bingResult = bing(query, 5)
	print bingResult
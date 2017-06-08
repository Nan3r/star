#-*-coding:utf-8-*-

from lib.tool import getHtml
from lib.tool import get
'''
对URL去重，相似度高的,大厂商的URL,然后再对URL访问，对其有效性判读
得到GET型的URL，这里只比较相邻的URL
标准:
1.http://nan3r.me:8081/cdsa/cda/aaa.jsp 与这个一模一样的
2.参数相同，数值不同的也要去除
'''
def uniqueUrl(urlList):
	urlList = list(set(urlList))#使用set方法先去一遍重
	result = whileU(urlList)
	domainTmp = []
	dicTmp = {}
	returnRes = []
	while 1:
		lenhead = len(result)
		result = whileU(result)
		lenhou = len(result)
		if lenhead == lenhou:
			break
	for i in result:
		domainTmp.append(get(i)['domain'])
	domainTmp = list(set(domainTmp))
	for k in domainTmp:
		dicTmp[k] = 0
	for y in result:
		tmp = get(y)['domain']
		if dicTmp[tmp] < 5:
			returnRes.append(y)
			dicTmp[tmp] += 1
	return returnRes

'''
循环去重
'''
def whileU(urlList):
	result = []
	tmp = []
	for i, value in enumerate(urlList):
		if i + 1 == len(urlList):
			break
		tmp = betweenUrl(urlList[i], urlList[i + 1])
		if not tmp:
			continue
		if len(tmp) == 2:
			result.extend(tmp)
		if len(tmp) == 1:
			result.append(tmp[0])
	return list(set(result))

'''
对相邻两个URL去重
'''
def betweenUrl(aUrl, bUrl):
	a_Url = get(aUrl)['url']
	b_Url = get(bUrl)['url']
	aparams = get(aUrl)['params'].split('&')
	bparams = get(bUrl)['params'].split('&')
	if a_Url != b_Url or len(aparams) != len(bparams):
		return [aUrl, bUrl]
	akey = []
	for x in aparams:
		akey.append(x.split('=')[0])
	bkey = []
	for x in bparams:
		bkey.append(x.split('=')[0])
	if cmp(akey, bkey) == 0:
		return [aUrl]
	if cmp(akey, bkey) == -1:
		return [aUrl, bUrl]
	return False
'''
对单个网页进行爬(GET类型)
对href标签里面的进行获取
'''
def getGetUrl(url):
	from bs4 import BeautifulSoup
	if url.find('http://') == -1 and url.find('https://') == -1:
		url = 'http://'+url
	resultUrl = [url]
	scheme = get(url)['scheme']
	domain = get(url)['domain']
	html = getHtml(url)
	if html:
		soup = BeautifulSoup(html, 'lxml')
		for link in soup.find_all('a', href=True):
			href= link['href']
			if is_get(href):
				hrefScheme = get(href)['scheme']
				if hrefScheme == '':
					href = 'http://'+href
				hrefDomain = get(href)['domain']
				if hrefDomain == '' and domain != '':
					href = scheme + '://' + domain + href[7:]
					resultUrl.append(href)
	return resultUrl


'''
是否是sqlmap可识别的get型链接
'''
def is_get(url):
	import re 
	regex = r'(\S*?)\?.*=.*'
	res = re.match(regex,url)
	if res:
		return res.group(1)
	else:
		return 0

'''
获取到爬虫的结果,并且去重,没有使用多线程
'''
def getAllUrls(urlList):
	import time
	startTime = time.time()
	allUrl = []
	for i,url in enumerate(urlList):
		spiderUrl = getGetUrl(url)
		for tmpUrl in uniqueUrl(spiderUrl):
			allUrl.append(tmpUrl)
		if time.time() - startTime > 5:
			print 'Finish {:.2f}%'.format(100*i/float(len(urlList)))
	return allUrl
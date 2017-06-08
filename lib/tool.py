#coding:utf-8

'''
获取配置里面的参数
'''

def getConfig(config, name):
	import ConfigParser
	conf = ConfigParser.ConfigParser()
	conf.read('./star.conf')
	return conf.get(config, name)

'''
检查配置文件
'''
def checkConf(api):
	isSetSqlmapapi = getConfig('config', 'sqlapi')
	if not isSetSqlmapapi:
		exit('[**]Set Sqlmapapi Address In Star.conf')

	if api == 'google':
		proxy = getConfig('google', 'proxy')
		apikey = getConfig('google', 'apikey')
		search_engine = getConfig('google', 'search_engine')
		if not proxy:
			exit('[**]Must Set Proxy In Star.conf')
		elif not apikey:
			exit('[**]Must Set apikey In Star.conf')
		elif not apikey:
			exit('[**]Must Set search_engine In Star.conf')

'''
屏蔽含有这些关键字的URL
'''
def filterU(url):
	filterKeyWd = filterKey()
	for kw in filterKeyWd:
		if url.find(kw) != -1:
			return False
	return url

def filterKey():
	import ConfigParser
	conf = ConfigParser.ConfigParser()
	conf.read('star.conf')
	key = conf.get('filterkey', 'key')
	return key.split(', ')

'''
读取文件
'''
def readFile(txtName):
	urls = []
	with open(txtName, 'r') as f:
		urls = f.readlines()
	return urls

'''
随机UA
'''
def randomUA():
	import random
	headers = [
	'Mozilla/5.0 (Windows NT 5.1; U; pl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00',
	'Mozilla/5.0 (Windows NT 5.1; U; ru) Opera 8.51',
	'Mozilla/5.0 (Windows NT 5.1; U; zh-cn; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
	'Mozilla/5.0 (Windows NT 5.1; U; zh-cn; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53',
	'Mozilla/5.0 (Windows NT 5.1; U; zh-cn; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.70',
	'Mozilla/5.0 (Windows NT 5.2; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0 Opera 9.27',
	'Mozilla/5.0 (Windows NT 5.2; U; ru; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.70',
	'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
	'Mozilla/5.0 (Windows NT 6.0; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.51',
	'Mozilla/5.0 (Windows NT 6.0; U; ja; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00',
	'Mozilla/5.0 (Windows NT 6.0; U; tr; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 10.10',
	'Mozilla/5.0 (Windows NT 6.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01',
	'Mozilla/5.0 (Windows NT 6.1; U; en-GB; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.51',
	'Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9b3) Gecko/2008020514 Opera 9.5'
	]
	return headers[random.randint(0, len(headers)-3)]
'''
获取网页内容
'''
def getHtml(url):
	import requests
	requests.packages.urllib3.disable_warnings()
	headers = {
		'User-Agent':randomUA()
	}
	try:
		html = requests.get(url, headers=headers, timeout=5, verify=False)
		#html.encoding = 'utf-8'
		return html.text
	except Exception as e:
		return False

'''
判断是否可以访问
'''
def is_200(url):
	import requests
	code = requests.get(url, allow_redirects = False).status_code
	if code == 200:
		return True
	return False

'''
获取到跳转后的网址,搜索引擎跳转
'''
def getRdirect(url):
	import requests
	try:
		html = requests.head(url)
		return html.headers['Location']
	except Exception as e:
		return False

'''
对于get类型url进行分解
return: [url, params]
'''
def get(url):
	import urlparse
	parseResult = urlparse.urlparse(url)
	url = parseResult.scheme + '://' + parseResult.netloc + parseResult.path
	params = parseResult.query
	return { 
			'url' : url, 
			'domain' : parseResult.netloc,
			'scheme' : parseResult.scheme,
			'params' : params
		}

'''
随机返回一个UA
'''
def getRandomUA():
	import random
	UA = [
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6) AppleWebKit/531.4 (KHTML, like Gecko) Version/4.0.3 Safari/531.4',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
			'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_2; en-au) AppleWebKit/525.8+ (KHTML, like Gecko) Version/3.1 Safari/525.6',
			'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_2; en-gb) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
			'mozilla/3.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/5.0.1',
			'Mozilla/4.0 (compatible; Intel Mac OS X 10.6; rv:2.0b8) Gecko/20100101 Firefox/4.0b8)',
			'Mozilla/4.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.2) Gecko/2010324480 Firefox/3.5.4',
			'Mozilla/4.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.7) Gecko/2008398325 Firefox/3.1.4',
			'Mozilla/5.0 (compatible; Windows; U; Windows NT 6.2; WOW64; en-US; rv:12.0) Gecko/20120403211507 Firefox/12.0',
			'Mozilla/5.0 (Linux i686; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0',
			'Mozilla/5.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'
	]
	return UA[random.randint(0, len(UA))]


if __name__ == '__main__':
	url = 'http://ss/archiver/cdsa/cda/aaa.jsp?id=2&cid=2&ridsssrct=asc#sss'
	print get(url)['url']
	print get(url)['domain']
	print get(url)['scheme']
	print get(url)['params']
	print getRandomUA()
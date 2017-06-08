#-*-coding:utf-8-*-
'''
主程序
'''
from lib.options import cmdline
from lib import engine
from lib import show
from lib import sqli
from lib import spider
from lib.tool import readFile
from lib.tool import checkConf
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
	'''
	log
	'''
	log = '''
------------------------------------------------------------------------------------
|      _  _  _  _         _  _  _  _  _              _              _  _  _  _     |
|    _(_)(_)(_)(_)_      (_)(_)(_)(_)(_)           _(_)_           (_)(_)(_)(_) _  |
|   (_)          (_)           (_)               _(_) (_)_         (_)         (_) |
|   (_)_  _  _  _              (_)             _(_)     (_)_       (_) _  _  _ (_) |
|     (_)(_)(_)(_)_            (_)            (_) _  _  _ (_)      (_)(_)(_)(_)    |
|    _           (_)           (_)            (_)(_)(_)(_)(_)      (_)   (_) _     |
|   (_)_  _  _  _(_)           (_)            (_)         (_)      (_)      (_) _  |
|     (_)(_)(_)(_)             (_)            (_)         (_)      (_)         (_) |
------------------------------------------------------------------------------------
			                   Powered By Nan3r <mail:nan3ryue@gmail.com>
	'''
	print log
	'''
	#获取参数
	#如果是显示结果，显示完就退出
	'''
	args = cmdline.cmdLineParser()
	if args.show:
		show.showResult()
		exit()

	'''
	检查配置文件
	'''
	checkConf(args.api)
	

	'''
	是否读取文件
	'''
	isReadTxt = args.inFile
	if not isReadTxt:
		'''
		#获取搜索引擎的结果
		'''
		print '[*]Getting Engine Results.........'
		engineResult = engine.getEngineResult(args.api, args.query, args.pages)
		print '[*]Get Done,Total is %s results' % len(engineResult)

		'''
		#对搜索到的页面进行爬取
		'''
		print '[*]Spidering Engine Results.........'
		sqlUrls = spider.getAllUrls(engineResult)
		print '[*]Spidering Done.........'
	else:
		sqlUrls = readFile(isReadTxt)

	'''
	#进行sql注入检测
	'''
	print '[*]Verify All Engine Results.........'
	sqli.sqlmapapi(sqlUrls, args.threadNum)
	print '[*]Verify Done Results.........'
#!/usr/bin/python
#-*-coding:utf-8-*-

import requests
import time
import json
import threading
import Queue
from lib.tool import getConfig
import logging

API_URL = getConfig('config', 'sqlapi')

LEVELS = {
			'debug': logging.DEBUG,
			'info': logging.INFO,
			'warning': logging.WARNING,
			'error': logging.ERROR,
			'critical': logging.CRITICAL
		}
LOG = {
"level" : LEVELS["debug"],
"filename" : "./log/sqli.log",
"format" : '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s',
"datefmt" : '%Y-%m-%d %H:%M:%S'
}


class sqlVerify(object):
	"""
	使用sqlmapapi的方法进行与sqlmapapi建立的server进行交互

	"""
	def __init__(self, server='', target='',save='', data = '',referer = '',cookie = ''):
		super(sqlVerify, self).__init__()
		self.server = server
		if self.server[-1] != '/':
			self.server = self.server + '/'
		self.target = target.strip()
		self.taskid = ''
		self.engineid = ''
		self.status = ''
		self.data = data
		self.saveName = save
		self.referer = referer
		self.cookie = cookie
		self.start_time = time.time()
		self.logger = logging.getLogger('app.run')
		self.logger.info('Creating an instance of sqlVerify for {0}.'.format(self.target))

	def task_new(self):
		try:
			self.taskid = json.loads(requests.get(self.server + 'task/new').text)['taskid']
			#print 'Created new task: ' + self.taskid
			if len(self.taskid) > 0:
				return True
			return False
		except Exception:
			self.logger.error("sqlmapapi.py is not running")

	def task_delete(self):
		json_kill = requests.get(self.server + 'task/' + self.taskid + '/delete', timeout=2).text
		# if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
		#	#print '[%s] Deleted task' % (self.taskid)
		#	return True
		#return False

	def scan_start(self):
		headers = {'Content-Type': 'application/json'}
		payload = {'url': self.target}
		url = self.server + 'scan/' + self.taskid + '/start'
		try:
			t = json.loads(requests.post(url, data=json.dumps(payload), headers=headers, timeout=2).text)
			self.engineid = t['engineid']
			if len(str(self.engineid)) > 0 and t['success']:
				self.logger.debug("Starting to scan "+ self.target)
				return True
		except Exception as e:
			return False

	def scan_status(self):
		self.status = json.loads(
			requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
		if self.status == 'running':
			return 'running'
		elif self.status == 'terminated':
			return 'terminated'
		else:
			return 'error'

	def scan_data(self):
		self.data = json.loads(
			requests.get(self.server + 'scan/' + self.taskid + '/data', timeout=2).text)['data']
		if len(self.data) == 0:
			#print 'not injection\t'
			pass
		else:
			f = open('./output/'+self.saveName,'a+')
			f.write(self.target+'\n')
			f.close()
			self.logger.warning('injection \t')

	def option_set(self):
		headers = {'Content-Type': 'application/json'}
		option = {"options": {
					"randomAgent": True,
					"dbms":"mysql",
					"tech": "BEUST"
					}
				 }
		url = self.server + 'option/' + self.taskid + '/set'
		t = json.loads(
			requests.post(url, data=json.dumps(option), headers=headers, timeout=2).text)
		#print t

	def scan_stop(self):
		json_stop=requests.get(self.server + 'scan/' + self.taskid + '/stop', timeout=2).text
		# json.loads(
		#     requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']

	def scan_kill(self):
		json_kill=requests.get(self.server + 'scan/' + self.taskid + '/kill', timeout=2).text
		# json.loads(
		#     requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']

	def run(self):
		if not self.task_new():
			return False
		self.option_set()
		if not self.scan_start():
			print 'Start Error!'
			return False
		while True:
			if self.scan_status() == 'running':
				time.sleep(10)
			elif self.scan_status() == 'terminated':
				break
			else:
				break
			#print time.time() - self.start_time
			if time.time() - self.start_time > 500:
				self.scan_stop()
				self.scan_kill()
				error = True
				break
		try:
			self.scan_data()
			self.task_delete()
		except Exception as e:
			pass
		#print time.time() - self.start_time

class myThread(threading.Thread):
	def __init__(self,q,thread_id):
		threading.Thread.__init__(self)
		self.q=q
		self.thread_id=thread_id
	def run(self):
		while not self.q.empty():
			#print "threading "+str(self.thread_id)+" is running"
			objects=self.q.get()
			result=objects.run()

def sqlmapapi(urls, threadNum):
	logger = logging.getLogger('app')
	logger.setLevel(LOG["level"])
	fh = logging.FileHandler(LOG["filename"])
	fh.setLevel(LOG["level"])
	formatter = logging.Formatter(LOG['format'], LOG["datefmt"])
	fh.setFormatter(formatter)
	sh = logging.StreamHandler()
	sh.setLevel(LOG["level"])
	sh.setFormatter(formatter)
	logger.addHandler(fh)
	logger.addHandler(sh)
	logger.info('the program starts!')

	#print urls
	saveName = str(time.strftime("%Y-%m-%d", time.localtime()))+'.txt'
	workQueue = Queue.Queue()
	for tar in urls:
		s = sqlVerify(API_URL, tar, saveName)
		workQueue.put(s)
	threads = []
	nloops = range(threadNum)   #threads Num
	for i in nloops:
		t = myThread(workQueue, i)
		#t.setDaemon(True)
		t.start()
		threads.append(t)
	for i in nloops:
		threads[i].join()
	logger.info("Exiting Main Thread")

if __name__ == '__main__':
	#main()
	#pass

	t = sqlVerify('http://127.0.0.1:8775', 'http://www.changan-mazda.com.cn/market/runningmen/article.php?id=191')
	t.run()
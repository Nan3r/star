#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
'''
按照文件修改时间的最新，读取最新的文件里面的url
'''

DIR = "./output/"
def showResult():
	result = []
	iterms = os.listdir(DIR)
	iterms.sort(compare)

	'''
	倒序读取文件
	'''
	for it in iterms[::-1]:
		for resurl in open(DIR+it, 'r'):
			result.append(resurl.strip())
			result = list(set(result))
			'''
			显示15条最新记录
			'''
			if len(result) > 15:
				break
		if len(result) > 15:
				break

	for i in result:
		print '[*] '+i.strip()

 
  
def compare(x, y):  
	stat_x = os.stat(DIR + "/" + x)  
	stat_y = os.stat(DIR + "/" + y)  
	if stat_x.st_ctime < stat_y.st_ctime:  
	    return -1  
	elif stat_x.st_ctime > stat_y.st_ctime:  
	    return 1  
	else:  
	    return 0
#!/usr/bin/env python
# encoding: utf-8

import requests,threading
import os,sys
from urllib import quote
from termcolor import colored

reload(sys)
sys.setdefaultencoding('utf-8')

class Dir_fuzz(threading.Thread):
	def __init__(self,fuzz_init_url,dir_fuzz_list):
		threading.Thread.__init__(self)
		self.fuzz_init_url = fuzz_init_url
		self.dir_fuzz_list = dir_fuzz_list

	def run(self):
		dir_fuzz_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	    'Accept':'text/html;q=0.9,*/*;q=0.8',
	    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	    'Accept-Encoding':'gzip',
	    'Connection':'close',
	    'Referer':self.fuzz_init_url}

		times_403 = 0
		times_302 = 0
		times_cant_connect = 0

		for i in self.dir_fuzz_list:
			i = i.strip('\r\n')
			testing_url = self.fuzz_init_url+quote(i)
			print "[-]Test:"+testing_url

			try:
				r = requests.get(testing_url,headers=dir_fuzz_header,timeout=20,verify=False)
			except Exception, e:
				print colored("[!]Can't Connect!",'yellow')
				times_cant_connect = times_cant_connect+1
			print r.status_code
			if r.status_code == 200:
				print colored("[+]200:"+testing_url,'green')
			if r.status_code == 403:
				print colored("[-]403:"+testing_url,'yellow')
				times_403 = times_403+1
			if r.status_code == 302:
				print colored("[-]302:"+testing_url,'yellow')
				times_302 = times_302+1

			if (times_302>30)or(times_403>30)or(times_cant_connect>25):
				print colored("[!]Stop_Fuzz",'red')
				break

if __name__ == '__main__':

	fd = open(os.getcwd()+'/dic/dir.txt','r')
	dir_fuzz_list = fd.readlines()
	fd.close()

	url = 'http://www.zhenkong.info'

	Thread_number = 5
	Threads = []
	
	for i in xrange(0,Thread_number):
		m = (len(dir_fuzz_list)/Thread_number)*i
		n = (len(dir_fuzz_list)/Thread_number)*(i+1)

		t = Dir_fuzz(url,dir_fuzz_list[m:n])
        Threads.append(t)
        t.start()
        t.join()
	print "[^]Job Done!"




from bs4 import BeautifulSoup
import requests
import re
import urllib2
import urllib
import subprocess
import os
import cookielib
import json
import shutil
import timeit

def getSoup(url, header):
	return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)),'html.parser')

def getQuery(desc):
	query = desc
	query= query.split()
	query='+'.join(query)
	return query

def makeZip(desc):
	start_time = timeit.default_timer()
	if not os.path.exists('static/images/scrape'):
		os.makedirs('static/images/scrape')

	query = getQuery(desc)
	imageUrls = []
	#queryUrl = "http://www.google.com/search?q=" + query + "&source=lnms&tbm=isch"
	#queryUrl = "https://www.google.com/search?as_st=y&tbm=isch&as_q=" + query + ""
	queryUrl = "https://www.google.com/search?as_st=y&tbm=isch&as_q=" + query + "&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=ift:jpg"
	header={
	'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	soup = getSoup(queryUrl, header)

	for i in soup.find_all("div",{"class":"rg_meta"}):
	    link = str(json.dumps(json.loads(i.text)["ou"]))[1:-1]
	    imageUrls.append(link)

	i = 0
	f = 0
	for url in imageUrls:
		try:
			urllib.urlretrieve(url, 'static/images/scrape/' + str(i) + '.jpg')
			i =  i + 1
		except:
			f = f + 1
		#os.system("wget -P static/images/scrape " + url)
		#process = subprocess.Popen("wget -P static/images/scrape " + url, shell=True, stdout=subprocess.PIPE)
		#process.wait()
		#print process.returncode

	print f
	shutil.make_archive(desc, 'zip', 'static/images/scrape')
	shutil.rmtree('static/images/scrape')
	elapsed = timeit.default_timer() - start_time
	print elapsed
	return str(desc + ".zip")
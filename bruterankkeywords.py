#!/usr/bin/python 
#for python version 3.7.3

#http://shafis.in

import urllib
import requests 
import re
import re
import os, sys
import operator
import json
import pprint

from collections import OrderedDict
from collections import Counter
from itertools import islice


os.system('cls')

banner_file = "bruterank.banner" 
#banner file
def banner():
    global banner_file
    open_banner = open(banner_file, "r")
    for line in open_banner:
        print (line.rstrip())
    open_banner.close()

def stripHTMLTags (html):
#Strip HTML tags from any string and transfrom special entities.
    text = html

#Apply rules in given order.
    rules = [
      { r'>\s+' : u'>'},                  # Remove spaces after a tag opens or closes.
      { r'\s+' : u' '},                   # Replace consecutive spaces.
      { r'\s*<br\s*/?>\s*' : u'\n'},      # Newline after a <br>.
      { r'</(div)\s*>\s*' : u'\n'},       # Newline after </p> and </div> and <h1/>.
      { r'</(p|h\d)\s*>\s*' : u'\n\n'},   # Newline after </p> and </div> and <h1/>.
      { r'<head>.*<\s*(/head|body)[^>]*>' : u'' },     # Remove <head> to </head>.
      { r'<a\s+href="([^"]+)"[^>]*>.*</a>' : r'\1' },  # Show links instead of texts.
      { r'[ \t]*<[^<]*?/?>' : u'' },            # Remove remaining tags.
      { r'^\s+' : u'' }                   # Remove spaces at the beginning.
    ]
 
    for rule in rules:
      for (k,v) in rule.items():
        try:
          regex = re.compile (k)
          text  = regex.sub (v, text)
        except:
          pass #Pass up whatever we don't find.
 
  #Replace special strings.
    special = {
      '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
      '&lt;'   : '<', '&gt;'  : '>'
    }
 
    for (k,v) in special.items():
      text = text.replace (k, v)
 
    return text


banner()
#Create an empty list for generation logic.
y_arr = []

try:
    print ('[*] Trying URLs in sites.scrape...')
    file_list = open('sites.scrape','r')
    sites = file_list.read().split(',')

except:
    print ('[X] execption 1')
    banner()
    sys.exit()

for site in sites:
    try:
        site = site.strip()
        print ("[*] Downloading Content For : ")
        print ("    -" + site)
        x_arr = []
        response = urllib.request.urlopen(site)
        response.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0')]
        xx = (response.read().decode('utf-8'))
        x = stripHTMLTags(xx)
	#Replace junk found in our response
        x = x.replace('\n',' ')
        x = x.replace(',',' ')
        x = x.replace('.',' ')
        x = x.replace('/',' ')
        x = re.sub('[^A-Za-z0-9]+', ' ', x)
        x_arr = x.split(' ')
        for y in x_arr:
            y = y.strip()
            if y and (len(y) > 4):
              if ((y[0] == '2') and (y[1] == 'F')) or ((y[0] == '2') and (y[1] == '3')) or ((y[0] == '3') and (y[1] == 'F')) or ((y[0] == '3') and (y[1] == 'D')):
                y = y[2:]
              y_arr.append(y)
    except Exception as e:
        print ("[X] Execption Error 2 ")
        print (" \t For URL : "+ site )
        print (" \t -- Reason : " + str(e))
        pass

#funtion to find Keyword list
KeywordList = dict(Counter(y_arr))
print ("[*] Processing KeywordList...")
sKeywordList = sorted(KeywordList.items(), key=operator.itemgetter(1), reverse=True)
with open('KeywordList.txt', 'w') as json_file:
  json.dump(sKeywordList, json_file, indent=4, sort_keys=True)
cwd = os.getcwd()
print ("[*] Keyword list Generation Complete.")
print ("[*] Output JSON file Location - ")
print ("    -"+ cwd +"\\KeywordList.txt")

print ("[*]")
print ("---------Top 30 keywords indentified -----('keyword', score)-----------------------")
print (" ")
l = sKeywordList[0:50]

if len(l) % 2 != 0:
    l.append(" ")

l1 = l[0:10]
l2 = l[10:20]
l3 = l[30:40]

for K1, K2, K3 in zip(l1,l2,l3):
  print ('%-30s %-30s %s ' % (K1, K2, K3))
print ("--------------------------------------------------------------------------- ------")
print ("[*]")
#function to add unique words -- Better leave it as it is - Shafi
print ("[*] Total number of words found    >> " + str(len(y_arr)))  
print ("[*] Total Count of unique words    >> " + str(len(sKeywordList)))
print ("[*] Exiting Application.")






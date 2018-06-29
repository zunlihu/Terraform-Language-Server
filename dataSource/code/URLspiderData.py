# -*- coding: utf-8 -*-

import re
import urllib
import os
import time
import urllib2
import Queue
import threading
import socket

count=1
mylist = []

def get_repo(page):
    try:
        #req = urllib2.Request(page, headers=hdr)
        html = urllib.urlopen(page)
        content = html.read()
        #print content
        res_h3 = r'<h3>(.*?)</h3>'
        m_h3 = re.findall(res_h3, content,re.S|re.M)
    
        for line in m_h3:
            res_href = r'href="(.*?)">'
            m_href = re.findall(res_href,line, re.S|re.M)
            repo = 'https://github.com' + m_href[0]
            get_tf(repo) 

    except:
        print 'Fail to  connect the url:%s\n', page

def get_tf(folders):
    global count
    global mylist
    content = urllib.urlopen(folders).read()
    res_content = r'<td class="content">(.*?)</td>'
    m_content = re.findall(res_content,content,re.S|re.M)
    res_href = r'href="(.*?)">'
    for files in m_content:
        m_file = re.findall(res_href,files,re.S|re.M)
        if(not '.' in m_file[0]):
            get_tf('https://github.com'+m_file[0])
        elif('.tf' in m_file[0]):
            tf = urllib.urlopen('https://github.com'+m_file[0])
            tf_content = tf.read()
            res_tf = r'<a id="raw-url"(.*?)Raw</a>'
            m_raw = re.findall(res_tf,tf_content,re.S|re.M)
            raw_tf = re.findall(res_href,m_raw[0],re.S|re.M)
            
            try:
                urllib.urlretrieve('https://github.com'+raw_tf[0],'./data_tf/'+str(count)+'.tf')
                urllib.urlretrieve('https://github.com'+raw_tf[0],'./data_txt/'+str(count)+'.txt')
                print 'Download the No.%s tf files successfully\n'
                count += 1
                mylist.append('https://github.com'+raw_tf[0])

            except:
                print 'Fail to download the tf file:%s\n', raw_tf[0] 

def main():
    global count
    global mylist
    
        
    for i in range(1,100):
        url = 'https://github.com/search?l=HCL&p=%s&q=terraform&type=Repositories.html'%str(i)
        print url
        get_repo(url)

    file = open('tf_url_list.txt', 'w')  
    for line in mylist:
        file.write(line+'\n')
    file.close()    

    print 'Done!' 


if __name__ == '__main__':
    main()

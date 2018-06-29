# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import datetime
import json
import math

count=33275
url_list = []


def get_results(url,headers):
    try:
        req =  Request(url,headers=headers)
        response = urlopen(req).read()
        results = json.loads(response.decode())
        return results
    except:
        return []

def download(url):
    global count
    global url_list
    try:
        urlretrieve(url,'./data_tf/'+str(count)+'.tf')
        urlretrieve(url,'./data_txt/'+str(count)+'.txt')
        print ('No.%s'%str(count))
        print ('Download successfully:%s\n'%(url))
        count += 1
        url_list.append(url)
        
    except:
        print ('Fail to download the tf file:%s\n'%(url))

def download_files(folder,headers):
    try:
        files = get_results(folder,headers)
        for file in files:
            if ".tf" in  file['name']:
                download(file['download_url'])
        #elif (not "." in file['name']) and isinstance(get_results(folder+'/'+file['path'],headers),list):# if is subfolder
        #    download_files(folder+'/'+file['path'],headers)
    except:
        print('Download Failed!')



def main():
    global count
    global url_list
    #headers = {'User-Agent': 'Mozilla/5.0',
    #           'Authorization': 'token 28682976173c0d134bfdf9fbce94aa3e1b2ead69',
    #           'Content-Type': 'application/json',
    #           'Accept': 'application/json'
    #}
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token bbe36b82051f5a893bf3095049651ac3998ecc1a',
               'Content-Type': 'application/json',
               'Accept': 'application/json'
    }

    '''
    with open('star2.json','rb') as f:
        results = json.load(f)

    for item in results['items']:
        name = item['name']
        owner = item['owner']['login']
        contents_url = 'https://api.github.com/repos/{owner}/{name}/contents'.format(owner=owner, name=name)
        contents = get_results(contents_url,headers)
        for file in contents:
            try:
                if ".tf" in  file['name']:
                    download(file['download_url'])
                elif isinstance(get_results(contents_url+'/'+file['path'],headers),list):# if is subfolder
                    subfolder = contents_url+'/'+file['path']
                    files = get_results(subfolder,headers)
                    for code in files:
                        if ".tf" in  code['name']:
                            download(code['download_url'])
            except:
                print('Cannot download!')
                
    '''
    #total_repos = 8591
    url = 'https://api.github.com/search/repositories?q=terraform+language:HCL+stars:0+size:15..46'
    repos = get_results(url,headers)
    total_repos = repos['total_count']
    print ('total_repos:%s'%total_repos)
    total_page = math.ceil(total_repos/100)
    print ('total page:%s'%str(total_page))
    for page in range(1,total_page+1):
        page_url = url+'&page=%s&per_page=100'%(str(page))
        results = get_results(page_url,headers)   
        try:  
            for item in results['items']:
                name = item['name']
                owner = item['owner']['login']
                contents_url = 'https://api.github.com/repos/{owner}/{name}/contents'.format(owner=owner, name=name)
                contents = get_results(contents_url,headers)
                for file in contents:
                    try:
                        if ".tf" in  file['name']:
                            print ('Page%s:'%str(page))
                            download(file['download_url'])
                        elif isinstance(get_results(contents_url+'/'+file['path'],headers),list):# if is subfolder
                            subfolder = contents_url+'/'+file['path']
                            files = get_results(subfolder,headers)
                            for code in files:
                                if ".tf" in  code['name']:
                                    print ('Page%s:'%str(page))
                                    download(code['download_url'])
                    except:
                        print('Cannot download!')              
        except:     
            print('Open Error!')

    print('Download Done!\n')  
    print('Start write url list into txt...\n')        
    try:
        fp = open('tf_url_list.txt', 'a')  
        for line in url_list:
            fp.write(line+'\n')
        fp.close()    
        print ('Write Done!')
    except:
        print('Write Error!')
        


if __name__ == '__main__':
    main()

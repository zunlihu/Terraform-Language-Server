# -*- coding: utf-8 -*-
import sys

from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import datetime
import json
import math
import argparse
import os
count=1
url_list = []

def get_results(url,headers):
    try:
        req =  Request(url,headers=headers)
        response = urlopen(req).read()
        results = json.loads(response.decode())
        return results
    except:
        return []

def download(url, save_path, fileExtension):
    global count
    global url_list
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        urlretrieve(url,save_path+str(count)+fileExtension)
        print ('No.%s'%str(count))
        print ('Download successfully:%s\n'%(url))
        count += 1
        url_list.append(url)
        
    except:
        print ('Fail to download the tf file:%s\n'%(url))

def download_files(folder,headers,save_path, fileExtension):
    try:
        files = get_results(folder,headers)
        for file in files:
            if fileExtension in  file['name']:
                download(file['download_url'],save_path, fileExtension)
        #elif (not "." in file['name']) and isinstance(get_results(folder+'/'+file['path'],headers),list):# if is subfolder
        #    download_files(folder+'/'+file['path'],headers)
    except:
        print('Download Failed!')

def GetReposByPage(save_path, url,headers, fileExtension):
    repos = get_results(url,headers)
    total_repos = repos['total_count']
    print ('total_repos:%s'%total_repos)
    total_page = math.ceil(total_repos/100)
    print ('total page:%s'%str(total_page))
    for page in range(1,total_page+1):
        page_url = url+'&page=%s&per_page=100'%(str(page))
        print(page_url)
        results = get_results(page_url,headers)   
        try:  
            for item in results['items']:
                name = item['name']
                owner = item['owner']['login']
                contents_url = 'https://api.github.com/repos/{owner}/{name}/contents'.format(owner=owner, name=name)
                contents = get_results(contents_url,headers)
                for file in contents:
                    try:
                        if fileExtension in  file['name']:
                            print ('Page%s:'%str(page))
                            download(file['download_url'],save_path, fileExtension)
                        elif isinstance(get_results(contents_url+'/'+file['path'],headers),list):# if is subfolder
                            subfolder = contents_url+'/'+file['path']
                            files = get_results(subfolder,headers)
                            for code in files:
                                if fileExtension in  code['name']:
                                    print ('Page%s:'%str(page))
                                    download(code['download_url'],save_path, fileExtension)
                    except:
                        print('Cannot download!')              
        except:     
            print('Open Error!')
    print('Download Done!\n')  

def GetAllReposByCreated(save_path, headers, fileExtension):
    ## Get Chunks by Created date 
    created_url = 'https://api.github.com/search/repositories?q=Terraform+language:HCL+created:'
    created=["<2016-01-01", "2016-01-01..2016-07-01","2016-07-02..2017-01-01","2017-01-02..2017-04-01","2017-04-02..2017-07-01","2017-07-02..2017-09-01","2017-09-02..2017-11-01","2017-11-02..2018-01-01"]
    for date in created:
        url = created_url + date
        GetReposByPage(save_path, url,headers, fileExtension)
    
    for month in range(1, 8):
        start_date = str(datetime.date.today().replace(month=month).replace(day=2))
        end_date = str(datetime.date.today().replace(month=month+1).replace(day=1))
        date = start_date + '..'+end_date
        url = created_url + date
        GetReposByPage(save_path,url,headers, fileExtension)
    today = str(datetime.date.today())
    start_date = str(datetime.date.today().replace(day=2))
    date = start_date + '..'+today
    url = created_url + date
    GetReposByPage(save_path,url,headers, fileExtension)
    
def main():
    global count
    global url_list
    ########################################## Argument #########################################
   
    token = ""
    save_path = './github/'
    run_opt = 1
    fileExtension = '.tf'
  
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, default=token, help='(Required) Authentication token generated by github account')
    parser.add_argument('--save_path', type=str, default=save_path, help='(Optional) Define the folder to save files. If not exist, create it.')
    parser.add_argument('--run_opt', type=int, default=run_opt, help="(Optional) 1 for getting all tf files, 2 for update tf files dataset")
    args = parser.parse_args()

    if args.token:
        token = args.token
    if args.save_path:
        save_path = args.save_path
    if args.run_opt:
        run_opt = args.run_opt

    ########################################## Main #########################################
    headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token %s'%token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'
    }
    if(run_opt == 1):
        GetAllReposByCreated(save_path,headers, fileExtension)
    elif (run_opt == 2):
        created_url = 'https://api.github.com/search/repositories?q=Terraform+language:HCL+created:'
        today = str(datetime.date.today())
        url = created_url + today
        GetReposByPage(save_path,url,headers, fileExtension)
    
    
    print('Start write url list into txt...\n')        
    try:
        fp = open(save_path + 'url_list.txt', 'a')  
        for line in url_list:
            fp.write(line+'\n')
        fp.close()    
        print ('Write Done!')
    except:
        print('Write Error!')
        
if __name__ == '__main__':
    main()

import os
import sys
import json
import numpy as np
import re
import urllib.request as Request
import logging


def getDescrip(provider):
    TerraformPath = 'https://www.terraform.io'
    url = TerraformPath+provider
    content = Request.urlopen(url).read().decode('utf-8')
    providerlist = {}
    datalist = {}
    resourcelist = {}

    if("google" in provider):  
        rgx_block = r'<a href="#">Google Cloud Platform Data Sources</a>(.*?)</div>'
        c_block = re.findall(rgx_block, content, re.S|re.M)
        groupName = "Google Cloud Platform Data Sources"
    elif("oraclepaas" in provider):
        rgx_block = r'<a href="#">PaaS Data Sources</a>(.*?)</div>'
        c_block = re.findall(rgx_block, content, re.S|re.M)
        groupName = "PaaS Data Sources"
    elif("ovh" in provider):
        rgx_block = r'<a href="#">VRack Resources</a>(.*?)</div>'
        c_block = re.findall(rgx_block, content, re.S|re.M)
        groupName = "VRack Resources"
    else:
        rgx_block = r'<a href="#">Data Sources</a>(.*?)</div>'
        c_block = re.findall(rgx_block, content, re.S|re.M)
        groupName = "Data Sources"
        if(c_block == []):
            rgx_block = r'<a href="#">Resources</a>(.*?)</div>'
            c_block = re.findall(rgx_block, content, re.S|re.M)
            groupName = "Resources"
  
    rgx_item = r'<li>(.*?)</li>'
    rgx_url = r'<a href="(.*?)">'
    rgx_name = r'>(.*?)</a>'
    block = c_block[0]
    c_item = re.findall(rgx_item, block, re.S|re.M)
     
    for item in c_item:
        itemList = {}
        item_href = re.findall(rgx_url, item, re.S|re.M)
        item_name = re.findall(rgx_name, item, re.S|re.M)[0]
        for href in item_href:
            if(("#" in href) and ("Resource" in item_name or "Data" in item_name)):
                groupName = item_name
                continue
            elif(".html" in href):
                item_url = href
            
        item_groupName = groupName
        
        print("Name:%s    groupName:%s"%(item_name, item_groupName))
        print("URL:%s"%(TerraformPath+item_url))
        itemList["name"] = item_name
        itemList["url"] =  TerraformPath+item_url
        itemList["groupName"] = item_groupName
        itemList["args"] = findItemDescip(TerraformPath+item_url,"args") 
        itemList["attrs"]  = findItemDescip(TerraformPath+item_url,"attrs")
        
        print("DONE!\n")

        if("Resource" in item_groupName):
            itemList["type"] = "resource"
            resourcelist[item_name] = itemList
        elif("Data" in item_groupName):
            itemList["type"] = "data"
            datalist[item_name] = itemList
        
    providerlist["data"] = datalist
    providerlist["resource"] = resourcelist
        
    return providerlist

def findGroup(url):
    if("archive" in url):
        return "Data Sources"
    
    content = Request.urlopen(url).read().decode('utf-8')
    
    rgx_group = r'<li class="active">(.*?)<ul class="nav nav-visible">'
    block = re.findall(rgx_group,content, re.S|re.M)
    rgx_href =  r'<a href="#">(.*?)</a>'
    group = re.findall(rgx_href, block[0],re.S|re.M)[0]

    return group

def findItemDescip(url, descrip):
    try:
       content = Request.urlopen(url).read().decode('utf-8')
    except:
        print("ERROR! NO %s reference!"%descrip)
        return []

    itemList = []
    if(descrip == "args"):
        rgx_descrip = r'Argument Reference(.*?)</ul>'
    elif(descrip == "attrs"):
        rgx_descrip = r'Attributes Reference(.*?)</ul>'
    
    try:
        c_descrip = re.findall(rgx_descrip, content, re.S|re.M)[0]
        rgx_item = r'<li>(.*?)</li>'
        c_item = re.findall(rgx_item, c_descrip, re.S|re.M)
        print("Find %s %s reference!"%(str(len(c_item)),descrip))
        rgx_name = r'<a name="(.*?)" />'
        rgx_description = r'</a>(.*?)(\.|<\p>'
        for item in c_item:
            item_dict = {}
            c_name = re.findall(rgx_name, item, re.S|re.M)
            item_dict["name"] = c_name[0]
            try:
                c_description = re.findall(rgx_description, item, re.S|re.M)
                item_dict["description"] = c_description[0]
            except:
                item_dict["description"] = ""

            item_dict["args"] = []
            itemList.append(item_dict)
    except:
        print("ERROR! NO %s reference!"%descrip)
    
    return itemList

def getNullDes(provider):
    TerraformPath = 'https://www.terraform.io'
    url = TerraformPath+provider
    content = Request.urlopen(url).read().decode('utf-8')
    providerlist = {}
    datalist = {}
    resourcelist = {}

    rgx_block = r'<ul class="nav nav-visible">(.*?)</ul>'
    c_block = re.findall(rgx_block, content, re.S|re.M)
    
    rgx_item = r'<li>(.*?)</li>'
    rgx_url = r'<a href="(.*?)">'
    rgx_name = r'>(.*?)</a>'
    for block in c_block:
        c_item = re.findall(rgx_item, block, re.S|re.M) 
        for item in c_item:
            itemList = {}
            item_url = re.findall(rgx_url, item, re.S|re.M)[0]
            
            item_groupName = re.findall(rgx_name, item, re.S|re.M)[0]
            rgx = r'null/(.*?)\.html'
            item_name = "null_" + re.findall(rgx, item_url)[0]
            
            print("Name:%s    groupName:%s"%(item_name, item_groupName))
            print("URL:%s"%(TerraformPath+item_url))
            itemList["name"] = item_name
            itemList["url"] =  TerraformPath+item_url
            itemList["groupName"] = item_groupName
            itemList["args"] = findItemDescip(TerraformPath+item_url,"args") 
            itemList["attrs"]  = findItemDescip(TerraformPath+item_url,"attrs")
            
            print("DONE!\n")

            if("Resource" in item_groupName):
                itemList["type"] = "resource"
                resourcelist[item_name] = itemList
            elif("Data" in item_groupName):
                itemList["type"] = "data"
                datalist[item_name] = itemList
            
    providerlist["data"] = datalist
    providerlist["resource"] = resourcelist
        
    return providerlist

def getHttpDes(provider):
    TerraformPath = 'https://www.terraform.io'
    providerlist = {}
    datalist = {}
    
    itemList = {}
    item_url ="/docs/providers/http/data_source.html"
    item_name = "http"
    item_groupName = "Data Source"
    print("Name:%s    groupName:%s"%(item_name, item_groupName))
    print("URL:%s"%(TerraformPath+item_url))
    itemList["name"] = item_name
    itemList["url"] =  TerraformPath+item_url
    itemList["groupName"] = item_groupName
    itemList["type"] = "data"
    itemList["args"] = findItemDescip(TerraformPath+item_url,"args") 
    itemList["attrs"]  = findItemDescip(TerraformPath+item_url,"attrs")
    print("DONE!\n")

    datalist[item_name] = itemList
    providerlist["data"] = datalist

    return providerlist
    
def getExternalDes(provider):
    TerraformPath = 'https://www.terraform.io'
    providerlist = {}
    datalist = {}
    
    itemList = {}
    item_url = "/docs/providers/external/data_source.html"
    item_name = "external"
    item_groupName = "Data Source"
    print("Name:%s    groupName:%s"%(item_name, item_groupName))
    print("URL:%s"%(TerraformPath+item_url))
    itemList["name"] = item_name
    itemList["url"] =  TerraformPath+item_url
    itemList["groupName"] = item_groupName
    itemList["type"] = "data"
    itemList["args"] = findItemDescip(TerraformPath+item_url,"args") 
    itemList["attrs"]  = findItemDescip(TerraformPath+item_url,"attrs")
    print("DONE!\n")

    datalist[item_name] = itemList
    providerlist["data"] = datalist

    return providerlist

def getArchiveDes(url):
    providerlist = {}
    datalist = {}
    
    itemList = {}
    item_url = "https://www.terraform.io/docs/providers/archive/index.html"
    item_name = "archive_file"
    item_groupName = "Data Sources"
    print("Name:%s    groupName:%s"%(item_name, item_groupName))
    print("URL:%s"%(item_url))
    itemList["name"] = item_name
    itemList["url"] = item_url
    itemList["groupName"] = item_groupName
    itemList["type"] = "data"
    itemList["args"] = findItemDescip(item_url,"args") 
    itemList["attrs"]  = findItemDescip(item_url,"attrs")
    print("DONE!\n")

    datalist[item_name] = itemList
    providerlist["data"] = datalist
    return providerlist

def geth4Des(provider):
    TerraformPath = 'https://www.terraform.io'
    url = TerraformPath+provider
    content = Request.urlopen(url).read().decode('utf-8')
    providerlist = {}
    datalist = {}
    resourcelist = {}    

    rgx_block = r'<h4>(.*?)</li>'
    c_block = re.findall(rgx_block, content, re.S|re.M)
    rgx_group = r'(.*?)</h4>'
    rgx_item = r'<li>(.*?)a>'
    rgx_url = r'<a href="(.*?)">'
    rgx_name = r'html">(.*?)</'
    
    for block in c_block:
        groupName = re.findall(rgx_group, block,re.S|re.M)[0]
        c_item = re.findall(rgx_item, block, re.S|re.M)
       
        for item in c_item:
            itemList = {}
            item_url = re.findall(rgx_url, item, re.S|re.M)[0]
            item_name = re.findall(rgx_name, item, re.S|re.M)[0]
            print("Name:%s    groupName:%s"%(item_name, groupName))
            print("URL:%s"%(TerraformPath+item_url))
            itemList["name"] = item_name
            itemList["url"] =  TerraformPath+item_url
            itemList["groupName"] = groupName
            itemList["args"] = findItemDescip(TerraformPath+item_url,"args") 
            itemList["attrs"]  = findItemDescip(TerraformPath+item_url,"attrs")
            print("DONE!\n")
            
            if("Resource" in groupName):
                itemList["type"] = "resource"
                resourcelist[item_name] = itemList
            elif("Data" in groupName):
                itemList["type"] = "data"
                datalist[item_name] = itemList

    providerlist["data"] = datalist
    providerlist["resource"] = resourcelist
    return providerlist
            

def main():
    
    url = 'https://www.terraform.io/docs/providers/'
    content = Request.urlopen(url).read().decode('utf-8')
    rgx_table = r'<table class="table">(.*?)</table>'
    c_table = re.findall(rgx_table, content, re.S|re.M)
    
    rgx_td = r'<td>(.*?)</td>'
    rgx_url = r'<a href="(.*?)">'
    rgx_name = r'/providers/(.*?)/'
    
    c_td = re.findall(rgx_td, c_table[0])
    for item in c_td:
        try:
            provider_url = re.findall(rgx_url, item)[0]
            provider_name = re.findall(rgx_name, provider_url)[0]
        except:
            print("Invalid Provider!")
        try:
            if(provider_name == "null"):
                dict2json = getNullDes(provider_url)
            elif(provider_name == "http"):
                dict2json = getHttpDes(provider_url)
            elif(provider_name == "external"):
                dict2json = getExternalDes(provider_url)
            elif((provider_name == "archive") | (provider_name =="terraform-enterprise")):
                dict2json = geth4Des(provider_url)
            else:
                dict2json = getDescrip(provider_url)
            filename = "terraform-provider-"+provider_name+".json"
            with open("./provider/"+filename, 'w') as f:
                json.dump(dict2json, f)
            f.close()
            print("Write %s json files DONE!\n"%provider_name)
        except:
            with open(provider_name+'.txt', 'w') as f:
                f.write("ERROR!!")
            f.close()
    #dict = getDescrip("/docs/providers/oneandone/index.html")
    '''
    provider_name = "archive"
    url = "/docs/providers/ovh/index.html"
    dict2json = getDescrip(url)
    '''

    

if __name__ == '__main__':
    main()




import os
import sys
import json
import numpy as np
import re
import urllib.request as Request
import logging

def getName(arrayList):
    data = arrayList.tolist()
    return list(data.keys())

def getDescrip(NameList,type):
    TerraformPath = 'https://www.terraform.io'
    dictList = {}
    for item in NameList:  
        itemList = {}
        itemList["name"] = item
        itemList["type"] = type
        print("Name:%s    Type:%s"%(item,type))
        url = findURL(item,type)
        if(url):
            url = TerraformPath+url
        groupName = findGroup(url)

        itemList["url"] = url
        itemList["groupName"] = groupName
        itemList["args"] = findItemDescip(url,"args") 
        itemList["attrs"]  = findItemDescip(url,"attrs")
        print("DONE!\n")
    
        dictList[item] = itemList
    return dictList

def findGroup(url):
    try:
        content = Request.urlopen(url).read().decode('utf-8')
    except:
        print("ERROR! groupName: NULL!")
        return ""
    
    try:
        rgx_group = r'<li class="active">(.*?)<ul class="nav nav-visible">'
        block = re.findall(rgx_group,content, re.S|re.M)
        rgx_href =  r'<a href="#">(.*?)</a>'
        group = re.findall(rgx_href, block[0],re.S|re.M)[0]
        
    except:
        rgx_group = r'<li class="active">(.*?)</li>'
        block = re.findall(rgx_group,content, re.S|re.M)
        if(block == []):
            if("data" in url):
                group = "Data Source"
            elif("resource" in url):
                group = "Resource"
            else:
                group = ""
        else:
            rgx_href =  r'>(.*?)</a>'
            group = re.findall(rgx_href, block[0],re.S|re.M)[0]

    print("groupName:%s"%group)
    return group

def findURL(name,type):
    # find provider page 
    if("_" in name):
        rgx_provider = r'(.*?)_'
        provider = re.findall(rgx_provider,name)[0]    
    else:
        provider = name
    try:
        provider_url = 'https://www.terraform.io/docs/providers/%s/index.html'%provider
        content = Request.urlopen(provider_url).read().decode('utf-8')
    except:
        print("ERROR! URL: NULL!")
        return ""

    pattern_item = '<a href="(.*?)">'+name+'</a>'
    rgx_item = re.compile(pattern_item)
    item_url = rgx_item.findall(content,re.S|re.M)
    
    if(item_url == []):
        pattern_item = '<a href="(.*?)">'+type
        rgx_item = re.compile(pattern_item,re.IGNORECASE)
        item_url = rgx_item.findall(content,re.S|re.M)
        if(item_url == ([] or ["#"])):
            try:
                filename = name.split("_",1)[1]
                pattern_item = '<a href="(.*?)">'+filename+'</a>'
                rgx_item = re.compile(pattern_item)
                item_url = rgx_item.findall(content,re.S|re.M)
            except:
                print("ERROR! URL: NULL!")
                return ""

    for url in item_url:
        if(type == "data" and ("/d/" in url or "data_source" in url)):
            print("URL:%s"%url)
            return url
        elif(type == "resource"and ("/r/" in url or "resource" in url)):
            print("URL:%s"%url)
            return url
        else:
            print("ERROR! URL: NULL!")
            return ""

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

def main():
    
    dict2json = {}
    resList = np.load('./data_count/res_nums.npy')
    dataList = np.load('./data_count/data_nums.npy')
    resName = getName(resList)
    dataName = getName(dataList)
    dict2json["data"] = getDescrip(dataName,"data")
    print ("Get data types description Done!")
    dict2json["resource"] = getDescrip(resName,"resource")
    print ("Get resource types description Done!")

    json_str = json.dumps(dict2json)
    fileObject = open('jsonFile.json', 'w')  
    fileObject.write(json_str)  
    fileObject.close() 

    with open('terraform-provider-resourcedata.json', 'w') as f:
        json.dump(dict2json, f)
    print("Write json files DONE!")
    '''
    a = findURL("null_data_source","data")
    '''
   


    
   


if __name__ == '__main__':
    main()


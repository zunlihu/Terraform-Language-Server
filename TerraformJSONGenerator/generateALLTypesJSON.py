import os
import sys
import json
import numpy as np
import re
import urllib.request as Request
import log
import argparse
logger = log.setup_custom_logger('root')
def getName(arrayList):
    data = arrayList.tolist()
    return list(data.keys())

def getDescrip(provider):
    TerraformPath = 'https://www.terraform.io'
    url = TerraformPath+provider
    try:
        content = Request.urlopen(url).read().decode('utf-8')
    except:
        logger.info("URL ERROR!CAN NOT access the information from %s"%provider)
        return {}
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
    try:
        block = c_block[0]
    except:
        logger.info("ACCESS ERROR! CAN NOT find block types in %s"%provider)
        return {}

    c_item = re.findall(rgx_item, block, re.S|re.M)
     
    for item in c_item:
        itemList = {}
        item_href = re.findall(rgx_url, item, re.S|re.M)
        item_names = re.findall(rgx_name, item, re.S|re.M)
        rgx_itemname = r'html">(.*?)</a>'
        if(re.findall(rgx_itemname, item, re.S|re.M) != []):
            item_name = re.findall(rgx_itemname, item, re.S|re.M)[0]
        else:
            item_name = item_names[len(item_names) - 1]


        for i in range(len(item_names)):
            href = item_href[i]
            if(("#" in href) and ("Resource" in item_names[i] or "Data" in item_names[i])):
                groupName = item_names[i]
                continue
            elif(".html" in href):
                item_url = href
            
        item_groupName = groupName
        
        print("Name:%s    groupName:%s"%(item_name, item_groupName))
        print("URL:%s"%(TerraformPath+item_url))
        itemList["name"] = item_name
        itemList["url"] =  TerraformPath+item_url
        itemList["groupName"] = item_groupName
        itemList["args"] = findItemDescrip(TerraformPath+item_url,"args") 
        itemList["attrs"]  = findItemDescrip(TerraformPath+item_url,"attrs")
        
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

def findItemDescrip(url, descrip):
    
    content = Request.urlopen(url).read().decode('utf-8')
    itemList = []
    if(descrip == "args"):
        rgx_descrip = r'Argument Reference(.*?)(<h2|</ul>)'
        cn_descrip = re.findall(rgx_descrip, content, re.S|re.M)
        if(cn_descrip == []):
            logger.info("WARNing! %s DO NOT have %s Reference!"%(url, descrip))
            return []
        else:
            c_descrip = cn_descrip[0][0]
    elif(descrip == "attrs"):
        rgx_descrip = r'(Attributes|Attribute) Reference(.*?)</ul>'
        cn_descrip = re.findall(rgx_descrip, content, re.S|re.M)
        if (cn_descrip == [] or len(cn_descrip[0]) == 1):
            logger.info("WARNing! %s DO NOT have %s Reference!"%(url, descrip))
            return []
        else:
            c_descrip = cn_descrip[0][1]

    rgx_item = r'<li>(.*?)</li>'
    c_item = re.findall(rgx_item, c_descrip, re.S|re.M)
    print("Find %s %s reference!"%(str(len(c_item)),descrip))
    rgx_name = r'<a name="(.*?)" />'
    rgx_description = r'(</a>|-)(.*?)\.'
    for item in c_item:
        item_dict = {}
        c_name = re.findall(rgx_name, item, re.S|re.M)
        if(c_name != []):
            item_dict["name"] = c_name[0]
            try:
                c_description = re.findall(rgx_description, item, re.S|re.M)[0]
                item_dict["description"] = re.sub('<(.*?)>',"",c_description[1]) 
            except:
                #logger.info("ERROR! %s CANNOT find %s description!"%(url,c_name[0]))
                item_dict["description"] = ""
            print(c_name,item_dict["description"])
            item_dict["args"] = []
            itemList.append(item_dict)
    
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
            itemList["args"] = findItemDescrip(TerraformPath+item_url,"args") 
            itemList["attrs"]  = findItemDescrip(TerraformPath+item_url,"attrs")
            
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
    itemList["args"] = findItemDescrip(TerraformPath+item_url,"args") 
    itemList["attrs"]  = findItemDescrip(TerraformPath+item_url,"attrs")
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
    itemList["args"] = findItemDescrip(TerraformPath+item_url,"args") 
    itemList["attrs"]  = findItemDescrip(TerraformPath+item_url,"attrs")
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
    itemList["args"] = findItemDescrip(item_url,"args") 
    itemList["attrs"]  = findItemDescrip(item_url,"attrs")
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
            itemList["args"] = findItemDescrip(TerraformPath+item_url,"args") 
            itemList["attrs"]  = findItemDescrip(TerraformPath+item_url,"attrs")
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
def getALLproviders(save_path, run_opt):
    allProviders = {}
    dataList = {}
    resourceList = {}

    url = 'https://www.terraform.io/docs/providers/'
    content = Request.urlopen(url).read().decode('utf-8')
    rgx_table = r'<table class="table">(.*?)</table>'
    c_table = re.findall(rgx_table, content, re.S|re.M)
    
    rgx_td = r'<td>(.*?)</td>'
    rgx_url = r'<a href="(.*?)">'
    rgx_name = r'/providers/(.*?)/'
    c_td = re.findall(rgx_td, c_table[0])
    for item in c_td:
        provider_url = re.findall(rgx_url, item)
        if(provider_url != []):
            provider_name = re.findall(rgx_name, provider_url[0])[0]
            
            if(provider_name == "null"):
                providerDict = getNullDes(provider_url[0])
            elif(provider_name == "http"):
                providerDict = getHttpDes(provider_url[0])
            elif(provider_name == "external"):
                providerDict = getExternalDes(provider_url[0])
            elif((provider_name == "archive") | (provider_name =="terraform-enterprise")):
                providerDict = geth4Des(provider_url[0])
            else:
                providerDict = getDescrip(provider_url[0])
            
            if(providerDict != {}):
                if("data" in providerDict.keys()):
                    dataList = dict(dataList, **providerDict["data"])
                if("resource" in providerDict.keys()):
                    resourceList = dict(resourceList, **providerDict["resource"])
                
            else:
                filename = "terraform-provider-"+provider_name+".txt"
                with open(save_path + filename, 'w') as f:
                    f.write("{}")
                f.close()
    allProviders["data"] = dataList
    allProviders["resource"] = resourceList
    if(run_opt == 1):
        with open ("terraform-allprovider-noranked.json","w") as f:
            json.dump(allProviders, f)
        f.close()
    return allProviders

def main():
    save_path = './'
    dataranklist = './data_count/data_nums.npy'
    resourceranklist = './data_count/res_nums.npy'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_path', type=str, default=save_path, help='(Optional) Define the folder to save files. If not exist, create it.')
    parser.add_argument('--run_opt', type=int, default=1, help='(Optional) Define the run option. 1 represents no priority, 2 represents ranking based on defined priority.')
    parser.add_argument('--dataRanklist', type=str, default=dataranklist, help='(Optional) If run option is defined as 1, then you have to define ranklist for data types in *.npy.')
    parser.add_argument('--resourceRanklist', type=str, default=resourceranklist, help='(Optional) If run option is defined as 1, then you have to define ranklist for resource types in *.npy.')
    args = parser.parse_args()

    if args.save_path:
        save_path = args.save_path
    if args.dataRanklist:
        dataranklist = args.dataRanklist    
    if args.resourceRanklist:
        resourceranklist = args.resourceRanklist 

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    ################# Get ALL resource and data types information for ALL providers###########
    allproviders = getALLproviders(save_path, args.run_opt)
    dataList = allproviders["data"]
    resourceList = allproviders["resource"]
    
    ######################## Rank as defined list #############################
    if(args.run_opt == 2):
        rankedData = {}
        rankedResource = {}
        resNameList = np.load(resourceranklist)
        dataNameList = np.load(dataranklist)
        dataName = getName(dataNameList)
        resName = getName(resNameList)
        for name in dataName:
            print(name)
            try:
                rankedData[name] = dataList[name]
            except:
                continue
        rankedData = dict(rankedData, **dataList)
        print ("Get data types description Done!")
        for name in resName:
            print(name)
            try:
                rankedResource[name] = resourceList[name]
                del dataList[name]
            except:
                continue
        rankedResource = dict(rankedResource, **resourceList)
        print ("Get resource types description Done!")
        
        dict2json = {}
        dict2json["data"] = rankedData
        dict2json["resource"] = rankedResource

        with open(save_path +'terraform-provider-ranked.json', 'wt') as f:
            json.dump(dict2json, f)
        f.close()
        print("Write json files DONE!")

if __name__ == '__main__':
    main()
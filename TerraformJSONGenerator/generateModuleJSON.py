# -*- coding: utf-8 -*-
import argparse
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
import datetime
import json
import re
from operator import itemgetter

def get_results(url):
    try:
        req =  Request(url)
        response = urlopen(req).read()
        results = json.loads(response.decode())
        return results
    except:
        return []

def findInput(url):
    try:
        results = get_results(url)
        inputs = results["root"]["inputs"]
        return inputs
    except:
        return []

def getModules(modules):
    moduleList = {}
    rgx_source = r'(.*)/'
    for module in modules:
        itemList = {}
        module_source = re.findall(rgx_source,module["id"])[0]
        module_url = 'https://registry.terraform.io/modules/' + module_source
        module_name = module["name"]
        if(module_source in moduleList.keys()):
            print("ERROR! %s"%module_name)
        else:
            itemList["name"] = module_name
            itemList["url"] = module_url
            itemList["provider"] = module["provider"]
            itemList["version"] = module["version"]
            itemList["downloads"] = module["downloads"]
            itemList["description"] = module["description"]
            itemList["source"] = module_source
            itemList["args"] = findInput('https://registry.terraform.io/v1/modules/'+module_source)
            if module_name in moduleList :
                module_name = module_name + '_'+module["provider"]
            moduleList[module_source]= itemList
        #print("%s: Module %s Done!\n"%(module["provider"],module_name))
    return moduleList

def main():
    save_path = './'
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_path', type=str, default=save_path, help='(Optional) Define the folder to save files. If not exist, create it.')
    args = parser.parse_args()

    if args.save_path:
        save_path = args.save_path

    url = 'https://registry.terraform.io/v1/modules?limit=100'
    results = get_results(url)
    try:
        next_offset = results["meta"]["next_offset"]
    except:
        next_offset = []
    print("Offset: 0")
    modules = results["modules"]

    while(next_offset):
        url = 'https://registry.terraform.io/v1/modules?limit=100&offset=%s'%next_offset
        results = get_results(url)
        try:
            next_offset = results["meta"]["next_offset"]
        except:
            next_offset = []
        print("Offset: %s"%results["meta"]["current_offset"])
        modules+= results["modules"]
    
    modules_by_downloads = sorted(modules, key=itemgetter("downloads"),reverse =True)
    moduleList = getModules(modules_by_downloads)
    
    filename = "module-source-inputs.json"
    with open(save_path + filename, 'w') as f:
        json.dump(moduleList, f)
    f.close()
    print("Write modules into json files DONE!\n")
    
if __name__ == '__main__':
    main()

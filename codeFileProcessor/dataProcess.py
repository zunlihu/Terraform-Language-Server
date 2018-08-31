import os
import sys
import re
import collections
import matplotlib.pyplot as plt
import numpy as np
import wordcloud
import argparse
from pyecharts import WordCloud, Bar

def resourceExtract(text):
    reg_res = r'resource "(.*?)"'
    results = re.findall(reg_res,text)
    return results

def dataExtract(text):
    reg_res = r'data "(.*?)"'
    results = re.findall(reg_res,text)
    return results

def providerExtract(text):
    reg_res = r'provider "(.*?)"'
    results = re.findall(reg_res,text)
    return results

def get_wordCounts(file):
    if "resource" in file:
        type = "resource"
    if "data" in file:
        type = "data"

    with open(file,'rt') as f:
        word_box = []
        for line in f:
            word_box.extend(line.strip().split())
    counts = collections.Counter(word_box)
    counts=collections.OrderedDict(sorted(counts.items(), key=lambda t: t[1], reverse=True))
    np.save(file+'_ranked.npy', counts)

    with open( file+ "_ranked.txt","wt") as f:
        for item in list(counts.keys()):
            f.write(item + '\n')
    f.close()

    # Plot figures
    x = list(counts.keys())[0:50]
    y = list(counts.values())[0:50]
    bar = Bar('Terraform '+type+' types usage',width=1200, height=600)
    bar.add("", x, y,xaxis_min="dataMin",xaxis_max="dataMax",xaxis_interval=0,xaxis_margin =5,xaxis_label_textsize=9,xaxis_rotate=30,label_color=['#468','#2B4'])
    bar.render(type+'_bar.html')

    
    ## Plot wordCloud
    wordcloud = WordCloud(width=1200, height=620)
    wordcloud.add("", x, y, word_size_range=[30, 100],
                shape='diamond')
    wordcloud.render(type+'_wordCloud.html')
   
def wordCloud(frequencies):
    cloud = wordcloud.WordCloud(
        background_color='white'
    )
    cloud.fit_words(frequencies)

    plt.imshow(cloud)
    plt.axis("off")
    plt.savefig('wordCloud.png')
    plt.show()

def ignoreComment(text):
    res = text
    rgx_line = r'#(.*)'
    res = re.sub(rgx_line,"",res) 
    
    rgx_block = r'/\*((?:.|\n)*?)\*/'
    res = re.sub(rgx_block,"",res) 
    return res

def main():
    
    save_path = './'
    code_path = './data_tf'
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_path', type=str, default=save_path, help='(Optional) Define the folder to save files. If not exist, create it.')
    parser.add_argument('--code_path', type=str, default=code_path, help='(Required) Define the folder where program files are placed in.')
    
    args = parser.parse_args()
  
    if args.save_path:
        save_path = args.save_path
    if args.code_path:
        code_path = args.code_path
    
    if(save_path[-1] != '/'):
       save_path += '/'
    if(code_path[-1] != '/'):
        code_path += '/'
    files = os.listdir(code_path)
    res_type = open( 'extracted_resources.txt','wt')
    data_type = open( 'extracted_datatypes.txt','wt')
    for file in files:
        try:
            with open(code_path+file,'rt',encoding="utf8") as f:
                text = f.read()
            f.close()
            print("Read %s Done!"%file)   
        except:    
            print("ERROR! Can NOT open %s!"%file)
        text = ignoreComment(text)
        res = resourceExtract(text) 
        data = dataExtract(text)
        for item in res:
            res_type.write("%s\n"%item) 
        for item in data:
            data_type.write("%s\n"%item) 
    res_type.close()
    data_type.close()
    print("Read ALL Files Done!")
    
    get_wordCounts('extracted_resources.txt')
    get_wordCounts('extracted_datatypes.txt')

    
    
if __name__ == '__main__':
    main()

    







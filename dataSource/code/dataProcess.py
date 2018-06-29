import os
import sys
import re
import collections
import matplotlib.pyplot as plt
import numpy as np
import wordcloud

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

def get_wordNums(file):
    with open(file,'rt') as f:
        word_box = []
        for line in f:
            word_box.extend(line.strip().split())

    return collections.Counter(word_box)

def wordCloud(frequencies):
    cloud = wordcloud.WordCloud(
        background_color='white'
    )
    cloud.fit_words(frequencies)

    plt.imshow(cloud)
    plt.axis("off")
    plt.savefig('./data_count/images/res_wordCloud.png')
    plt.show()

def ignoreComment(text):
    res = text
    rgx_line = r'#(.*)'
    res = re.sub(rgx_line,"",res) 
    
    rgx_block = r'/\*((?:.|\n)*?)\*/'
    res = re.sub(rgx_block,"",res) 
    return res

def main():
    
    tf_path = './data_tf'
    txt_path = './data_txt'
    res_type = open('./data_count/resources.txt','wt')
    files = os.listdir(txt_path)
    
    for file in files:
        try:
            with open(txt_path+"/"+file,'rt',encoding="utf8") as f:
                text = f.read()
                f.close()
                print("Read %s Done!"%file)

        except:    
            print("ERROR! Can NOT open %s!"%file)
        text = ignoreComment(text)
        res = resourceExtract(text) 
        for item in res:
            res_type.write("%s\n"%item) 
    res_type.close()
    print("Read ALL Files Done!")
    
    res_data = get_wordNums('./data_count/resources.txt')
    print(res_data)
    
    res_data=collections.OrderedDict(sorted(res_data.items(), key=lambda t: t[1], reverse=True))
    np.save('res_nums.npy',res_data)
    with open("res_nums.txt","wt") as f:
        for item in list(res_data.keys()):
            f.write(item + '\n')
    f.close()

    # Plot figures
    x = list(res_data.values())[0:50]
    y = list(res_data.keys())[0:50]
    plt.barh(range(len(x)),x,align='center')
    plt.yticks(range(len(y)), y)
    plt.xlabel('Counts')
    plt.title('Terraform resource types usage')
    plt.savefig('./data_count/images/resNums.png')
    plt.show()
    
    wordCloud(res_data)
    '''
    with open(txt_path+"/25268.txt",'rt',encoding="utf8") as f:
        text = f.read()
        f.close()
    text = ignoreComment(text)
    res = resourceExtract(text) 
    print(res)
    '''

if __name__ == '__main__':
    main()

    







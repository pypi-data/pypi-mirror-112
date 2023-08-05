#-*- encoding: UTF-8 -*-
import requests
import re
import os
def download_ris(id,path):
    '''
    retrieve ris for the file
    '''
    
    ris_url = 'https://ieeexplore.ieee.org/xpl/downloadCitations'
    data = {
        'recordIds': id,
        'download-format': 'download-ris',
        'citations-format': 'citation-only'
    }
    down_path = path+'\\'+id+'.ris'
    res = requests.post(ris_url,data=data)
    with open(down_path,'wb+') as f:
        f.write(res.content)
    print('RIS has been downloaded')

def save_path(path):
    with open('.\\download_path.txt','w') as f:
        f.write(path)

def read_path():
    if(os.path.exists('.\\download_path.txt')):
        with open('.\\download_path.txt','r') as f:
            return f.readlines()[0]
    else:
        path = input("Input download path:\n")
        save_path(path)
        return path

def test():
    path = read_path()
    url = input("URL: \n")

    while(url == "chp"):
        path = input("Input download path:\n")
        url = input("URL: \n")
        
    id = re.findall("(\d{6,})",url)[0]
    print(f"RIS try to download")
    try:
        download_ris(id,path)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    test()
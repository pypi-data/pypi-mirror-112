#-*- encoding: UTF-8 -*-
import requests
import re
def download_ris(id):
    '''
    retrieve ris for the file
    '''
    
    ris_url = 'https://ieeexplore.ieee.org/xpl/downloadCitations'
    data = {
        'recordIds': id,
        'download-format': 'download-ris',
        'citations-format': 'citation-only'
    }
    down_path = 'D:\\Downloads\\'+id+'.ris'
    res = requests.post(ris_url,data=data)
    with open(down_path,'wb+') as f:
        f.write(res.content)
    print('RIS has been downloaded')

def test():
    url = input("URL: \n")
    id = re.findall("=(\d.*)",url)[0]
    print(f"RIS try to download, ID = {id}")
    try:
        download_ris(id)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    test()
import requests
from bs4 import BeautifulSoup as soup
import os
import gzip
import io
import wget
import os

path=os.getcwd()

def getsoup(url):
    r=requests.get(url)
    Soup=soup(r.text,'html.parser')
    return Soup

def reset(i):
    with open(os.path.join(path,'cache.txt'),'w') as f:
        f.write(i)
        

def insert(i):
    url='https://directory.email-verifier.io/-email--email-list-'+i+'.html'
    Soup=getsoup(url)
    box=Soup.findAll('div',attrs={'class':'ibox-title'})[-1]
    rows=box.findAll('div',attrs={'class':'row'})[1:-1]
    with open(os.path.join(path,'data.txt'),'w') as f:
        for row in rows:
            div=row.findAll('div')
            f.write(div[0].find('a').get('href')+'|'+div[0].text.strip()+'|'+div[1].text.strip()+'|'+div[2].text.strip()+'|'+div[3].text.strip()+'|'+i+'|No\n')
    reset(i)

       
def geturl():
    with open('data.txt','r') as f:
        data=f.readlines()
        for d in data:
            flag=d.split('|')[-1]
            if('No' in flag):
                return d.split('|')[:-1]
    with open('cache.txt','r') as f:
        d=int(f.read())
    if(d==140945):
        return None
    else:
        insert(str(d+1))
        return geturl()



def getfiledata():
    with open('data.txt','r') as f:
        data=f.readlines()
        return data

def update():
    data=getfiledata()
    with open('data.txt','w+') as f:
        fg=1
        for d in data:
            flag=d.split('|')[-1]
            if('No' in flag and fg==1):
                flag='yes\n'
                fg=0
            fa=d.split('|')
            f.write(fa[0]+'|'+fa[1]+'|'+fa[2]+'|'+fa[3]+'|'+fa[4]+'|'+fa[5]+'|'+flag)
            

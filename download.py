import os
from aiohttp import ClientSession
import asyncio
from bs4 import BeautifulSoup as soup
import csv
import requests
import time
from function import geturl,update
import json


async def fetch(url, session):
    if(url[-1]==''):
        return []
    ur='https://directory.email-verifier.io/'+url[-1]    
    retries=0
    while(retries!=5):
        try:
            async with session.get(ur) as response:
                delay = response.headers.get("DELAY")
                date = response.headers.get("DATE")
                print("{}:{} with delay {}".format(date, response.url, delay))
                content= await response.read()
                Soup=soup(content,'html.parser')
                divs=Soup.findAll('div',attrs={'class':'col-lg-9'})
                if(len(divs)<2):
                    return url
                for div in divs[1:]:
                    email=div.text.strip()
                    email=email[email.find(':')+1:].strip()
                    url.append(email)
                return url
        except:
            print("Retrying "+url)
            retries=retries+1
    return []



async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, session)

async def run(r,locs,seed):
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(seed)
    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, locs[i], session))
            tasks.append(task)
        return await  asyncio.gather(*tasks)




def getlocs(url):
    ur='https://directory.email-verifier.io/'+url
    r=requests.get(ur)
    Soup=soup(r.text,'html.parser')
    try:
        web=Soup.find('a',attrs={'itemprop':'url'}).get('href')
    except:
        web=''
    rows=[web]
    prsns=Soup.findAll('div',attrs={'itemtype':'http://schema.org/Person'})
    for per in prsns:
        name=per.find('div',attrs={'itemprop':'name'}).text.strip()
        job=per.find('div',attrs={'itemprop':'jobTitle'}).text.strip()
        btn=per.find('div',attrs={'class':'btn-group'}).text.strip()
        if(btn=='Verify his/her professional email address for free'):
            link=per.find('a').get('href')
        else:
            link=''
        row=[name,job,link]
        rows.append(row)
    return rows
def download(seed):
    url=geturl()
    if(url==None):
        return None
    print(url)
    locs=getlocs(url[0])
    number=len(locs)
    with open('companies.txt','a') as f:
        f.write(url[1]+','+url[2]+','+url[3]+','+url[4]+','+url[5]+','+locs[0]+',')
        nms=[]
        for r in locs[1:]:
            nms.append(r[0])
        nms=','.join(nms)
        f.write(nms+'\n')
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(number-1,locs[1:],seed))
        rows=loop.run_until_complete(future)
    except:
        loop.stop()
        print("retrying "+url[0])
        return url
    with open('emails.txt','a') as f:
        for row in rows:
            if(row==[]):
                continue
            f.write(row[0]+','+row[1]+','+url[1]+',')
            for r in row[3:-1]:
                f.write(r+',')
            f.write(row[-1]+'\n')
            
    update()
    return url



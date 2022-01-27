import requests
from bs4 import BeautifulSoup 
import csv
import re
#from time import clock
from multiprocessing import Pool
import requests.api
from functools import partial
from fake_useragent import UserAgent

ua=UserAgent()

headers={
        "User-Agent":ua.random
        }

requests=requests.Session()
#start=clock()
page=requests.get("",headers=headers) #link to website is missing

soup=BeautifulSoup(page.content,'lxml')

links=soup.select('a[title$=" "]') #title is missing
states=[l.get_text() for l in links]
urls=[''+s for s in states] #url is missing
#pages=[requests.get(u) for u in urls]
p = Pool(16)  # Pool tells how many at a time
kwargs={'headers':headers}
req=partial(requests.get,**kwargs)
pages=p.map(req,urls)
p.terminate()
p.join()
soups=[BeautifulSoup(pa.content,'lxml') for pa in pages]
with open('oklahoma.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["State","Phone","Website"])
    i=0
    for sou in soups:
        so=sou.find_all('div', class_="info")
        phone=' '
        for j in range(0,len(so)):
            try:
                phoneN=so[j].text
                phoneNumbers=re.findall(r"\d{3}-\d{3}-\d{4}",phoneN)
                phone=phoneNumbers[0]
            except:
                pass
        website=' '
        for j in range(0,len(so)):
            if website==' ' and str(so[j].find_previous_sibling('h3'))=='<h3></h3>': #heading is missing
                try:
                    website=so[j].find('a', attrs={'href':re.compile("^http")}).get('href')
                except:
                    pass
        writer.writerow([states[i], phone, website])
        i=i+1
#end=clock()-start
#print(end)

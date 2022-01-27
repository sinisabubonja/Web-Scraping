import requests
from bs4 import BeautifulSoup 
import csv
import re
#from time import clock
from fake_useragent import UserAgent
import Tor

def requests_with_thor(u):
    ua=UserAgent()
    headers={"User-Agent":ua.random}
    Tor.renew_connection()
    r=requests.get(u,proxies={"http":"socks5://127.0.0.1:9050","https":"socks5://127.0.0.1:9050"},headers=headers)
    print("You visited the link {}".format(u))
    req=requests.get('http://httpbin.org/user-agent',proxies=proxies,headers=headers)
    print("\nYour user agent is {}\n\n\n".format(req.json()['user-agent']))
    return r

proxies={
        "http":"socks5://127.0.0.1:9050",
        "https":"socks5://127.0.0.1:9050"
        }

ua=UserAgent()

headers={
        "User-Agent":ua.random
        }

requests=requests.Session()
#start=clock()
page=requests.get("http://www.county-clerk.net/county.asp?state=Oklahoma",proxies=proxies,headers=headers)

req=requests.get('http://httpbin.org/ip',proxies=proxies,headers=headers)
print("\nYour IP address is {}\n".format(req.json()['origin']))
print("You visited the link http://www.county-clerk.net/county.asp?state=Oklahoma\n")
req=requests.get('http://httpbin.org/user-agent',proxies=proxies,headers=headers)
print("Your user agent is {}\n\n".format(req.json()['user-agent']))

soup=BeautifulSoup(page.content,'lxml')

links=soup.select('a[title$=" county clerk oklahoma"]')
states=[l.get_text() for l in links]
states=[states[i] for i in range(0,5)]
urls=['http://www.county-clerk.net/countyclerk.asp?state=Oklahoma&county='+s for s in states]
pages=[requests_with_thor(u) for u in urls]

soups=[BeautifulSoup(pa.content,'lxml') for pa in pages]
with open('oklahoma.csv','w') as csv_file:
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
            if website==' ' and str(so[j].find_previous_sibling('h3'))=='<h3>County Website</h3>':
                try:
                    website=so[j].find('a', attrs={'href':re.compile("^http")}).get('href')
                except:
                    pass
        writer.writerow([states[i], phone, website])
        i=i+1
#end=clock()-start
#print(end)

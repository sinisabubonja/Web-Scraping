from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
from time import sleep
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from multiprocessing import Process, Manager

def name(soup,table):
    name=soup.find('div', class_="search-page-heading-red")
    name=re.findall(r"\s*(.+[^$\s])[\s\ ]*",str(name.get_text()))
    name=name[0]
    table['name']=name

def address(soup,table):
    address=soup.find('img', src="images/address-icon.png")
    address=address.nextSibling
    address=address.nextSibling
    address=address.nextSibling
    address1=re.sub(r' ,',',',str(address))
    address1=re.sub(r'- ',' ',str(address1))
    address1=re.findall(r"[^\s]+",str(address1))
    address1=' '.join(address1)
    address=address.nextSibling
    address=address.nextSibling
    address2=re.sub(r' ,',',',str(address))
    address2=re.sub(r'- ',' ',str(address2))
    address2=re.findall(r"[^\s]+",str(address2))
    address2=' '.join(address2)
    address=address1+'\n'+address2
    table['address']=address

def phone(soup,table):
    phone=soup.find('img', src="images/call.png")
    phone=phone.nextSibling
    phone=re.findall(r"[^\s]+",str(phone))
    phone=' '.join(phone)
    table['phone']=phone

def industry(soup,table):
    boxes=soup.find_all('div', class_="overview-box2")

    industry=boxes[0].find_all('strong')
    industry=industry[0].nextSibling
    industry=industry.nextSibling
    industry=re.sub(r' ,',',',str(industry))
    industry=re.findall(r"[^\s]+",str(industry))
    industry=' '.join(industry)
    table['industry']=industry

def comptype(soup,table):
    boxes=soup.find_all('div', class_="overview-box2")

    companytype=boxes[1].find_all('strong')
    companytype=companytype[0].nextSibling
    companytype=companytype.nextSibling
    companytype=re.sub(r' ,',',',str(companytype))
    companytype=re.findall(r"[^\s]+",str(companytype))
    companytype=' '.join(companytype)
    table['companytype']=companytype

if __name__ == '__main__':

    m=Manager()
    table=m.dict()

    table['name']=' '
    table['address']=' '
    table['phone']=' '
    table['industry']=' '
    table['companytype']=' '

    ua=UserAgent()

    opts = Options()
    opts.add_argument(ua.random)

    driver = webdriver.Chrome(chrome_options=opts) 
    driver.get("") #link to website is missing
    driver.find_element_by_link_text("3 Elements Events").click()
    driver.switch_to_window(driver.window_handles[0])
    driver.close()
    driver.switch_to_window(driver.window_handles[0])

    file=open('companies.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(["CompanyName","Address","Phone Number","Industry","Company Type"])

    next=True
    i=0
    while next==True:  
        i=i+1
        if i==1333:
            next=False
    
        soup = BeautifulSoup(driver.page_source,"lxml")
        #suvisno ali neka
        try:
            driver.find_element_by_link_text("Next »").click()
        except:
            next=False

        delay=300
        try:
            myElemL = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search-page-heading-red')))
        except TimeoutException:
            print("Loading took too much time!")  

        p1=Process(target=name, args=(soup,table))
        p2=Process(target=address, args =(soup,table))
        p3=Process(target=phone, args =(soup,table))
        p4=Process(target=industry, args =(soup,table))
        p5=Process(target=comptype, args =(soup,table))

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()

        writer.writerow([table['name'],table['address'],table['phone'],table['industry'],table['companytype']])

        if next==False:
            break

    file.close()
    driver.close()

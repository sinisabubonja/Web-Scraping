from selenium import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
from time import sleep
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

#first open tor browser

ua=UserAgent()

webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent']=ua.random

service_args=['--proxy=localhost:9150','--proxy-type=socks5',]

driver=webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',service_args=service_args)

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
    if i==1334:
        break
    soup = BeautifulSoup(driver.page_source,"lxml")
    try:
        driver.find_element_by_link_text("Next »").click()
    except:
        next=False

    delay=300
    try:
        myElemL = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search-page-heading-red')))
    except TimeoutException:
        print("Loading took too much time!")  

    name=soup.find('div', class_="search-page-heading-red")
    name=re.findall(r"\s*(.+[^$\s])[\s\ ]*",str(name.get_text()))
    name=name[0]

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

    phone=soup.find('img', src="images/call.png")
    phone=phone.nextSibling
    phone=re.findall(r"[^\s]+",str(phone))
    phone=' '.join(phone)

    boxes=soup.find_all('div', class_="overview-box2")

    industry=boxes[0].find_all('strong')
    industry=industry[0].nextSibling
    industry=industry.nextSibling
    industry=re.sub(r' ,',',',str(industry))
    industry=re.findall(r"[^\s]+",str(industry))
    industry=' '.join(industry)

    companytype=boxes[1].find_all('strong')
    companytype=companytype[0].nextSibling
    companytype=companytype.nextSibling
    companytype=re.sub(r' ,',',',str(companytype))
    companytype=re.findall(r"[^\s]+",str(companytype))
    companytype=' '.join(companytype)

    writer.writerow([name,address,phone,industry,companytype])

    if next==False:
        break

file.close()
driver.close()



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

headers={#'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent':ua.random,
        #'Accept-Encoding':'gzip',
        }

for key, value in headers.items():
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

#sudo npm install selenium-standalone@latest -g
#sudo selenium-standalone install
#selenium-standalone start
#service_args=['--webdriver=8080',]

service_args=['--proxy=localhost:9150','--proxy-type=socks5','--load-images=no',]

driver=webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',service_args=service_args)

#driver.get("http://httpbin.org/anything")
#driver.get_screenshot_as_file('anything.png')
#print(driver.page_source)

sessions=['20175','20179']
years=['1', '2', '3', '4']
dict={'20175':'Summer 2017','20179':'Fall/Winter 2017-2018'}

file=open('university_course_data_via_tor.csv', 'w')
writer = csv.writer(file)
writer.writerow(["Session","Year of Study","Course Code","Course Name","Course Description"])

for se in sessions:
    for ye in years: 
        driver.get("") #link to website is missing
        delay=300
        try:
            myElemL = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.selectize-input.items.has-options.full.has-items')))
            #print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")        
        session=driver.find_element_by_css_selector("div.selectize-input.items.has-options.full.has-items")
        session.click()
        sel="div.option[data-value='"+se+"']"
        delay = 300 # seconds
        try:
            myElemS = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            #print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")        
        s=driver.find_element_by_css_selector(sel)
        s.click()
        delay=300
        try:
            myElemYe = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.selectize-input.items.not-full.has-options")))
            #print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")         
        year=driver.find_element_by_css_selector("div.selectize-input.items.not-full.has-options")
        year.click()
        sel="div.option[data-value='"+ye+"']"
        delay = 300 # seconds
        try:
            myElemY = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            #print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")        
        y=driver.find_element_by_css_selector(sel)
        y.click()
        driver.find_element_by_css_selector("div.bannerText").click()
        driver.find_element_by_xpath('//button[text()="Search Courses"]').click()
        #sleep(1)
        delay = 300 # seconds
        try:
            myElemB = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'course')))
            #print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        soup = BeautifulSoup(driver.page_source,"lxml")
        courses=soup.find_all('div', class_="course")
        num_courses=len(courses)
        for i in range(0,num_courses):
            coursecode_name=courses[i].find('span').find('h4')
            descript=courses[i].find('div', class_="alert alert-info infoCourseDetails infoCourse")
            cc_n=coursecode_name.get_text()
            cd=descript.get_text()
            coursecode=re.findall(r"[A-Z]{3}\d{3}[A-Z]{1}\d{1}[A-Z]{1}",cc_n)   
            name=re.findall(r"[A-Z]{3}\d{3}[A-Z]{1}\d{1}[A-Z]{1}\ - (.+)",cc_n)
            description=re.findall(r"[\s]*([^\[\]]+)",cd)
            coursecode=coursecode[0]
            name=name[0]
            description=description[0]
            writer.writerow([dict[se],ye,coursecode,name,description])

file.close()
driver.close()

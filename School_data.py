#import all the necessary libraries
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from time import sleep
import numpy as np

#configure webdriver to use Chrome browser
driver = webdriver.Chrome("C:\\Users\\dell\\Documents\\python_web_scrapping\\chromedriver.exe")

#URL that you want to scrape
driver.get("https://targetstudy.com/school/cbse-schools-in-madhya-pradesh.html") 


names=[]
details=[]
locations=[]
locations1=[]
locations2=[]
links=[]

#extracting the data and storing the data in variables
i=1
while True:
    content = driver.page_source
    soup = BeautifulSoup(content)
    print("Page Number : %d" % (i))
    for a in soup.findAll('div', attrs={'class':'card-body'}):

        name = a.find('h4')
        location = a.find('p', attrs={'class':'card-subtitle mt-0'})
        detail = a.find('ul', attrs={'class':'list-info'})
        
        if name != None:
            names.append(str(name.text))

        if location !=None:
            locations.append(str(location.text).replace(u'\xa0', u'|').replace("Indiaphone","|").replace("_iphone","").replace("phone_iphone","").replace("location_on","").replace(u'\n',u'').split("|"))
        
        if detail != None:
            details.append(str(detail).replace('<ul class="list-info">','').replace('</li>',',').replace('<li>','').replace('</ul>',''))
            
   
    try:
        driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div/div[1]/div[2]/ul/li[7]/a').click()
        sleep(5)
        i+=1
        if i>29:
            break
    except:
        break
        

#Storing the data in a required format
names = np.array(names)
locations = np.array(locations)
city_location = []
city_info= []
phone=[]
for i in locations:
    city_location.append(i[0].strip())
    city_info.append(i[1].strip())
    if len(i)==3:
        phone.append(i[2].strip().replace(" ",""))
    else:
        phone.append('NA')

details = np.array(details)

df = pd.DataFrame(list(zip(names,city_location,city_info, phone, details)),columns=['School_Name','Location','City','Phone',"Details"])
df.to_csv("school_details.csv")

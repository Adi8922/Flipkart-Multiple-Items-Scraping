import pandas as pd
import requests
from bs4 import BeautifulSoup
from glob import glob
from datetime import datetime
import re

inputfile = ("C:/Users/Ḥ/aditya/Aditya.xlsx")
inputfile
dfdata = pd.read_excel(inputfile)
categories = dfdata["categories"].to_list()
print(categories)

columns = ["name","prices","discount","quantity"]

for item in categories:
    url = "https://www.flipkart.com/search?q="+item.lower().replace(" ","%20")+"grocery&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    res = requests.get(url)
    html = res.content
    data = open("C:/Users/Ḥ/aditya/"+item+".html","wb")
    data.write(html)
    data.close()
   
files = glob("C:/Users/Ḥ/aditya/*.html")   
for file in files:
    output = []
    data = open(file,"rb")
    content = data.read().decode("utf-8")
    #print(type(content))
    data.close()
    soup = BeautifulSoup(content,"lxml")
    page_tag = soup.find("div","_1YokD2 _2GoDe3 col-12-12")
    products_rows = page_tag.find_next_siblings("div","_1AtVbE col-12-12")
    for row in products_rows:
        products = row.findAll("div",{"data-id":re.compile(".*")})
        for product in products:
            try:
                product_name = product.find("a",attrs={"class":"s1Q9rs"})["title"]
            except: 
                product_name = None
            
            try:   
                product_prices = product.find("div",attrs={"class":"_30jeq3"}).text
            except:
                product_prices = None
            try:    
                product_discount = product.find("div",attrs={"class":"_3Ay6Sb"}).text
            except:
                product_discount = None
            
            try:       
                product_quantity = product.find("div",attrs={"class":"_3Djpdu"}).text
            except:  
                product_quantity = None
                
            output_rows = [product_name,product_prices,product_discount,product_quantity]
            output.append(output_rows)
                    
    outfile = file.replace(".html",".xlsx")
    out_data = pd.DataFrame(output,columns=columns)
    out_data.to_excel(outfile,index=False)


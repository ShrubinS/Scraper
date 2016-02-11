from bs4 import BeautifulSoup
import urllib
import requests     
import os
import urllib2
import json

products = {}

def _crawl_():
    r = urllib.urlopen('http://www.walmart.com/search/?query=mobile%20phones&cat_id=3944_542371_1073085').read()
    soupthis = BeautifulSoup(r)
    while soupthis:
        print("-------------START OF NEXT PAGE-------------") 
        product_divs = soupthis.find_all("div", class_="js-tile js-tile-landscape tile-landscape")        
        
        for product_div in product_divs:
            product = {}
            text = product_div.div.h4.a.get_text()
            link = product_div.a['href']
            link = 'http://www.walmart.com' + link
            product['product_link'] = link
            print product['product_link']
            products.setdefault(text,[]).append(product)
        print("---------------PRODUCT LINKS ADDED FOR PAGE 1-----------------")    

        for productName in products:
            values = products[productName]
            child = values[0]
            product = {}
            link = child['product_link']
            r = requests.get(link)
            data = r.text
            soup = BeautifulSoup(data)
            div_features = soup.find_all("div", class_="js-ellipsis module")
            if div_features:
                product['features'] = div_features[0].get_text()
                products[productName].append(product)
        print("---------------PRODUCT FEATURES ADDED FOR PAGE 1-----------------")    
    
        for product_div in product_divs:
            product = {}
            product['img_src'] = product_div.a.img['data-default-image']
            print product['img_src']
            products[product_div.div.h4.a.get_text()].append(product)
        print("-----------PRODUCT IMAGES (IMAGE_SRC) ADDED FOR PAGE 1--------------")    
    
        print products
        
        for productName in products:
            values = products[productName]
            imgUrl_dict = values[2]
            imgUrl = imgUrl_dict['img_src']
            url_img = os.path.basename(imgUrl)
            url_dir = ""
            url_dir = "C:\walmart\\" + url_img
            urllib.urlretrieve(imgUrl, url_dir)
            product = {}
            product['img_local'] = url_dir
            print product['img_local']
            products[productName].append(product)
        print("-----------PRODUCT IMAGES (IMAGE_LOCAL) ADDED FOR PAGE 1--------------")     
    
        next_button = soupthis.find_all("a", class_="paginator-btn paginator-btn-next")
        soupthis = []
        if next_button:
            print next_button[0]
            next_ = next_button[0]['href']
            next_link = "http://www.walmart.com/search/" + next_
            r = requests.get(next_link)
            data = r.text
            soupthis = BeautifulSoup(data)
    with open("wallmart_products.json", "w") as writeJSON:
        json.dump(products, writeJSON)        
    
    
_crawl_()
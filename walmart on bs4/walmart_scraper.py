from bs4 import BeautifulSoup
import urllib
import requests     
import os
import urllib2

r = urllib.urlopen('http://www.walmart.com/search/?query=mobile%20phones&cat_id=3944_542371_1073085').read()
soupthis = BeautifulSoup(r)

products = {}

product_divs = soupthis.find_all("div", class_="js-tile js-tile-landscape tile-landscape")

for product_div in product_divs:
    product = {}
    text = product_div.div.h4.a.get_text()
    link = product_div.a['href']
    link = 'http://walmart.com' + link
    product['product_link'] = link
    print product['product_link']
    products.setdefault(text,[]).append(product)
    

for productName in products:
    values = products[productName]
    print values
    child = values[0]
    product = {}
    link = child['product_link']
    print link
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data)
    div_features = soup.find_all("div", class_="js-ellipsis module")
    product['features'] = div_features[0].get_text()
    products[productName].append(product)  

for product_div in product_divs:
    product = {}
    print product_div.a.img['data-default-image']
    product['img_src'] = product_div.a.img['data-default-image']
    print product['img_src']
    products[product_div.div.h4.a.get_text()].append(product)
    

for productName in products:
    values = products[productName]
    imgUrl_dict = values[2]
    print imgUrl_dict
    imgUrl = imgUrl_dict['img_src']
    url_img = os.path.basename(imgUrl)
    url_dir = ""
    url_dir = "C:\walmart\\" + url_img
    urllib.urlretrieve(imgUrl, url_dir)
    product = {}
    product['img_local'] = url_dir
    products[productName].append(product)
    
products
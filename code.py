from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#Functions

def get_title(soup):
    
    try:
        title = soup.find('div', attrs = {'id': 'titleSection'}).find('span', attrs = {'id': 'productTitle'}).text.strip()
    except AttributeError:
        title = ""
        
    return title

def get_price(soup):
    
    try:
        price = soup.find('div', attrs = {"id": "corePriceDisplay_desktop_feature_div"}).find('span', attrs = {"class": "a-price-whole"}).text.replace('.', '')
    except AttributeError:
        price = ""
        
    return price

def get_ratings(soup):
    
    try:
        ratings = soup.find('div', attrs = {"id": "averageCustomerReviews"}).find('span', attrs = {"class": "a-size-base a-color-base"}).text.strip()
    except AttributeError:
        ratings = ""
        
    return ratings
    
       

# code to web scrape

URL = "https://www.amazon.in/s?k=iphone&crid=1KAKAV0S7JU98&sprefix=iphone%2Caps%2C206&ref=nb_sb_noss_1"

HEADERS = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36', 'Accept-Language' : 'en-US, en;q=0.5'})

response = requests.get(URL, headers = HEADERS)

soup = BeautifulSoup(response.content, "html.parser")

links = soup.find_all("a", attrs = {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})


link_list = []

for x in links:
    link_list.append(x.get('href'))
    
d = {"title" : [], "price" : [], "ratings" : []}

for link in link_list:
    webpage = requests.get("https://www.amazon.in/" + link, headers = HEADERS)
    new_soup = BeautifulSoup(webpage.content, "html.parser")
    
    d['title'].append(get_title(new_soup))
    d['price'].append(get_price(new_soup))
    d['ratings'].append(get_ratings(new_soup))
    
    
# dictionary to data frame   
amazon_df = pd.DataFrame.from_dict(d)

amazon_df['title'].replace('', np.nan, inplace=True)
amazon_df.dropna(subset=['title'], inplace = True)

# data frame to csv file
amazon_df.to_csv("amazon_data_2.csv", header=True, index=False)
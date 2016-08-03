# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 15:36:42 2016

@author: brjohn
"""

import proxy
from bs4 import BeautifulSoup

def find_occurences(yelp_id, key_wds):
    yelp_base = 'http://www.yelp.com'
    
    a = proxy.open_url(yelp_base+yelp_id)
    r = BeautifulSoup(a, 'html.parser')
    
    merchant_name = r.find("h1", {"itemprop":"name"}).text.strip()
    postal_code = r.find("span", {"itemprop": "postalCode"}).text 
    state = r.find("span", {"itemprop":"addressRegion"}).text
    try:    
        num_reviews = r.find("span", {"itemprop": "reviewCount"}).text
    except:
        num_reviews = 0
    try:    
        rating = r.find("meta", {"itemprop": "ratingValue"})['content']
    except:
        rating = 0
    
    reviews = []
    for item in r.findAll("p", {"itemprop":"description"}):
        reviews.append(item.text.replace('<br>', ' ').replace('</br>', ' '))
    
    key_wd_count = 0
    
    for wd in key_wds:
        for rev in reviews:
            key_wd_count += rev.lower().count(wd)

    num_reviews = max(1, int(num_reviews))    
    key_wd_ratio = 1.0*key_wd_count/num_reviews
    
    print yelp_id
    print merchant_name
    print "postal code: ", postal_code
    print "state: ", state
    print "num reviews: ", num_reviews
    print "rating: ", rating
    print "key_wd count: ", key_wd_count
    print "key_wd/review: ", key_wd_ratio
    
    return key_wd_ratio
    
def find_key_wd_rating(yelp_id, key_wds):
    yelp_base = 'http://www.yelp.com'

    try:    
        a = proxy.open_url(yelp_base+yelp_id)
    except:
        print "Error accessing page"
        return -1
        
    r = BeautifulSoup(a, 'html.parser')

    try:    
        num_reviews = r.find("span", {"itemprop": "reviewCount"}).text
    except:
        return -1
    
    reviews = []
    for item in r.findAll("p", {"itemprop":"description"}):
        reviews.append(item.text.replace('<br>', ' ').replace('</br>', ' '))
    
    key_wd_count = 0
    
    for wd in key_wds:
        for rev in reviews:
            key_wd_count += rev.lower().count(wd)

    num_reviews = max(1, int(num_reviews))    
    key_wd_ratio = 1.0*key_wd_count/num_reviews
    
    return key_wd_ratio

if __name__ == '__main__':
    # Testing:
    business_yelp_id = '/biz/uncorked-wine-co-new-york-3'
    key_wds = ['wine', 'cabernet', 'vino']
    
    find_occurences(business_yelp_id, key_wds)
    
    ## find other links
    
    a2 = proxy.open_url("http://www.yelp.com/nyc")
    r2 = BeautifulSoup(a2, 'html.parser')
    
    yelp_base = 'http://www.yelp.com/'
    biz_IDs=[]
    
    for i in r2.findAll("a", {"class":"biz-name js-analytics-click"}):
        biz_IDs.append(i['href'])
    
    for i in biz_IDs:
        find_occurences(i, key_wds)





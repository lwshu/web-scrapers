# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 09:32:34 2015

@author: Lingwei
"""

import urllib2
import re
import csv
import math
import string

# read intial html
init_url="http://www.rvtrader.com/dealers?"
init_request = urllib2.Request(init_url)
init_response = urllib2.urlopen(init_request)
init_html=init_response.read()

# crawl url for each State
loca_url_pattern=re.compile('<li><a href="(/dealers.*?)" data-track="state-link-.*?>(.*?)</li>',re.S)
loca_url=re.findall(loca_url_pattern,init_html)

# from the url of each State, crawl the name and address of each dealership
url_base='http://www.rvtrader.com'
len_list=len(loca_url)
dealer_list=[]

for i in xrange(len_list):
    
    # html of each State
    state_url=url_base+loca_url[i][0]
    if ' ' in state_url:
        state_url=string.replace(state_url,' ','%20') #change url into utf-8 form
    state_request=urllib2.Request(state_url)
    state_response=urllib2.urlopen(state_request)
    state_html=state_response.read()
    count=0
    
    if '0 RV dealer results found.' not in state_html: # if no dealership in this state, then skip to the next
        # crawl the first page of dealerships        
        dealer_pattern=re.compile('<h1 class="org">(.*?)</h1>(.*?)<br />(.*?)<span class',re.S)
        result_page=re.findall(dealer_pattern,state_html)
        result_page_num=len(result_page)        
        for j in xrange(result_page_num):
            zip=result_page[j][2].split('&')[0]
            count+=1
            data_row=[result_page[j][0],result_page[j][1]+zip,'RV_FM_'+state_url[-2:]+'_'+str(count)]
            # collect the data for each dealership in the form of (name, address, code)             
            dealer_list.append(data_row)
        # check whether there are more than one page of dealerships in this State
        page_num=int(math.ceil(int(re.findall(r'\d+',loca_url[i][1])[0])/25.0))
        
        if page_num>1: #if there are more than one page, then crawl the rest of pages
            for k in xrange(2,page_num+1):
                url_split=state_url.split('?')
                # construct the url of the next page
                state_url_next=url_split[0]+'?page='+str(k)+'&'+url_split[1]
                state_request_next=urllib2.Request(state_url_next)
                state_response_next=urllib2.urlopen(state_request_next)
                state_html_next=state_response_next.read()
                # crawl the next page
                result_page=re.findall(dealer_pattern,state_html_next)
                result_page_num=len(result_page)
                for j in xrange(result_page_num):
                    zip=result_page[j][2].split('&')[0]
                    count+=1
                    data_row=[result_page[j][0],result_page[j][1]+zip,'RV_FM_'+state_url[-2:]+'_'+str(count)]
                    dealer_list.append(data_row)
    else: 
        continue # if no dealership in this state, then skip to the next

# create CSV
with open('RV_20150928.csv', 'wb') as f:
    writer=csv.writer(f)
    writer.writerows(dealer_list)


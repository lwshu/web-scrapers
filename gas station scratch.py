# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:19:25 2015

@author: Lingwei
"""

import mechanize 
import re
import csv

br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False) 
br.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")] 

r=br.open('http://roadnow.com/gas_interstates.php')

interstate_links=[]
for link in br.links():
    if 'Interstate' in link.text and 'Gas Stations' in link.text:
        interstate_links.append(link)

gas_stations=[]
  
for link in interstate_links:
    request1=br.click_link(link)
    response=br.follow_link(link)
    request2=br.click_link(text_regex='Gas Stations near(.*)')
    br.open(request2)
    html=br.response().read()
    pattern=re.compile('<br/><a name="event\d*"><b>(.*?)</b></a><br/>(.*?),<a href=.*?</a><br/>')
    gas_station=re.findall(pattern,html)
    for station in gas_station:
        data_row=[station[0],station[1],station[1].split(',')[-1]]
        gas_stations.append(data_row)
    
gas_stations.sort(key=lambda tup:tup[2])

gas_stationss=gas_stations[:]

count=1
length=len(gas_stationss)
for i in xrange(length-1):
    if gas_stationss[i][2]==gas_stationss[i+1][2]:
        gas_stationss[i][2]='GASSTATION_'+gas_stationss[i][2]+'_'+str(count)
        count+=1
    else:
        gas_stationss[i][2]='GASSTATION_'+gas_stationss[i][2]+'_'+str(count)
        count=1
        
# create CSV
with open('gasstation_20151019.csv', 'wb') as f:
    writer=csv.writer(f)
    writer.writerows(gas_stationss)
        

        
    
    
    
        
    
    
'''
first things first, import the python modules we'll need, listed in the order you'll need them'''

import os
import time
import re
import urllib2

from bs4 import BeautifulSoup

'''go through each of the volumes in a collection, click the plain text link and scrape it'''

# defines a function to get ocr based on one argument, a collection url
def get_volume_ocr(collection_url):

    collection = urllib2.urlopen(collection_url).read()
    collection_soup = BeautifulSoup(collection)
    
    full_text_urls = collection_soup.find_all('a', {'class': 'fulltext icomoon-document-2'})
    
    volume_urls = []
    for full_text_url in full_text_urls:
        volume_url = 'https://babel.hathitrust.org' + full_text_url['href']
        volume_urls.append(volume_url)

    '''get the volume id and store that as a variable, because we'll use it later'''
    
    for volume_url in volume_urls:
        item_id_string = volume_url.split("=")[-1]

        '''go to each volume url and figure out how many pages it has'''
        
        volume = urllib2.urlopen(volume_url).read()
        volume_soup = BeautifulSoup(volume)
        
        action_go_last = volume_soup.find('a', {'id': 'action-go-last'})
       
        action_go_last_url = action_go_last['href']
        page_count = int(re.search(r'seq=(\d{1,4})', action_go_last_url).group(1))

        '''output the ocr to text file for each volume'''
        # then we'll go through each page (and eventually adding one to go to the next one), as long as the number of the pages we're on is less than or equal to the total number of pages
        for page in range(1, page_count + 1):
            if page == 10:
                break
            while True:
                try:
                    ocr_url = 'https://babel.hathitrust.org/cgi/pt?id=' + item_id_string + ';view=plaintext;seq=' + str(page)
                    ocr = urllib2.urlopen(ocr_url).read()
                    ocr_soup = BeautifulSoup(ocr)
                    page_item_page_text = ocr_soup.find('div', {'class': 'page-item page-text'})
                    if page_item_page_text is not None:
                        page_item_page_text = re.sub(r'<(.*)?>', '', str(page_item_page_text))
                        print page_item_page_text

                        output_filename = os.path.join('ocr', "{0}.txt".format(item_id_string))
                        with open(output_filename, mode='a') as text_file:
                            text_file.write("\n" + page_item_page_text)
                    time.sleep(1)
                except:
                    time.sleep(10)
                    continue

                break
            

# to run this, change 'https://babel.hathitrust.org/cgi/mb?a=listis;c=397666231;sort=title_a;pn=1;sz=50' to the url for your collection (you can also change the variable name if you like)
michigan_technic = 'https://babel.hathitrust.org/cgi/mb?c=1974496242;a=listis;sort=title_a;pn=1'

# run it!
get_volume_ocr(michigan_technic)

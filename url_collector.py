#!/usr/bin/env python3

import sys
import re
import requests
import time
import random
import argparse
from bs4 import BeautifulSoup

pure_value = {}
session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

def url_duplicate_check(save_file):
    url_list = []
    for url in open(save_file).readlines():
        url_list.append(url)

    url_list = set(url_list)
    write_file = open(save_file,'w')

    for url in url_list:
        write_file.write(url)
    write_file.close()

def url_collect(save_file):
    try:
        r = session.get('http://tor66sezptuu2nta.onion/random')
    except Exception as err:
        print (err)
        return

    html = r.text
    soup = BeautifulSoup(html,'lxml')
    data = soup.find_all('td')

    with open(save_file,'a') as save_file:
        for idx in data:
            seq = idx.find_all('a')
            for contents in seq:
                url = str(contents['href'])
                print (url)
                #url = re.sub('https?://','',str(contents['href']))
                #description = contents['data-tooltip']
                save_file.write(url+'\n')
                #save_file.write(url.ljust(80) + description + "\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collecting URLs for DarkWeb Data Analyzer.')
    parser.add_argument('-o', '--output', required=True, help='input the URL list file to save.')
    args = parser.parse_args()

    save_file = args.output 

    while True:
        try:
            url_collect(save_file)
            url_duplicate_check(save_file)
            #time.sleep(random.randrange(10,40))

        except Exception as err:
            pass
        
        except KeyboardInterrupt as KbdIrpt:
            print('\n\033[33mThe total number of URLs collected so far is ' + str(len(open(save_file).readlines())) + '\033[0m')
            sys.exit(0)


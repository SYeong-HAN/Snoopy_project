#!/usr/bin/env python3
import re
import requests
import time
import random
import sys
import argparse
from bs4 import BeautifulSoup

timeout = 10
session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

collect_filter1 = re.compile(r'^https?')
collect_filter2 = re.compile(r'mailto:?')
collect_filter3 = re.compile(r'javascript:?')
collect_filter4 = re.compile(r'\w+.php\w+')
collect_filter5 = re.compile(r'pdf$|zip$|7z$|jpg$|jpeg$|png$')

def find_sub(target_url, cnt):
    try:
        r = session.get(target_url,timeout = timeout)
    except Exception as err:
        return 
    
    proceed_percent = (cnt/file_line_cnt)*100
    info = "\033[42m" + target_url + "\033[0m"
    print(info.ljust(80) + str(round(proceed_percent,2)) + "%  " + "(" + str(cnt) + " of " + str(file_line_cnt) + ")")
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    class_title_a_list = soup.select('a')
    sub_list = []
    written_results.write(str(target_url)+"\n")
    
    for a in class_title_a_list:
        a_href = str(a.get('href')).strip()
    
        if len(a_href) == 0 or collect_filter2.search(a_href) or collect_filter3.search(a_href) or collect_filter5.search(a_href):
            continue 
        elif collect_filter1.search(a_href):
            if '.onion' not in a_href:
                continue
            result = a_href
            sub_list.append(result)
            continue
        elif a_href[0] == '.':
            a_href = a_href.replace(a_href[0],'',1)
            a_href =  '/' + a_href
        elif a_href[0] != '/':
            a_href = '/' + a_href

        if collect_filter4.search(a_href):
            a_href = a_href.replace('.php','.php?',1)
        
        result = target_url + a_href 
        sub_list.append(result)

    sub_list = set(sub_list)
    print('\n' .join(sub_list))
    
    for idx in sub_list:
        written_results.write(str(idx)+"\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collecting Subpage from URLs File to File.')
    parser.add_argument('-i', '--input', required=True, help='input the URL list file.')
    parser.add_argument('-o', '--output', required=True, help='Output file to save SubPage.')
    args = parser.parse_args()
    
    url_list = args.input
    subpage_file = args.output

    try:
        written_results = open(subpage_file,'a')
        file_line_cnt = len(open(url_list,'r').readlines())
        current_line_cnt = 1
        with open(url_list,'r') as f:
            for idx in f:
                target_url = str(idx[:-1])
                find_sub(target_url, current_line_cnt)
                time.sleep(random.randrange(1,3))
                current_line_cnt = current_line_cnt + 1
        written_results.close()
    except KeyboardInterrupt as err:
        written_results.close()
        sys.exit()


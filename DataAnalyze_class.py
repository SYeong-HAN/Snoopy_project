#-*- coding:utf-8 -*-
import os
import sys
import re
import requests
import subprocess
import os
import json
import time
from bs4 import BeautifulSoup

current_dir_path = os.path.dirname(os.path.realpath(__file__))
keywords_dir_path = current_dir_path + '/keywords'
reports_dir_path = current_dir_path + '/reports'
timeout = 10
session = requests.session()

current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

class DataAnalyze:
    def __init__(self):
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
        self.userChoiceKeywords = ""
        self.html_language = ""
        self.contents_1 = ""
        self.contents_2 = ""

    def KeywordsList(self):
        keywords_value = {}
        keywords_value[1] = '/hack_keywords.txt'
        keywords_value[2] = '/porn_keywords.txt'
        keywords_value[3] = '/murder_keywords.txt'
        keywords_value[4] = '/drug_keywords.txt'

        print('\nThe following keywords are available..\n')
        for no, idx in enumerate(keywords_value.values(), 1):
            idx = idx.split('_')[0]
            print('\t',str(no)+'.',idx[1:])

        choice_num = int(input('\nSelect Keyword Number : '))
        align_cnt = 1
        with open(keywords_dir_path + keywords_value.get(choice_num), 'r') as keyword:
            self.userChoiceKeywords = keywords_dir_path + keywords_value.get(choice_num)
            print('\nselected keywords are as follow : \n')
            for idx in keyword:
                idx = idx[:-1]
                print(idx.ljust(12), end=' | ')
                if align_cnt % 10 == 0: print(' ')
                align_cnt = align_cnt + 1
            print('\n')

    def ExtractContents(self, target_url, current_cnt, total_cnt):
        dark_data = {}
        temp_dict = {}
        sub_list = []
        descripts = "None"
        lang = "None"
        titles="None"
        process_flow_info = "\033[42m" + target_url + "\033[0m"
        process_percent = (current_cnt / total_cnt) * 100

        try:
            r = session.get(target_url, timeout = timeout)
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
        except Exception as err:
            print(process_flow_info.ljust(80) + str(round(process_percent,2)) + "% " + "(" + str(current_cnt) + " of " + str(total_cnt) + ")")
            print('\033[31mNot Connected.\033[0m')
            return

        try:
            descripts = soup.find("meta", {"name" : "description"}).get("content")
            lang = soup.html['lang']
            titles = soup.title.string.decode('utf8')
        except Exception:
            pass

        contents = soup.find_all('p')
        data_list = []

        for data in contents:
            if 'Your browser has JavaScript disabled.' in data.text: continue
            else: data_list.append(data.text.strip())

        if len(data_list) != 0:
            data_list = ' '.join(data_list)
            flag = 0
            for keyword in open(self.userChoiceKeywords, 'r').readlines():
                contents_filter = r'\b' + re.escape(keyword[:-1])
                collect_filter = re.compile(contents_filter)

                if collect_filter.search(data_list):
                    flag = 1
                    print(process_flow_info.ljust(80) + str(round(process_percent,2)) + "% " + "(" + str(current_cnt) + " of " + str(total_cnt) + ")")
                    print('-'*50)
                    print('\033[35m' + '<' + str(keyword[:-1] + '>' + '\033[0m'))
                    print(data_list)
                    temp_dict[target_url] = {'title_' : titles, 'keywords_' : str(keyword[:-1]), 'descript_' : descripts, 'timestamp' : current_time, 'lang_' : lang, 'contents_' : data_list}
                    dark_dict_ = dict(**temp_dict)
                    with open(os.path.join(reports_dir_path, current_time + '.json'), 'a+', encoding='UTF8') as json_file:
                        json.dump(dark_dict_, json_file, indent='\t', ensure_ascii=False)
                    print('-'*50)


            if flag == 0:
                print(process_flow_info.ljust(80) + str(round(process_percent,2)) + "% " + "(" + str(current_cnt) + " of " + str(total_cnt) + ")")
                print('\033[31mNothing Matched.\033[0m')
                return

        else:
            print(process_flow_info.ljust(80) + str(round(process_percent,2)) + "% " + "(" + str(current_cnt) + " of " + str(total_cnt) + ")")
            print('\033[31mNothing Matched.\033[0m')
            return

    def FindKorSite(self, target_url):
        try:
            r = session.get(target_url, timeout = timeout)
            html = r.text
            soup = BeautifulSoup(html, 'lxml')

            for idx in range(1,7,1):
                h = ("h" + str(idx))
                h_tag = soup.select(h)

                for h_t in h_tag:
                    title_tag = soup.select('title')
                    for t_t in title_tag:
                        korean = re.compile('[^\u3131-\u3163\uac00-\ud7a3]+')
                        self.contents_1 = korean.sub('', t_t.text)
                        self.contents_2 = korean.sub('', h_t.text)
                        self.html_language = soup.select('html[lang=ko]')

            if bool(self.html_language) or bool(self.contents_1) or bool(self.contents_2):
                print(target_url.ljust(70) + "[" + "\033[32mMatched\033[0m" + "]")
                print(t_t.text)
            else: print(target_url.ljust(70) + "[" + "\033[31mNot Matched\033[0m" + "]")

        except Exception as err:
            print(target_url.ljust(70) + "[" + "\033[31mNot Connected\033[0m" + "]")
            return

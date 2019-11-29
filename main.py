#!/usr/bin/env python3

import sys
import os
import getopt
import re
import requests
import subprocess
import argparse
import DataAnalyze_class
from bs4 import BeautifulSoup

url_check_rule = re.compile('^https?')
current_dir_path = os.path.dirname(os.path.realpath(__file__))
keywords_dir_path = current_dir_path + '/keywords'
reports_dir_path = current_dir_path + '/reports'

menu_instruction = [ 'Extract contents based on keywords.',
                     'Extract Korean DarkWeb URL.',
                     'Exit' ]

class Start:
    def __init__(self, target_url_list):
        self.url = target_url_list

    def url_format_check(self):
        for url in open(self.url,'r').readlines():
            if not url_check_rule.search(url):
                print(url[:-1])
                print('URL list file components must be URL format... ex) https://jgeklfjdhwasd.onion/~~~')
                sys.exit()

    def banner(self):
        print('\033[36m')
        print('*-----------*-----------*----------------------*-----------*-----------*')
        print('|   ____             _                  _       ____        _          |')
        print('|  |  _ \  __ _ _ __| | ____      _____| |__   |  _ \  __ _| |_ __ _   |')
        print('|  | | | |/ _` |  __| |/ /\ \ /\ / / _ \  _ \  | | | |/ _` | __/ _` |  |')
        print('|  | |_| | (_| | |  |   <  \ V  V /  __/ |_) | | |_| | (_| | || (_| |  |')
        print('|  |____/ \__,_|_|  |_|\_\  \_/\_/ \___|_.__/  |____/ \__,_|\__\__,_|  |')
        print('|      _                _                                              |')
        print('|     / \   _ __   __ _| |_   _ _______ _ __                           |') 
        print('|    / _ \ |  _ \ / _` | | | | |_  / _ \  __|                          |')
        print('|   / ___ \| | | | (_| | | |_| |/ /  __/ |                             |')
        print('|  /_/   \_\_| |_|\__,_|_|\__, /___\___|_|     - made by Snoopy Team   |') 
        print('|                         |___/                                        |')
        print('*-----------*-----------*----------------------*-----------*-----------*')
        print('\nWelcome to our DarkWeb Data Analyzer v.0.0')
        print('DarkWeb Data Analyzer is a program that lets cyber investigators search and collect analyzed data from the Darkweb.\n')
        print('\t\t\t\t\033[33m',str(len(open(target_list,'r').readlines())),'DarkWeb URLs are all set.\033[0m')

    def OptionFunc(self, opt):
        if opt == '1':
            data_analyze.KeywordsList()
            current_url_no = 1
            url_total_cnt = len(open(target_list, 'r').readlines())
            for url in open(target_list,'r').readlines():
                data_analyze.ExtractContents(url[:-1], current_url_no, url_total_cnt)
                current_url_no = current_url_no + 1
            sys.exit(0)
        elif opt == '2':
            print('\n\033[33mFinding Korean URL. . .\033[0m\n')
            for url in open(target_list,'r').readlines():
                    data_analyze.FindKorSite(url[:-1])
            sys.exit(0)
        elif opt == '3':
            sys.exit(0)
        else:
            print('Invalid Option.')
            return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DarkWeb Data Analyzer using Cybercrime keywords.')
    parser.add_argument('-i', '--input' , required=True, help='input URLs list file.')
    args = parser.parse_args()
    
    target_list = args.input

    try:
        start = Start(target_list)
        start.url_format_check()
        start.banner()
        data_analyze = DataAnalyze_class.DataAnalyze()

        print('-'*24)
        print(' Menu list given below.')
        print('-'*24,'\n')

        for no, contents in enumerate(menu_instruction, 1):
            print ('\t',str(no)+'.',contents)

        while True:
            opt = input("\nSelect Option number : ")
            start.OptionFunc(opt)
    except KeyboardInterrupt as err:
        sys.exit(1)

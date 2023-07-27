import csv
import difflib
import urllib.parse
import re
from file_to_set import *
from comparison_prints import *

# to run, enter at the prompt: `python3 comparison.py`

suf = '../scrapy_urls/' # suf is short for scrapy_urls_folder 
scUf = '../scrutiny_urls/processed' # scUf is short for scrutiny_urls_folder

scrapy_paths = [suf + '/test.csv', 
               suf + '/armymwr_urls.csv', 
               suf + '/get_smart_about_drugs_urls.csv', 
               suf + '/james_webb_urls.csv',
               suf + '/travel_dod_mil_urls.csv',
               suf + '/veteran_affair_urls.csv']
scrutiny_paths = [scUf + '/test.txt',
                scUf + '/armymwr.txt', 
                scUf + '/get_smart_about_drugs.txt', 
                scUf + '/james_webb.txt',
                scUf + '/travel_dod_mil.txt',
                scUf + '/veteran_affairs.txt']
text_gaps = ['test',
             'armymwr',
             'get smart about drugs',
             'james webb',
             'travel.dod.mil',
             'veteran_affairs'
             ]

with open("results.txt", "w") as file:
    for i in range(0, len(scrapy_paths)):
        scrapy_urls = csv_to_set(scrapy_paths[i])
        scrutiny_urls = txt_to_set(scrutiny_paths[i])
        print('___________________________________________\n' + text_gaps[i] + ' results:')
        make_comparisons(scrapy_urls, scrutiny_urls)





import csv
import difflib
import urllib.parse
import re

def csv_to_set(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        url_list = list(reader)
        url_list = list(map(''.join, url_list))
    f.close()
    url_set = set(url_list)
    return url_set

def txt_to_set(file_path):
    with open(file_path, 'r') as f:
       url_list = f.readlines()
       url_list = list(map(''.join, url_list))
    f.close()
    fixed_urls = []
    for url in url_list:
        fixed_urls.append(re.sub("\n", "", url))
    url_set = set(fixed_urls)
    return url_set

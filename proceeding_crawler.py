import os
import requests
import argparse
import re
from crawler import abstract

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def crawl_abstrct(url):
    print("Loading abstract...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    abstract = soup.find(class_='Abstract').find_all(class_='Para')
    return '\n'.join([str(p) for p in abstract])

def crawl(url, savedir):
    domain = urlparse(url).netloc

    print("Loading main page...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    md = "# Abstract from [Conference]\n"

    maxpage = int(soup.find(class_='test-maxpagenum').text)
    for page in range(1, maxpage+1):
        print("Loading page {0}/{1}...".format(page, maxpage))
        response = requests.get(url + '?page={}'.format(page))
        soup = BeautifulSoup(response.text, 'lxml')
        
        papers = soup.find_all(class_='chapter-item')
        for i, paper in enumerate(papers):
            print("page {0} paper {1}/{2}".format(page, i, len(papers)))

            title = paper.find(class_='content-type-list__link')
            author = paper.find(class_='content-type-list__text')
            abstract = crawl_abstrct(urljoin('https://' + domain, title.get('href')))

            md += "## " + title.text + "\n"
            md += "- Authors: {}\n".format(author.text)
            md += "- Abstract: {}\n".format(abstract)
            md += "\n"

    
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    
    with open(os.path.join(savedir, 'abstract.md'), 'w', encoding='utf-8') as f:
        f.write(md)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download papers from Springer proceedings.')
    # parser.add_argument('command', type=str,
    #                     help='"crawl" for crawling all papers from the site; "download" for downloading all papers crawled; "abstract" for generating abstract for all papers crawled')
    parser.add_argument('--url', type=str, default=None,
                        help='the url to the accepted papers panel from the site')
    # parser.add_argument('--skip', action="store_true",
    #                     help='skip download and abstract generation if this arg is presented')
    # parser.add_argument('--skip_download', action="store_true",
    #                     help='skip download if this arg is presented')
    # parser.add_argument('--skip_abstract', action="store_true",
    #                     help='skip abstract generation if this arg is presented')
    parser.add_argument('--savedir', type=str, default='.',
                        help='the directory to save all papers')
    # parser.add_argument('--maxcount', type=int, default=-1,
    #                     help="maximum number of papers to crawl")
    
    args = parser.parse_args()
    
    crawl(args.url, args.savedir)
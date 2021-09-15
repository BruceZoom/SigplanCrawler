import os
import requests
import argparse
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def crawl(url, savedir=".", maxcount=-1):
    if not os.path.exists(savedir):
        print("Creating directory")
        os.makedirs(savedir)

    print("Crawling")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    papers = soup.find(id="event-overview").table.find_all('tr')[1:]
    
    df = pd.DataFrame(columns=('title', 'link', 'media', 'pre-print'))

    for idx, paper in enumerate(papers):
        if (idx == maxcount):
            print("Terminating")
            break

        print("{0}/{1}".format(idx, len(papers)))
        content = paper.contents[1]

        title = content.a.text.translate({ord(i): None for i in '\/:*?"<>|'})

        links = content.find_all(class_="publication-link navigate")

        source = [link for link in links if 'Link' in link.text]
        if len(source) > 0: source = source[0]['href']
        else: source = None

        media = [link for link in links if 'Media' in link.text]
        if len(media) > 0: media = media[0]['href']
        else: media = None

        pprint = [link for link in links if 'Pre-print' in link.text]
        if len(pprint) > 0: pprint = pprint[0]['href']
        else: pprint = None

        df.loc[-1] = [title, source, media, pprint]
        df.index = df.index + 1
        # df = df.append(pd.DataFrame({'title': title, 'link': source, 'media': media}))

    df.to_csv(os.path.join(savedir, 'paper_links.csv'), index=False)

    return df


def download(df, savedir='.'):
    if not os.path.exists(savedir):
        print("Creating directory")
        os.makedirs(savedir)

    print("Downloading")
    for i in range(df.shape[0]):
        print("{0}/{1}".format(i, df.shape[0]))
        title = df.iloc[i]['title']
        source = df.iloc[i]['link']
        pprint = df.iloc[i]['pre-print']

        if source is not np.nan and source is not None:
            fname = os.path.join(savedir, title + ".pdf")
            print(source + "   ===>>>   " + fname)
            try:
                response = requests.get(source) 
                with open(fname, "wb") as pdf:
                    pdf.write(response.content)
            except Exception as e:
                print(e)
        
        if pprint is not np.nan and pprint is not None:
            fname = os.path.join(savedir, "[preprint]" + title + ".pdf")
            print(pprint + "   ===>>>   " + fname)
            try:
                response = requests.get(pprint) 
                with open(fname, "wb") as pdf:
                    pdf.write(response.content)
            except Exception as e:
                print(e)


def abstract(df, savedir='.'):
    if not os.path.exists(savedir):
        print("Creating directory")
        os.makedirs(savedir)

    print("Generating Abstract")
    md = "# Abstract from [Conference]\n"
    for i in range(df.shape[0]):
        print("{0}/{1}".format(i, df.shape[0]))
        title = df.iloc[i]['title']
        source = df.iloc[i]['link']
        media = df.iloc[i]['media']
        pprint = df.iloc[i]['pre-print']

        md += "## " + title + "\n"
        if source is np.nan or source is None:
            md += "- Paper Link: None\n"
        else:
            md += "- Paper Link: {}\n".format(source)
        
        if pprint is np.nan or pprint is None:
            md += "- Pre-print Link: None\n"
        else:
            md += "- Pre-print Link: {}\n".format(source)

        if media is np.nan or media is None:
            md += "- Abstract: None\n"
        else:
            response = requests.get(media)
            soup = BeautifulSoup(response.text, 'lxml')
            abstract = soup.find('label', text=re.compile('Abstract')).parent
            md += "- Abstract: {}\n".format(''.join([str(p) for p in abstract.find_all('p')]))
        
        md += "\n"
    
    print("Saving Abstract")
    with open(os.path.join(savedir, 'abstract.md'), 'w', encoding='utf-8') as f:
        f.write(md)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download papers from sigplan site.')
    parser.add_argument('command', type=str,
                        help='"crawl" for crawling all papers from the site; "download" for downloading all papers crawled; "abstract" for generating abstract for all papers crawled')
    parser.add_argument('--url', type=str, default=None,
                        help='the url to the accepted papers panel from the site')
    parser.add_argument('--skip', action="store_true",
                        help='skip download and abstract generation if this arg is presented')
    parser.add_argument('--skip_download', action="store_true",
                        help='skip download if this arg is presented')
    parser.add_argument('--skip_abstract', action="store_true",
                        help='skip abstract generation if this arg is presented')
    parser.add_argument('--savedir', type=str, default='.',
                        help='the directory to save all papers')
    parser.add_argument('--maxcount', type=int, default=-1,
                        help="maximum number of papers to crawl")
    
    args = parser.parse_args()
    
    if args.command == "crawl":
        df = crawl(args.url, args.savedir, args.maxcount)
        if not args.skip:
            if not args.skip_abstract:
                abstract(df, args.savedir)
            if not args.skip_download:
                download(df, args.savedir)
    elif args.command == "download":
        df = pd.read_csv(os.path.join(args.savedir, 'paper_links.csv'))
        download(df, args.savedir)
    elif args.command == "abstract":
        df = pd.read_csv(os.path.join(args.savedir, 'paper_links.csv'))
        abstract(df, args.savedir)
    else:
        print("Unkwon Command")

# SigplanCrawler
For crawling papers from sigplan conferences.

# Requirements
Python 3, BeautifulSoup4

# Usage
The crawler has three command: "crawl", "download", and "abstract".
```
usage: crawler.py [-h] [--url URL] [--skip] [--skip_download]
                  [--skip_abstract] [--savedir SAVEDIR] [--maxcount MAXCOUNT]
                  command

Download papers from sigplan site.

positional arguments:
  command              "crawl" for crawling all papers from the site;
                       "download" for downloading all papers crawled;
                       "abstract" for generating abstract for all papers
                       crawled

optional arguments:
  -h, --help           show this help message and exit
  --url URL            the url to the accepted papers panel from the site
  --skip               skip download and abstract generation if this arg is
                       presented
  --skip_download      skip download if this arg is presented
  --skip_abstract      skip abstract generation if this arg is presented
  --savedir SAVEDIR    the directory to save all papers
  --maxcount MAXCOUNT  maximum number of papers to crawl
```

For all commands, the `--savedir` argument is always suggetted to be specified to organize papers from different conferences.

Command "crawl" will scan through accepted papers from the site and download their basic information into "<savedir>/paper_links.csv", and it then download all papers, if they exist, into the savedir and generates a summary of all papers' abstracts in "<savedir>/abstract.md".
  
Use `--url` to specify the page of accepted papers, e.g., "https://popl19.sigplan.org/track/POPL-2019-Research-Papers?#event-overview" for POPL 2019.

Use `--skip`, `--skip_download`, and `--skip_abstract` to skip the download sequence, or the abstract generation, or both process in this command.

Use `--maxcount` to limit the maximum number of papers to crawl.

You may skip both process in "crawl" mode, and use "download" and "abstract" command to continue download and abstract generation separately.
You need to specify `--savedir` as the directory "crawl" uses to save file "paper_links.csv".



# wordgrabber

This script finds a list of words from a website that can be used to create a customized wordlist used for bruteforcing.
The script needs a list of URL's to scrape from and a crawler is not added on purpose. You can use Burp suite or ZAP proxy or whatever to crawl and then export the list of URL's to a file which can be used by this script.

It is written in Python 3.x and is a minimal port of https://github.com/SmeegeSec/SmeegeScrape

Usage and options:

python wordgrabber.py -l "d:\url list.txt"

It is mandatory that a list of URL's to be scraped is fed to the script

Other options:

-o : Name of the output file you want
-min: Minimum characters in a word to be scraped
-max: Max characters in a word to be scraped


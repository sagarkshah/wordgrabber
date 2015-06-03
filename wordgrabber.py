__author__ = 'Sagar Shah'

import argparse
import os
import re
import requests
from collections import OrderedDict
from bs4 import BeautifulSoup

title = "Written by Sagar"
print(title)
parser = argparse.ArgumentParser(description=title, formatter_class=argparse.RawTextHelpFormatter)

operationGroup = parser.add_mutually_exclusive_group(required=True)
operationGroup.add_argument('-l', action="store", dest="webList",
                            help="Specify a text file with a list of URLs to scrape (separated by newline).")

optionGroup = parser.add_argument_group('paramters and options')
optionGroup.add_argument('-o', action="store", dest="outputFile",
                         help="Output filename. (Default: wordlist.txt)")
optionGroup.add_argument('-min', action="store", dest="minLength", type=int,
                         help="Set the minimum number of characters for each word (Default: 3).")
optionGroup.add_argument('-max', action="store", dest="maxLength", type=int,
                         help="Set the maximum number of characters for each word (Default: 30).")

args = parser.parse_args()



def webUrl(fullUrl):
    # URL validation
    validUrl = re.compile(
        r'^(?:http)s?://|'  # http:// or https://
        r'^(?:http)s?://www.'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if validUrl.match(fullUrl):
        try:
            u = requests.get(fullUrl)
            html = u.content.decode('utf-8')
            soup = BeautifulSoup(html)
            tokens = soup.get_text().strip()
            tokens = tokens.split(" ")

            for token in tokens:
                if len(token) > minl or len(token) < maxl:
                    if not token in wordList:
                        token = token.strip('\t')
                        token = token.strip('\n')
                        wordList.append(token)

            print("Scraped URL - {0}".format(fullUrl))
        except Exception as e:
            print('There was an error connecting to or parsing {0}'.format(fullUrl))
            print('Error: %s' % e)
    else:
        print('INVALID URL - {0}. Format must be http(s)://www.google.com.'.format(fullUrl))


def webList(webListFile):
    if os.path.isfile(webListFile):
        with open(webListFile) as f:
            webList = f.readlines()

        for url in webList:
            webUrl(url.rstrip('\n'))

        f.close()
    else:
        print('Error opening file')


def output():
    try:
        if not args.outputFile:
            args.outputFile = 'wordlist.txt'
        outputFile = open(args.outputFile, 'w', encoding='utf-8')
        wordListFinal = OrderedDict.fromkeys(wordList).keys()

        for word in wordListFinal:
            outputFile.write(word)
            outputFile.write('\n')
        outputFile.close()

        print('\n{0} unique words have been scraped.'.format(len(wordListFinal)))
        print ('Output file successfully written: {0}'.format(outputFile.name))
    except Exception as e:
        print('Error creating output file: {0}'.format(outputFile.name))
        print(e)


if __name__ == '__main__':

    wordList = list()
    charBlacklist = ""

    if args.minLength or args.maxLength:
        minl = args.minLength if args.minLength else 3
        maxl = args.maxLength if args.maxLength else 30
        if minl > maxl:
            print('Argument minLength cannot be greater than maxLength. Setting defaults to min=3 max=30.')
            minl = 3
            maxl = 15

    charBlacklist = ""

    if args.webList:
        webList(args.webList)
    output()
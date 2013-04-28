#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import random
from bs4 import BeautifulSoup
import urllib.parse
import re

browsers = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121621 Ubuntu/8.04 (hardy) Firefox/3.0.5',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            ]

def download(url):
    if (len(url) < 3):
        return None
    headers = {
        'User-Agent': browsers[random.randint(0, len(browsers) - 1)],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5'
    }
    try:
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request, timeout = 5)
        data = response.read()
        return data
    except:
        pass
        return None

class google:
    SEARCH_URL = "http://www.google.%(tld)s/search?hl=%(lang)s&newwindow=1&output=search&sclient=psy-ab&q=%(query)s"
    NEXT_PAGE = "http://www.google.%(tld)s/search?hl=%(lang)s&newwindow=1&q=%(query)s&start=%(start)d&sa=N"
    
    def __init__(self, query, lang="en", tld="com"):
        self.query = query
        self.lang = lang
        self.tld = tld
        self.num = 10
    
    def __fetch_page(self, page):
        pattern = google.SEARCH_URL
        if page > 0:
            pattern = google.NEXT_PAGE
        
        url = pattern % {
               'query': urllib.parse.quote_plus(self.query),
               'start': page * self.num,
               'tld' : self.tld,
                'lang' : self.lang
        }
        
        return download(url)
    
    def get_results(self, page):
        text = self.__fetch_page(page)
        soup = BeautifulSoup(text)
        
        res = []
        results = soup.findAll('li', {'class': 'g'})
        
        for result in results:
            try:
                a = result.find('a')
                name = a.text
                match = re.match(r'/url\?q=(http[^&]+)&', a['href'])
                url = urllib.parse.unquote(match.group(1))
                res.append({"name" : name, "url" : url})
            except:
                pass
                continue
        
        return res
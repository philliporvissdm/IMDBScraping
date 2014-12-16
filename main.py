"""
Scrape info from www.imdb.com
"""

__author__ = 'Phillip Orviss'

from bs4 import BeautifulSoup
import mechanize
import cookielib
import re

"""Create browser instance"""

def instantiatebrowser():
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    return br

browser = instantiatebrowser()
browser.open('http://www.imdb.com')

browser.select_form(nr=0)
browser.form['q'] = 'age of dragons'
browser.submit()

soup = BeautifulSoup(browser.response().read())

titles_div = soup.find_all('td', {'class':'result_text'})

linkList = []


for link in titles_div:
    if link.find('a',{'href':re.compile('^/title/.*tt_.*$')}) is not None:
        linkList.append('http://www.imdb.com'+link.find('a',{'href':re.compile('^/title/.*tt_.*$')})['href'])

movie_list = []

for link in linkList:
    browser.open(link)
    soup = BeautifulSoup(browser.response().read())
    title = soup.find('span', {'itemprop':'name'}).text
    try:
        rel_date = soup.find('meta', {'itemprop':'datePublished'})['content']
    except:
        rel_date = 'Unknown'
    resultSet = {'title':title, 'release date':rel_date}
    movie_list.append(dict(resultSet))

print movie_list

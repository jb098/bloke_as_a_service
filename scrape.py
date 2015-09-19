from bs4 import BeautifulSoup
import requests

football_page_url = 'http://www.bbc.co.uk/sport/0/football/'
football_page = requests.get(football_page_url)
football_soup = BeautifulSoup(football_page.text)

live_link = [a for heading in football_soup.findAll('h2', attrs={'class':'headline-live'}) for a in heading][1].attrs['href']
live_page_url = 'http://www.bbc.co.uk/%s' % (live_link,)
live_page = requests.get(live_page_url)
live_soup = BeautifulSoup(live_page.text)

paragraphs = [p.text.replace('"', '').replace('Â', '') for p in live_soup.findAll('p') if '"' in p.text]

with open("quotes.txt", 'a') as quotes:
    for p in paragraphs:
        quotes.write(p+"\n")

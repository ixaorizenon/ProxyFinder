import urllib.parse
import urllib.request
import os
import re
import threading

class Anonymous(object):
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.16) Gecko/20080702 Firefox/2.0.0.16',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; WOW64; rv:2.0) Gecko/20100101 Firefox/4.0',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0) Gecko/20100101 Firefox/7.0',
            'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0',
            'Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0',
            'Mozilla/5.0 (Windows NT 6.1; Trident/5.0; rv:11.0) like Gecko'
        ]

    def random_agent(self):
        import random
        return random.choice(self.user_agents)

    def request(self, url):
        headers = {'User-Agent': self.random_agent()}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_proxies(self, url):
        html = self.request(url)
        if not html:
            return []
        proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', html)
        return proxies

    def write_proxies_to_file(self, proxies, filename='proxy.txt'):
        with open(filename, 'w') as file:
            for proxy in proxies:
                file.write(f"{proxy}\n")

    def fetch_and_save_proxies(self, urls):
        all_proxies = []
        for url in urls:
            print(f"Scraping proxies from {url}")
            proxies = self.scrape_proxies(url)
            if proxies:
                all_proxies.extend(proxies)
        self.write_proxies_to_file(all_proxies)
        print(f"Saved {len(all_proxies)} proxies to file.")

def main():
    urls = [
        'http://www.sslproxies.org',
        'https://www.proxy-list.download/HTTPS',
        'http://free-proxy-list.net',
        'http://www.us-proxy.org'
    ]

    anon = Anonymous()
    anon.fetch_and_save_proxies(urls)

if __name__ == '__main__':
    main()

from datetime import datetime
import threading
import sys
import os
import pickle
import re

import requests
from bs4 import BeautifulSoup

# Import parent class
from .FomcBase import FomcBase

class FomcStatement(FomcBase):
    '''
    A convenient class for extracting statements from the FOMC website
    Example Usage:  
        fomc = FomcStatement()
        df = fomc.get_contents()
    '''
    def __init__(self, verbose=True, max_threads=10, base_dir='../data/FOMC/'):
        super().__init__('statement', verbose, max_threads, base_dir)

    def _get_links(self, from_year):
        '''Override to set all statement links.'''
        self.links = []
        self.titles = []
        self.speakers = []
        self.dates = []

        # Current statements on calendar page
        r = requests.get(self.calendar_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        if self.verbose:
            print("Getting links for statements from calendar...")
        contents = soup.find_all('a', href=re.compile(r'^/newsevents/pressreleases/monetary\d{8}[ax]\.htm'))
        for a in contents:
            href = a['href']
            self.links.append(href)
            self.titles.append('FOMC Statement')
            dt = self._date_from_link(href)
            self.dates.append(datetime.strptime(dt, '%Y-%m-%d'))
            self.speakers.append(self._speaker_from_date(dt))
        if self.verbose:
            print(f"  → Found {len(self.links)} current statements.")

        # Archived statements before 2015
        if from_year <= 2014:
            if self.verbose:
                print("Getting links from archive pages...")
            for year in range(from_year, 2015):
                url = self.base_url + f"/monetarypolicy/fomchistorical{year}.htm"
                r_year = requests.get(url)
                soup_year = BeautifulSoup(r_year.text, 'html.parser')
                yearly = soup_year.find_all('a', string=re.compile(r'^Statement$', re.I))
                for a in yearly:
                    href = a['href']
                    self.links.append(href)
                    self.titles.append('FOMC Statement')
                    dt = self._date_from_link(href)
                    dtdt = datetime.strptime(dt, '%Y-%m-%d')
                    # Correct known mismatches
                    corrections = {
                        datetime(2007,6,18): datetime(2007,6,28),
                        datetime(2007,8,17): datetime(2007,8,16),
                        datetime(2008,1,22): datetime(2008,1,21),
                        datetime(2008,3,11): datetime(2008,3,10),
                        datetime(2008,10,8): datetime(2008,10,7)
                    }
                    self.dates.append(corrections.get(dtdt, dtdt))
                    self.speakers.append(self._speaker_from_date(dt))
                if self.verbose:
                    print(f"  → {year}: found {len(yearly)} archived statements.")
        if self.verbose:
            print(f"Total statement links: {len(self.links)}")

    def _add_article(self, link, index=None):
        '''Fetch and store one statement's text.'''  
        if self.verbose:
            sys.stdout.write('.')
            sys.stdout.flush()
        res = requests.get(self.base_url + link)
        soup = BeautifulSoup(res.text, 'html.parser')
        paras = soup.find_all('p')
        self.articles[index] = "\n\n[SECTION]\n\n".join([p.get_text().strip() for p in paras])

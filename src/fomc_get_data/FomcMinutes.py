from datetime import datetime
import sys
import re
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
from .FomcBase import FomcBase

class FomcMinutes(FomcBase):
    def __init__(self, verbose=True, max_threads=10, base_dir='../data/FOMC/'):
        super().__init__('minutes', verbose, max_threads, base_dir)

    def _get_links(self, from_year):
        self.links, self.titles, self.speakers, self.dates = [], [], [], []
        for year in range(from_year, datetime.today().year + 1):
            url = self.base_url + f"/monetarypolicy/fomchistorical{year}.htm"
            if self.verbose:
                print(f"Getting minutes for {year}: {url}")
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            anchors = soup.find_all('a', href=re.compile(r'(minutes|fomcmoa).*?\.(pdf|htm)$', re.I))
            for a in anchors:
                href = a['href']
                dt = self._date_from_link(href)
                self.links.append(href)
                self.titles.append('Minutes')
                self.dates.append(datetime.strptime(dt, '%Y-%m-%d'))
                self.speakers.append(self._speaker_from_date(dt))
        if self.verbose:
            print(f"Total minutes links: {len(self.links)}")

    def _add_article(self, link, index=None):
        if self.verbose:
            sys.stdout.write('.')
            sys.stdout.flush()
        full_link = requests.compat.urljoin(self.base_url, link)
        if full_link.lower().endswith('.pdf'):
            res = requests.get(full_link)
            pdf_reader = PdfReader(BytesIO(res.content))
            text = "\n".join([page.extract_text() or '' for page in pdf_reader.pages])
        else:
            res = requests.get(full_link)
            soup = BeautifulSoup(res.text, 'html.parser')
            paras = soup.find_all('p')
            text = "\n\n[SECTION]\n\n".join([p.get_text().strip() for p in paras])
        self.articles[index] = text

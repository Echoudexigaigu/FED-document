import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
from .FomcBase import FomcBase

class FomcTealbook(FomcBase):
    def __init__(self, verbose=True, max_threads=4, base_dir='../data/FOMC/'):
        super().__init__('tealbook', verbose, max_threads, base_dir)

    def _get_links(self, from_year):
        self.links = []
        self.titles = []
        self.dates = []
        self.speakers = []
        start = max(from_year, 2010)
        for year in range(start, datetime.today().year + 1):
            page_url = self.base_url + f"/monetarypolicy/fomchistorical{year}.htm"
            if self.verbose:
                print(f"Fetching Tealbook for {year}: {page_url}")
            r = requests.get(page_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            found = soup.find_all('a', href=re.compile(r'tealbooka.*\.pdf$', re.I))
            for a in found:
                href = a['href']
                dt_str = self._date_from_link(href)
                self.links.append(href)
                self.titles.append('Tealbook A')
                self.dates.append(datetime.strptime(dt_str, '%Y-%m-%d'))
                self.speakers.append(self._speaker_from_date(dt_str))
        if self.verbose:
            print(f"Total Tealbook A links: {len(self.links)}")

    def _add_article(self, link, index=None):
        if self.verbose:
            import sys; sys.stdout.write('.'); sys.stdout.flush()
        full_link = requests.compat.urljoin(self.base_url, link)
        if self.verbose:
            print(f"\nDownloading from: {full_link}")
        res = requests.get(full_link)
        pdf_reader = PdfReader(BytesIO(res.content))
        text = "\n".join([page.extract_text() or '' for page in pdf_reader.pages])
        self.articles[index] = text

from datetime import datetime
import sys
import re
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
from .FomcBase import FomcBase

class FomcAgenda(FomcBase):
    def __init__(self, verbose=True, max_threads=10, base_dir='data/FOMC/'):
        super().__init__('agenda', verbose, max_threads, base_dir)

    def _get_links(self, from_year):
        self.links, self.titles, self.speakers, self.dates = [], [], [], []
        end_year = datetime.today().year
        for year in range(from_year, end_year + 1):
            url = self.base_url + f"/monetarypolicy/fomchistorical{year}.htm"
            if self.verbose:
                print(f"Fetching agenda for {year}: {url}")
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                anchors = soup.find_all('a', href=re.compile(r'agenda.*\.pdf$', re.I))
                for a in anchors:
                    href = a['href']
                    dt = self._date_from_link(href)
                    self.links.append(href)
                    self.titles.append('Agenda')
                    self.dates.append(datetime.strptime(dt, '%Y-%m-%d'))
                    self.speakers.append(self._speaker_from_date(dt))
            except Exception as e:
                if self.verbose:
                    print(f"Error fetching agenda for {year}: {e}")
                continue
        if self.verbose:
            print(f"Total agenda links: {len(self.links)}")


    def _add_article(self, link, index=None):
        """
        Download and extract text from an FOMC Agenda PDF.
        """
        if self.verbose:
            sys.stdout.write('.')
            sys.stdout.flush()
            
        try:
            full_link = requests.compat.urljoin(self.base_url, link)
            if self.verbose:
                print(f"\nDownloading agenda from: {full_link}")
                
            res = requests.get(full_link)
            res.raise_for_status()
            
            # Extract text from PDF
            pdf_reader = PdfReader(BytesIO(res.content))
            text = "\n".join([page.extract_text() or '' for page in pdf_reader.pages])
            
            self.articles[index] = text
            
        except Exception as e:
            if self.verbose:
                print(f"\nError downloading agenda {link}: {e}")
            self.articles[index] = ""

if __name__ == "__main__":
    import os
    import sys
    
    # Create test directory in current location
    test_base_dir = './fomc_agenda_test_output/'
    os.makedirs(test_base_dir, exist_ok=True)
    
    # Test FomcAgenda - just test link discovery first
    print("Testing FOMC Agenda scraper...")
    agenda_scraper = FomcAgenda(verbose=True, base_dir=test_base_dir)
    
    # Test just the link finding functionality for 2019 
    print("Finding agenda links for 2019...")
    agenda_scraper._get_links(from_year=2019)
    
    if len(agenda_scraper.links) > 0:
        print(f"✓ Success! Found {len(agenda_scraper.links)} agenda documents")
        print("Sample links found:")
        for i, link in enumerate(agenda_scraper.links[:3]):  # Show first 3
            print(f"  {i+1}. {link}")
            
        # Test downloading one agenda document
        print("\nTesting download of first agenda...")
        agenda_scraper.articles = [''] * len(agenda_scraper.links)
        agenda_scraper._add_article(agenda_scraper.links[0], 0)
        
        if agenda_scraper.articles[0]:
            print("✓ Successfully downloaded and extracted text from agenda!")
            print(f"Text length: {len(agenda_scraper.articles[0])} characters")
        else:
            print("✗ Failed to download agenda content")
    else:
        print("✗ No agenda documents found. Check the meeting dates or URL structure.") 
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
        
        # Known FOMC meeting dates (since agendas follow specific meeting schedule)
        # These are the actual FOMC meeting dates that have agendas available
        # Note: FOMC documents have ~5 year embargo, so only 2019 and earlier are publicly available
        self.fomc_meeting_dates = {
            2019: ["20190130", "20190320", "20190501", "20190619", "20190731", "20190918", "20191030", "20191211"],
            2018: ["20180131", "20180321", "20180502", "20180613", "20180801", "20180926", "20181108", "20181219"],
            2017: ["20170201", "20170315", "20170503", "20170614", "20170726", "20170920", "20171101", "20171213"],
            2016: ["20160127", "20160316", "20160427", "20160615", "20160727", "20160921", "20161102", "20161214"],
            2015: ["20150128", "20150318", "20150429", "20150617", "20150917", "20151028", "20151216"],
            2014: ["20140129", "20140319", "20140430", "20140618", "20140730", "20140917", "20141029", "20141217"],
            2013: ["20130130", "20130320", "20130501", "20130619", "20130731", "20130918", "20131030", "20131218"],
            2012: ["20120125", "20120313", "20120425", "20120620", "20120801", "20120913", "20121024", "20121212"],
            2011: ["20110126", "20110315", "20110427", "20110622", "20110809", "20110921", "20111102", "20111213"],
            2010: ["20100127", "20100316", "20100428", "20100623", "20100810", "20100921", "20101103", "20101214"],
            # Add more years as needed - these dates can be found from the FOMC calendar
        }

    def _get_links(self, from_year):
        """
        Get FOMC Agenda document links from the Federal Reserve files directory.
        Agendas are individual PDF files with specific meeting dates.
        
        Due to FOMC's ~5 year embargo policy, only documents from 2019 and earlier 
        are publicly available.
        """
        self.links, self.titles, self.speakers, self.dates = [], [], [], []
        
        # Limit the to_year to 2019 due to 5-year embargo
        current_year = datetime.today().year
        max_available_year = min(2019, current_year - 5)
        
        if self.verbose:
            print(f"Note: FOMC documents have ~5 year embargo. Searching years {from_year} to {max_available_year}")
        
        for year in range(from_year, max_available_year + 1):
            if year not in self.fomc_meeting_dates:
                if self.verbose:
                    print(f"No meeting dates defined for {year}, skipping...")
                continue
                
            for meeting_date in self.fomc_meeting_dates[year]:
                # Construct the agenda PDF URL
                agenda_url = f"/monetarypolicy/files/FOMC{meeting_date}agenda.pdf"
                full_url = self.base_url + agenda_url
                
                if self.verbose:
                    print(f"Checking agenda for {meeting_date}: {full_url}")
                
                try:
                    # Check if the agenda PDF exists
                    response = requests.head(full_url, timeout=10)
                    if response.status_code == 200:
                        # Parse date from meeting_date string
                        dt = self._date_from_link(meeting_date)
                        if dt:
                            self.links.append(agenda_url)
                            self.titles.append(f'FOMC Agenda - {meeting_date}')
                            self.dates.append(datetime.strptime(dt, '%Y-%m-%d'))
                            self.speakers.append(self._speaker_from_date(dt))
                            
                            if self.verbose:
                                print(f"✓ Found agenda for {meeting_date}")
                        else:
                            if self.verbose:
                                print(f"✗ Could not parse date from {meeting_date}")
                    else:
                        if self.verbose:
                            print(f"✗ Agenda not available for {meeting_date} (HTTP {response.status_code})")
                            
                except Exception as e:
                    if self.verbose:
                        print(f"✗ Error checking {meeting_date}: {e}")
                    continue
                
        if self.verbose:
            print(f"Total agenda documents found: {len(self.links)}")

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
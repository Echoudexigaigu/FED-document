from datetime import datetime
import sys
import re
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
from .FomcBase import FomcBase

class FomcBlueBook(FomcBase):
    def __init__(self, verbose=True, max_threads=4, base_dir='data/FOMC/'):
        super().__init__('bluebook', verbose, max_threads, base_dir)

    def _date_from_link(self, link):
        """
        Override parent method to handle Blue Book specific date patterns.
        Blue Books may have dates in different formats.
        """
        # Try the parent method first (looks for 8-digit dates)
        try:
            return super()._date_from_link(link)
        except (IndexError, ValueError):
            # Try alternative patterns for Blue Books
            # Look for patterns like 20230315, 2023-03-15, etc.
            date_patterns = [
                r'(\d{4})(\d{2})(\d{2})',  # YYYYMMDD
                r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
                r'(\d{4})(\d{1,2})(\d{1,2})',  # YYYYMDD or YYYYMMDD
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, link)
                if match:
                    year, month, day = match.groups()
                    # Pad month and day with zeros if needed
                    month = month.zfill(2)
                    day = day.zfill(2)
                    return f"{year}-{month}-{day}"
            
            # If no date found, return None
            return None

    def _get_links(self, from_year):
        """
        Get FOMC Blue Book document links from the Federal Reserve historical materials.
        Blue Books were published from 1965 to 2010, when they merged with Green Books to become Teal Books.
        """
        self.links, self.titles, self.speakers, self.dates = [], [], [], []
        
        # Blue Books only available from 1965 to 2010
        start_year = max(1965, from_year)
        end_year = min(2010, datetime.today().year)
        
        if start_year > 2010:
            if self.verbose:
                print("Blue Books were discontinued in 2010. Use FomcTealbook for documents after 2010.")
            return
        
        for year in range(start_year, end_year + 1):
            url = self.base_url + f"/monetarypolicy/fomchistorical{year}.htm"
            if self.verbose:
                print(f"Getting Blue Book links for {year}: {url}")
            
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Find Blue Book links with more comprehensive patterns
                # Look for links that contain 'blue' in href or link text, or monetary policy alternatives
                anchors = soup.find_all('a', href=re.compile(r'.*\.pdf$', re.I))
                
                for a in anchors:
                    href = a['href']
                    link_text = a.get_text().lower()
                    
                    # Check if this is likely a Blue Book link
                    blue_book_indicators = [
                        'blue' in href.lower(),
                        'blue' in link_text,
                        'bluebook' in href.lower(),
                        'bluebook' in link_text,
                        'monetary policy alternatives' in link_text,
                        'book a' in link_text,  # Sometimes referred to as "Book A"
                        'bb' in href.lower() and len(href.split('/'))[-1].startswith(('bb', 'BB'))
                    ]
                    
                    if any(blue_book_indicators):
                        dt = self._date_from_link(href)
                        if dt:  # Only add if we can parse a date
                            self.links.append(href)
                            self.titles.append('Blue Book')
                            self.dates.append(datetime.strptime(dt, '%Y-%m-%d'))
                            self.speakers.append(self._speaker_from_date(dt))
                        
            except Exception as e:
                if self.verbose:
                    print(f"Error processing {year}: {e}")
                continue
                
        if self.verbose:
            print(f"Total Blue Book links found: {len(self.links)}")
            if end_year >= 2010:
                print("Note: Blue Books were discontinued in 2010 and merged with Green Books to form Teal Books.")

    def _add_article(self, link, index=None):
        """
        Download and extract text from a Blue Book PDF.
        """
        if self.verbose:
            sys.stdout.write('.')
            sys.stdout.flush()
            
        try:
            full_link = requests.compat.urljoin(self.base_url, link)
            if self.verbose:
                print(f"\nDownloading Blue Book from: {full_link}")
                
            res = requests.get(full_link)
            res.raise_for_status()
            
            # Extract text from PDF
            pdf_reader = PdfReader(BytesIO(res.content))
            text = "\n".join([page.extract_text() or '' for page in pdf_reader.pages])
            
            self.articles[index] = text
            
        except Exception as e:
            if self.verbose:
                print(f"\nError downloading Blue Book {link}: {e}")
            self.articles[index] = ""

if __name__ == "__main__":
    import os
    
    # Create test directory
    test_base_dir = os.path.join('..', '..', 'data', 'fomc_bluebook_test_output')
    os.makedirs(test_base_dir, exist_ok=True)
    
    # Test FomcBlueBook
    bluebook_scraper = FomcBlueBook(verbose=True, base_dir=test_base_dir)
    bluebook_scraper.get_contents(from_year=2000)  # Test with years before 2010
    bluebook_scraper.pickle_dump_df(filename="bluebook.pickle")
    print(f"Scraped {len(bluebook_scraper.articles)} Blue Book documents") 
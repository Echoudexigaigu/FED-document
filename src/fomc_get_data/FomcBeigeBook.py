from datetime import datetime
import sys
import re
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
from .FomcBase import FomcBase

class FomcBeigeBook(FomcBase):
    def __init__(self, verbose=True, max_threads=10, base_dir='data/FOMC/'):
        super().__init__('beigebook', verbose, max_threads, base_dir)

    def _date_from_link(self, link):
        """
        Override parent method to handle Beige Book specific date patterns.
        Beige Books may have dates in different formats.
        """
        # Try the parent method first (looks for 8-digit dates)
        try:
            return super()._date_from_link(link)
        except (IndexError, ValueError):
            # Try alternative patterns for Beige Books
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
        Get FOMC Beige Book document links from the Federal Reserve website.
        Beige Books are published 8 times per year since 1983.
        """
        self.links, self.titles, self.speakers, self.dates = [], [], [], []
        
        # First get current Beige Books from the main Beige Book page
        url = self.base_url + "/monetarypolicy/publications/beige-book-default.htm"
        if self.verbose:
            print(f"Getting current Beige Book links from: {url}")
            
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find PDF links for current Beige Books
            pdf_links = soup.find_all('a', href=re.compile(r'.*[Bb]eige[Bb]ook.*\.pdf$', re.I))
            
            for a in pdf_links:
                href = a['href']
                # Try to extract date from filename or nearby text
                dt = self._date_from_link(href)
                if dt:
                    try:
                        year = int(dt.split('-')[0])
                        if year >= from_year:
                            self.links.append(href)
                            self.titles.append('Beige Book')
                            self.dates.append(datetime.strptime(dt, '%Y-%m-%d'))
                            self.speakers.append(self._speaker_from_date(dt))
                    except (ValueError, IndexError) as e:
                        if self.verbose:
                            print(f"Error parsing date {dt} for {href}: {e}")
                        continue
        except Exception as e:
            if self.verbose:
                print(f"Error getting current Beige Books: {e}")
        
        # Get historical Beige Books from FOMC historical materials
        for year in range(max(1983, from_year), datetime.today().year + 1):
            url = self.base_url + f"/monetarypolicy/fomchistorical{year}.htm"
            if self.verbose:
                print(f"Getting Beige Book links for {year}: {url}")
            
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Find Beige Book links with more specific patterns
                # Look for links that contain 'beige' in href or link text
                anchors = soup.find_all('a', href=re.compile(r'.*\.(pdf|htm)$', re.I))
                
                for a in anchors:
                    href = a['href']
                    link_text = a.get_text().lower()
                    
                    # Check if this is likely a Beige Book link
                    if ('beige' in href.lower() or 'beige' in link_text or 
                        'summary of commentary' in link_text or 
                        'current economic conditions' in link_text):
                        
                        dt = self._date_from_link(href)
                        if dt:  # Only add if we can parse a date
                            try:
                                self.links.append(href)
                                self.titles.append('Beige Book')
                                self.dates.append(datetime.strptime(dt, '%Y-%m-%d'))
                                self.speakers.append(self._speaker_from_date(dt))
                            except ValueError as e:
                                if self.verbose:
                                    print(f"Error parsing date {dt} for {href}: {e}")
                                continue
                        
            except Exception as e:
                if self.verbose:
                    print(f"Error processing {year}: {e}")
                continue
                
        if self.verbose:
            print(f"Total Beige Book links found: {len(self.links)}")

    def _add_article(self, link, index=None):
        """
        Download and extract text from a Beige Book document (PDF or HTML).
        """
        if self.verbose:
            sys.stdout.write('.')
            sys.stdout.flush()
            
        try:
            full_link = requests.compat.urljoin(self.base_url, link)
            if self.verbose:
                print(f"\nDownloading Beige Book from: {full_link}")
                
            res = requests.get(full_link)
            res.raise_for_status()
            
            if full_link.lower().endswith('.pdf'):
                # Extract text from PDF
                pdf_reader = PdfReader(BytesIO(res.content))
                text = "\n".join([page.extract_text() or '' for page in pdf_reader.pages])
            else:
                # Extract text from HTML
                soup = BeautifulSoup(res.text, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                # Get text content
                text = soup.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
            
            self.articles[index] = text
            
        except Exception as e:
            if self.verbose:
                print(f"\nError downloading Beige Book {link}: {e}")
            self.articles[index] = ""

if __name__ == "__main__":
    import os
    
    # Create test directory
    test_base_dir = os.path.join('..', '..', 'data', 'fomc_beigebook_test_output')
    os.makedirs(test_base_dir, exist_ok=True)
    
    # Test FomcBeigeBook
    beigebook_scraper = FomcBeigeBook(verbose=True, base_dir=test_base_dir)
    beigebook_scraper.get_contents(from_year=2020)
    beigebook_scraper.pickle_dump_df(filename="beigebook.pickle")
    print(f"Scraped {len(beigebook_scraper.articles)} Beige Book documents") 
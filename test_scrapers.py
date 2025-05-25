#!/usr/bin/env python3
"""
Test script for all FOMC scraper classes.
This script tests the newly created classes: FomcAgenda, FomcBeigeBook, and FomcBlueBook.
"""

import os
import sys
sys.path.append('src')

from fomc_get_data.FomcAgenda import FomcAgenda
from fomc_get_data.FomcBeigeBook import FomcBeigeBook
from fomc_get_data.FomcBlueBook import FomcBlueBook

def test_scraper(scraper_class, test_name, from_year=2020, max_docs=2):
    """Test a scraper class and download a small sample of documents."""
    print(f"\n{'='*50}")
    print(f"Testing {test_name}")
    print(f"{'='*50}")
    
    try:
        # Create test directory
        test_base_dir = os.path.join('data', f'test_{test_name.lower().replace(" ", "_")}')
        os.makedirs(test_base_dir, exist_ok=True)
        
        # Initialize scraper
        scraper = scraper_class(verbose=True, base_dir=test_base_dir)
        
        # Get links first
        print(f"Getting links for {test_name} from {from_year}...")
        scraper._get_links(from_year)
        
        print(f"Found {len(scraper.links)} links")
        if len(scraper.links) == 0:
            print(f"No links found for {test_name}")
            return
        
        # Limit to first few documents for testing
        if len(scraper.links) > max_docs:
            scraper.links = scraper.links[:max_docs]
            scraper.titles = scraper.titles[:max_docs]
            scraper.speakers = scraper.speakers[:max_docs]
            scraper.dates = scraper.dates[:max_docs]
            print(f"Limited to {max_docs} documents for testing")
        
        # Download and process documents using the correct method name
        print(f"Downloading {len(scraper.links)} documents...")
        df = scraper.get_contents(from_year)
        
        # Save results using the correct method name
        scraper.pickle_dump_df(filename=f"{test_name.lower().replace(' ', '_')}.pickle")
        
        print(f"Successfully scraped {len(scraper.articles)} {test_name} documents")
        print(f"Data saved to: {test_base_dir}")
        print(f"DataFrame shape: {df.shape}")
        
        # Show sample content
        if scraper.articles and len(scraper.articles) > 0:
            first_article = scraper.articles[0]
            if first_article:
                print(f"Sample content (first 200 chars): {first_article[:200]}...")
            else:
                print("First article is empty")
        else:
            print("No articles found")
        
    except Exception as e:
        print(f"Error testing {test_name}: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function."""
    print("Testing FOMC Scraper Classes")
    print("This script will test the newly created scraper classes by downloading sample documents.")
    
    # Test Agenda scraper
    test_scraper(FomcAgenda, "FOMC Agenda", from_year=2020, max_docs=2)
    
    # Test Beige Book scraper  
    test_scraper(FomcBeigeBook, "FOMC Beige Book", from_year=2023, max_docs=2)
    
    # Test Blue Book scraper (only available until 2010)
    test_scraper(FomcBlueBook, "FOMC Blue Book", from_year=2008, max_docs=2)
    
    print(f"\n{'='*50}")
    print("Testing completed!")
    print("Check the 'data/' directory for downloaded test files.")
    print(f"{'='*50}")

if __name__ == "__main__":
    main() 
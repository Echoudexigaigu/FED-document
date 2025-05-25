# 🏛️ Federal Reserve Document Scraper - Usage Guide

## 📋 Overview

This project now includes complete scrapers for all major FOMC document types. All the missing files mentioned in the README.md have been implemented:

✅ **FomcAgenda.py** - FOMC Meeting Agendas  
✅ **FomcBeigeBook.py** - Beige Book Reports  
✅ **FomcBlueBook.py** - Blue Books (1965-2010)  

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test the Scrapers

Run the test script to verify everything works:

```bash
python test_scrapers.py
```

### 3. Download Specific Document Types

Use the main script to download specific document types:

```bash
# Download FOMC Agendas from 2020
python src/FomcGetData.py agenda 2020

# Download Beige Books from 2023
python src/FomcGetData.py beigebook 2023

# Download Blue Books from 2008 (only available until 2010)
python src/FomcGetData.py bluebook 2008

# Download all document types from 2020
python src/FomcGetData.py all 2020
```

## 📊 Available Document Types

| Document Type | Command | Years Available | Description |
|--------------|---------|-----------------|-------------|
| **Agenda** | `agenda` | 1980-present | Meeting agendas outlining discussion topics |
| **Beige Book** | `beigebook` | 1983-present | Economic conditions by Federal Reserve District |
| **Blue Book** | `bluebook` | 1965-2010 | Monetary policy alternatives (discontinued in 2010) |
| **Minutes** | `minutes` | 1993-present | Meeting minutes and decisions |
| **Statements** | `statement` | 1994-present | Post-meeting policy statements |
| **Transcripts** | `meeting_script` | 1994-present (5-year delay) | Full meeting transcripts |
| **Greenbook** | `greenbook_part1` | 1964-2010 | Economic analysis and forecasts |
| **Tealbook** | `tealbook_a` | 2010-present | Economic analysis (replaced Greenbook/Bluebook) |

## 📁 Output Structure

Downloaded files are organized as:

```
data/
├── agenda/
│   ├── FOMC_agenda_2020-01-01.txt
│   └── ...
├── beigebook/
│   ├── FOMC_beigebook_2023-01-15.txt
│   └── ...
└── bluebook/
    ├── FOMC_bluebook_2008-01-30.txt
    └── ...
```

## 🔧 Advanced Usage

### Individual Class Usage

```python
from src.fomc_get_data.FomcAgenda import FomcAgenda
from src.fomc_get_data.FomcBeigeBook import FomcBeigeBook
from src.fomc_get_data.FomcBlueBook import FomcBlueBook

# Create scraper instance
agenda_scraper = FomcAgenda(verbose=True, base_dir='./data/agendas/')

# Get documents from specific year
agenda_scraper.get_documents(from_year=2020)

# Save to DataFrame
df = agenda_scraper.save_to_DataFrame()

# Save as text files
agenda_scraper.save_texts(prefix="FOMC_agenda_")
```

### Batch Processing

```python
# Download multiple document types
document_types = [
    ('agenda', FomcAgenda, 2020),
    ('beigebook', FomcBeigeBook, 2023),
    ('bluebook', FomcBlueBook, 2008)
]

for doc_type, scraper_class, from_year in document_types:
    scraper = scraper_class(verbose=True)
    scraper.get_documents(from_year=from_year)
    scraper.save_to_DataFrame()
    print(f"Downloaded {len(scraper.articles)} {doc_type} documents")
```

## 📝 Document Details

### FOMC Agendas
- **Purpose**: Outline meeting discussion topics and structure
- **Format**: PDF files
- **Frequency**: 8 times per year (for each FOMC meeting)
- **Content**: Meeting agenda items, presentations, and discussion topics

### Beige Book
- **Purpose**: Regional economic conditions summary
- **Format**: PDF and HTML files
- **Frequency**: 8 times per year (published ~2 weeks before FOMC meetings)
- **Content**: Economic conditions by Federal Reserve District

### Blue Books (Historical)
- **Purpose**: Monetary policy alternatives and analysis
- **Format**: PDF files
- **Frequency**: 8 times per year (1965-2010)
- **Note**: Merged with Greenbook to form Tealbook in 2010

## 🔍 Web Sources

The scrapers extract data from these official Federal Reserve pages:

- **Agendas**: [FOMC Historical Materials](https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm)
- **Beige Book**: [Beige Book Publications](https://www.federalreserve.gov/monetarypolicy/publications/beige-book-default.htm)
- **Blue Books**: [FOMC Historical Materials](https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm)

## ⚠️ Important Notes

1. **Rate Limiting**: The scrapers include delays to respect the Federal Reserve website
2. **5-Year Delay**: Some documents (like transcripts) are only available after a 5-year delay
3. **PDF Extraction**: Uses PyPDF2 for PDF text extraction - some formatting may be lost
4. **Error Handling**: Scrapers include robust error handling for failed downloads

## 🐛 Troubleshooting

### Common Issues

1. **PDF Extraction Errors**:
   ```bash
   # Install additional PDF processing tools
   pip install pymupdf
   ```

2. **Network Timeouts**:
   - Reduce max_threads parameter
   - Add delays between requests

3. **Missing Dependencies**:
   ```bash
   pip install beautifulsoup4 requests pandas PyPDF2
   ```

## 📞 Support

For issues or questions:
1. Check the test script output: `python test_scrapers.py`
2. Review the verbose output for specific error messages
3. Ensure you have the latest version of dependencies

---

*Happy scraping! 🚀* 
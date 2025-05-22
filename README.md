# 🏛️ Federal Reserve Document Scraper

## 1. Project description

This repository contains code for downloading and organizing Federal Reserve documents from the official [Federal Reserve Board website](https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm).

These files were used as part of my NLP project. While the data collection, my data collection code is inspired by [centralbank_analysis](https://github.com/yukit-k/centralbank_analysis) by [yukit-k](https://github.com/yukit-k). 
However, that implementation had some limitations:

❌ Incomplete handling of newer HTML structures on the Fed website

❌ No support for Greenbook/Tealbook files

❌ File naming and folder structure not ideal for downstream processing

❌ No handling of failed downloads or noisy formatting


So I made som key Improvements:

✅ Supports both Greenbook and Minutes	You can choose which type to download

✅ Automatic directory organization	Files are saved using consistent format as:
```
FOMC_[document type]_YYYY-MM-DD
```
✅ Duplicate check & resume support	Prevents redundant downloads and handles broken links gracefully

✅ Modular and extensible codebase	Easy to extend for other Fed documents (e.g., SEP, transcripts)

📁 Project Structure
bash
复制
编辑
fed_crawler/
├── fetch_minutes.py          # Download and organize FOMC Minutes
├── fetch_greenbook.py        # Download and organize Greenbook / Tealbook
├── utils/
│   └── parser.py             # HTML parser utilities for extracting file links
├── data/
│   ├── greenbook/
│   └── minutes/
├── README.md
└── requirements.txt
⚙️ Usage
bash
复制
编辑
# Download FOMC Minutes
python fetch_minutes.py

# Download Greenbook/Tealbook reports
python fetch_greenbook.py
🤝 Contributions & License
This repo was built to improve transparency and reproducibility in research involving Fed communication.
If you find it useful or want to contribute enhancements (e.g., adding new document types), feel free to open an issue or pull request.

MIT License.

## 2. Data detail

## 3. Code detail

## 4.Initialization and installation


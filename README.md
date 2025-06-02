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

## 2. Project structure
```
FED-document/
├── data/                                   #没做，暂时也不重要
├── src/
│   ├── fomc_get_data
│   │   ├── FomcAgenda.py 
│   │   ├── FomcBase.py
│   │   ├── FomcBeigeBook.py
│   │   ├── FomcBlueBook.py
│   │   ├── FomcGreenbook.py
│   │   ├── FomcMeetingScript.py 
│   │   ├── FomcMinutes.py
│   │   ├── FomcPresConfScript.py
│   │   ├── FomcStatement.py
│   │   ├── FomcTealbook.py
│   │   ├── FomcTestimony.py
│   │   └── __init__.py
│   ├── FomcGetData.py                      #我搞好了，但是要修改
│   ├── QuandlGetData.py                    #❌没搞，暂时没搞懂他要干什么，可能要删掉
│   └── pdf2text.py                         #✅我搞好了，没有必要修改
├── LICENSE                                 #✅我搞好了，没有必要修改
└── requirements.txt                        #✅我搞好了，没有必要修改
```

## 3. Data detail

```
解释一下每个文件，直接chatgpt+wiki
```

## 4. Initialization and installation

```
最好做一个makefile，然后讲一下怎么下载数据
```

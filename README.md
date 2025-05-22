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
```
FED-document/
├── data/ #没做，暂时也不重要
│   ├──
│   ├──
│   ├──
│   ├──
│   ├──
│   ├──
│   ├──
│   └──
│
├── src/
│   ├──fomc_get_data
│   │   ├──FomcAgenda.py                   #❌没搞，你可以根据我加✅的写，比较简单
│   │   ├──FomcBase.py                     #我搞好了，但是可以修改
│   │   ├──FomcBeigeBook.py                #❌没搞，你可以根据我加✅的写，比较简单
│   │   ├──FomcBlueBook.py                 #❌没搞，你可以根据我加✅的写。注意2010年后bluebook和Greenbook合并为tealbook。
│   │   ├──FomcGreenbook.py                #✅我搞好了，没有必要修改
│   │   ├──FomcMeetingScript.py            #❌没搞，你可以根据我加✅的写。对应网页中的FOMC Meeting Transcript。
│   │   ├──FomcMinutes.py                  #✅我搞好了，没有必要修改
│   │   ├──FomcPresConfScript.py           #❌没搞好，比较难的一个
│   │   ├──FomcStatement.py                #✅我搞好了，没有必要修改
│   │   ├──FomcTealbook.py                 #✅我搞好了，没有必要修改
│   │   ├──FomcTestimony.py                #❌没搞，暂时没搞懂他要干什么
│   │   └──__init__.py                     #搞好了，但是要修改
│   │
│   ├──FomcGetData.py                      #我搞好了，但是要修改
│   ├──QuandlGetData.py                    #❌没搞，暂时没搞懂他要干什么
│   └──pdf2text.py                         #✅我搞好了，没有必要修改
│
└── requirements.txt                       #✅我搞好了，没有必要修改
```

## 2. Data detail

```
解释一下每个文件，直接chatgpt+wiki
```

## 3. Initialization and installation

```
最好做一个makefile，然后讲一下怎么下载数据
```


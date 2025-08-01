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
├── src/
│   ├── data
│   │   └── 
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
│   ├── FomcGetData.py                      
│   ├── QuandlGetData.py                    
│   └── pdf2text.py   
├── LICENSE
└── requirements.txt
```

## 3. Data detail

This repository contains modules for downloading and processing various official publications of the **Federal Open Market Committee (FOMC)**. These documents, produced and released by the Federal Reserve, provide detailed insight into U.S. monetary policy formation, communication, and economic analysis over time.

Below is a reference guide to the major FOMC document types represented in this repository.

---

## 📋 FOMC Document Overview

### 📅 `FomcAgenda.py` – Meeting Agendas
Agendas are created by the FOMC Secretariat in coordination with the Chair and outline the topics of discussion for each meeting, including standard items (e.g., open market operations, economic outlook) and special topics. Participants receive the agenda about one week in advance.

---

### 📄 `FomcStatement.py` – Policy Statements
FOMC statements are brief summaries of monetary policy decisions released **immediately after each meeting**. These statements have become a key communication tool since 1994 and are now issued after **every scheduled meeting**, even if policy remains unchanged.

---

### 📝 `FomcMinutes.py` – Meeting Minutes
Minutes provide a concise, narrative summary of policy discussions and rationales. Since 2004, they are released **three weeks** after each meeting. The minutes include details on voting outcomes and dissenting views, and are eventually included in the Fed’s Annual Report.

---

### 🧾 `FomcPresConfScript.py` – Press Conference Transcripts
Beginning in 2011, the Fed Chair has held press conferences following certain FOMC meetings. These transcripts document the Chair’s remarks and responses to journalists, offering additional context and forward guidance. Released shortly after the meeting.

---

### 🗣️ `FomcMeetingScript.py` – Meeting Transcripts
Verbatim transcripts of FOMC meetings, produced from audio recordings and lightly edited for readability. They are released with a **5-year delay**. For meetings prior to 1994, transcripts were reconstructed from raw records and may contain transcription uncertainties.

---

### 📚 `FomcGreenbook.py` – Greenbook (1964–2010)
The Greenbook, officially titled *Current Economic and Financial Conditions*, was prepared by Board staff and delivered to FOMC members **six days before each meeting**. It provided forecasts, data analyses, and economic outlooks.

- **Part 1:** Summary and forecast  
- **Part 2:** Detailed breakdowns  
- **Supplement:** Late-breaking updates

---

### 📘 `FomcBlueBook.py` – Bluebook (1965–2010)
The Bluebook, titled *Monetary Policy Alternatives*, outlined potential policy options and risks. It was distributed shortly after the Greenbook and informed FOMC decisions. The document evolved from earlier versions like *Money Market and Reserve Relationships*.

---

### 🧠 `FomcTealbook.py` – Tealbook (2010–Present)
The Tealbook replaced both the Greenbook and Bluebook in June 2010. It is split into two parts:

- **Tealbook A:** *Current Situation and Outlook* — Forecasts and financial developments  
- **Tealbook B:** *Strategies and Alternatives* — Policy options and simulations

Both are released with a **5-year lag**.

---

### 📙 `FomcBeigeBook.py` – Beige Book
The Beige Book, published **eight times a year**, summarizes anecdotal economic conditions across the 12 Federal Reserve Districts. Based on business surveys, interviews, and internal reports, it is released ~two weeks before each meeting.

---

### 🧾 `FomcTestimony.py` – Testimony before Congress
This includes the Chair’s **Semiannual Monetary Policy Report to Congress** and other testimonies. These communications explain the Fed’s outlook and policies directly to lawmakers and the public.

---

## 📚 References

- [Federal Reserve – FOMC Archive](https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm)  
- [Wikipedia – Federal Open Market Committee](https://en.wikipedia.org/wiki/Federal_Open_Market_Committee)


## 4. Initialization and installation

```

```

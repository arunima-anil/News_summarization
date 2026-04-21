<div align="center">

# Company News Sentiment Analysis Tool

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Models-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co)
[![NLP](https://img.shields.io/badge/Domain-NLP_%26_Sentiment-8b5cf6?style=for-the-badge)](.)

> Enter a company name - get news sentiment analysis, comparative report, and an AI-generated Hindi audio summary.

</div>

---

## What It Does

| Step | What Happens |
|---|---|
| 1. Input company name | App fetches the latest news articles |
| 2. Sentiment Analysis | Each article classified as Positive / Negative / Neutral |
| 3. Comparative Analysis | Cross-article trends and key topic extraction |
| 4. Hindi TTS Output | Full report converted to Hindi speech audio |

---

## Features

- Multi-source news fetching via APIs
- Transformer-based NLP (HuggingFace) for summarization and sentiment
- Hindi Text-to-Speech audio output
- Streamlit web interface
- Deployed on HuggingFace Spaces

---

## Project Structure

```
News_summarization/
├── app.py                 - Streamlit app entry point
├── news_fetcher.py        - News API integration
├── summarizer.py          - HuggingFace summarization pipeline
├── sentiment_analysis.py  - Sentiment classification
├── tts.py                 - Hindi text-to-speech generation
└── requirements.txt
```

---

## Run Locally

```bash
git clone https://github.com/arunima-anil/News_summarization
cd News_summarization
pip install -r requirements.txt
streamlit run app.py
```

---

<div align="center">Built as part of AI & Data Science portfolio | <a href="https://github.com/arunima-anil">@arunima-anil</a></div>

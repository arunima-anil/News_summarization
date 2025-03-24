import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from news_fetcher2 import get_news_articles  # Import the RSS scraping function
from news_fetcher import fetch_news  # Import the NewsAPI function
from sentiment_analysis import analyze_sentiment  # Import the sentiment analysis function
from summarizer import generate_overall_summary  # Import the summarizer function
from tts import translate_and_generate_audio  # Import the TTS function
import asyncio
import io
import json

# Set up the Streamlit app title
st.title("Company News Sentiment Analysis")

# Initialize session state for storing generated files
if "img_buffer" not in st.session_state:
    st.session_state.img_buffer = None
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None
if "json_report" not in st.session_state:
    st.session_state.json_report = None

# Input field for company name
company_name = st.text_input("Enter Company Name", placeholder="e.g., Reliance Industries")

# Dropdown to select news source
news_source = st.selectbox("Select News Source", ["NewsAPI", "Bing Scrape"])

# Submit button
if st.button("Generate Report"):
    if not company_name:
        st.warning("Please enter a company name to generate the report.")
    else:
        # Fetch news articles based on the selected news source
        with st.spinner("Fetching news articles and analyzing sentiment..."):
            if news_source == "RSS Scrape":
                articles = get_news_articles(company_name)  # Use RSS scraping
            else:
                articles = fetch_news(company_name)  # Use NewsAPI
            
            if not articles:
                st.error("No articles found. Please try again with a different company name.")
            else:
                # Display article summaries and sentiment analysis
                st.subheader("Article Summaries and Sentiment Analysis")
                sentiment_results = []  # Store sentiment results for overall analysis
                articles_with_sentiment = []  # Store articles with API-generated summaries and sentiment scores

                for i, article in enumerate(articles, 1):
                    with st.expander(f"Article {i}: {article['title']}"):
                        st.write(f"**URL:** {article['url']}")
                        st.write(f"**Published Date:** {article['publish_date'] or 'Unknown date'}")
                        st.write(f"**Content Preview:** {article['content'][:200]}...")  # Show first 200 chars of content

                        # Perform sentiment analysis
                        with st.spinner(f"Analyzing sentiment for Article {i}..."):
                            sentiment_result = analyze_sentiment(company_name, article['content'])
                            
                            if sentiment_result:
                                st.write(f"**Sentiment Score:** {sentiment_result['Score']}")
                                st.write(f"**Sentiment:** {sentiment_result['Sentiment']}")
                                st.write(f"**Summary:** {sentiment_result['Summary']}")
                                st.write(f"**Keywords:** {', '.join(sentiment_result['Keywords'])}")
                                
                                # Store sentiment results for overall analysis
                                sentiment_results.append(sentiment_result)
                                
                                # Store article with API-generated summary and sentiment score
                                articles_with_sentiment.append({
                                    "Title": article['title'],
                                    "summary": sentiment_result['Summary'],
                                    "Sentiment": sentiment_result['Sentiment'],
                                    "sentiment_score": float(sentiment_result['Score']),
                                    "Topics": sentiment_result['Keywords']
                                })
                            else:
                                st.error("Failed to analyze sentiment for this article.")

                # Generate overall summary using API-generated summaries and sentiment scores
                if articles_with_sentiment:
                    st.subheader("Overall News Summary and Sentiment")
                    
                    # Generate overall summary
                    overall_summary = generate_overall_summary(company_name, articles_with_sentiment)
                    
                    if overall_summary:
                        st.write(f"**Overall Summary:** {overall_summary}")
                    else:
                        st.error("Failed to generate overall summary.")

                    # Calculate overall sentiment score
                    overall_score = sum(article['sentiment_score'] for article in articles_with_sentiment) / len(articles_with_sentiment)
                    overall_sentiment = "Positive" if overall_score > 0 else "Negative" if overall_score < 0 else "Neutral"
                    
                    st.write(f"**Overall Sentiment Score:** {overall_score:.2f}")
                    st.write(f"**Overall Sentiment:** {overall_sentiment}")

                    # Pie chart for sentiment distribution
                    st.subheader("Sentiment Distribution")
                    sentiment_counts = {
                        "Positive": sum(1 for article in articles_with_sentiment if article['sentiment_score'] > 0),
                        "Negative": sum(1 for article in articles_with_sentiment if article['sentiment_score'] < 0),
                        "Neutral": sum(1 for article in articles_with_sentiment if article['sentiment_score'] == 0)
                    }
                    
                    fig, ax = plt.subplots()
                    ax.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct='%1.1f%%', colors=['green', 'red', 'gray'])
                    
                    # Save the pie chart to a BytesIO object and store it in session state
                    img_buffer = io.BytesIO()
                    plt.savefig(img_buffer, format='png')
                    img_buffer.seek(0)
                    st.session_state.img_buffer = img_buffer
                    
                    # Display the pie chart
                    st.pyplot(fig)

                    # Comparative sentiment analysis
                    st.subheader("Comparative Sentiment Analysis")
                    st.write(f"Out of {len(articles_with_sentiment)} articles:")
                    st.write(f"- Positive: {sentiment_counts['Positive']}")
                    st.write(f"- Negative: {sentiment_counts['Negative']}")
                    st.write(f"- Neutral: {sentiment_counts['Neutral']}")
                    st.write(f"Main topics covered: " + ', '.join(set([topic for article in articles_with_sentiment for topic in article['Topics']])))

                    # Generate Hindi TTS and make it playable
                    if overall_summary:
                        st.subheader("Hindi Audio Summary")
                        with st.spinner("Generating Hindi audio summary..."):
                            audio_file = asyncio.run(translate_and_generate_audio("The overall sentiment score is "+str(round(overall_score, 2)) + overall_summary))
                            
                            if audio_file:
                                st.audio(audio_file, format="audio/mp3")
                                
                                # Store the audio file in session state
                                st.session_state.audio_file = audio_file
                            else:
                                st.error("Failed to generate Hindi audio summary.")

                    # Generate JSON report
                    json_report = {
                        "Company": company_name,
                        "Articles": articles_with_sentiment,
                        "Comparative Sentiment Score": {
                            "Sentiment Distribution": sentiment_counts,
                            "Topics": list(set([topic for article in articles_with_sentiment for topic in article['Topics']]))
                        },
                        "Final Sentiment Score:": round(overall_score, 2),
                        "Overall Summary": overall_summary
                    }
                    st.session_state.json_report = json_report

# Add download buttons outside the main form submission block
if st.session_state.img_buffer:
    st.subheader("Download Report")
    st.download_button(
        label="Download Pie Chart",
        data=st.session_state.img_buffer,
        file_name="sentiment_distribution.png",
        mime="image/png"
    )

if st.session_state.audio_file:
    with open(st.session_state.audio_file, "rb") as f:
        audio_bytes = f.read()
    st.download_button(
        label="Download Audio File",
        data=audio_bytes,
        file_name="hindi_audio_summary.mp3",
        mime="audio/mp3"
    )

if st.session_state.json_report:
    json_data = json.dumps(st.session_state.json_report, indent=4)
    st.download_button(
        label="Download JSON Report",
        data=json_data,
        file_name="sentiment_report.json",
        mime="application/json"
    )

# Display a message if no company name is entered
if not company_name:
    st.warning("Please enter a company name to generate the report.")
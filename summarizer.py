import os
import logging
from typing import List, Optional, Dict
from groq import Groq

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize Groq client
try:
    client = Groq(api_key="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")
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {str(e)}")
    raise

def generate_overall_summary(company: str, articles: List[Dict[str, str]]) -> Optional[str]:
    """
    Generate an overall summary by combining individual summaries and sentiment scores using an LLM API.
    
    Args:
        company (str): Name of the company
        articles (List[Dict[str, str]]): List of articles, each containing 'summary' and 'sentiment_score'
        
    Returns:
        str: Combined overall summary, including sentiment analysis
        None: If summarization fails
    """
    system_prompt = """You are a professional summarizer and sentiment analyst. The user will provide a company name and a list of news articles about the company. 
Each article includes a summary and a sentiment score (ranging from -1 to +1, where -1 is negative, close to 0 is neutral, and +1 is positive).
Your task is to combine these summaries into a single, concise, and coherent overall summary. 
The overall summary should:
1. Be 3-4 sentences long.
2. Include an analysis of the overall sentiment based on the individual sentiment scores.
3. Focus on the key points and themes across all relevant summaries.
4. Highlight the most important developments or news about the company.
5. Avoid redundancy and repetition.
6. Maintain a neutral and professional tone."""

    # Combine individual summaries and sentiment scores into a single input
    user_input = f"Company: {company}\n\nArticles:\n"
    for i, article in enumerate(articles, 1):
        user_input += f"{i}. Summary: {article['summary']}\n   Sentiment Score: {article['sentiment_score']}\n"

    try:
        completion = client.chat.completions.create(
            model="qwen-2.5-32b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        # Extract the generated overall summary
        overall_summary = completion.choices[0].message.content
        return overall_summary
        
    except Exception as e:
        logger.error(f"Failed to generate overall summary: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Test with sample data
    test_company = "Reliance Industries"
    test_articles = [
        {"summary": "Reliance Industries reported a 20% increase in profits this quarter.", "sentiment_score": 0.8},
        {"summary": "The company announced plans to expand into European markets.", "sentiment_score": 0.7},
        {"summary": "Reliance is facing criticism from environmental groups over its carbon emissions.", "sentiment_score": -0.5}
    ]
    
    result = generate_overall_summary(test_company, test_articles)
    if result:
        print("Overall Summary:")
        print(result)
    else:
        print("Failed to generate overall summary.")
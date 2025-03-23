# sentiment_analysis.py
import os
import json
import logging
from typing import Dict, Optional
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

def analyze_sentiment(company: str, article_content: str) -> Optional[Dict[str, str]]:
    """
    Analyze sentiment of a news article for a specific company using Mistral via Groq Cloud
    
    Args:
        company (str): Name of the company
        article_content (str): Full text content of the news article
        
    Returns:
        Dict[str, str]: Analysis result with keys: Score, Sentiment, Summary, Keywords
        None: If analysis fails
    """
    system_prompt = """You are a sentiment analysis model and summarizer. The user will give the company name and news article as input. 
You have to analyze the news concerning the company to generate the output. You need to determine whether the news affects the company positively or negatively. 
The output should be in JSON format:
{
    "Score": , 
    "Sentiment": , 
    "Summary": , 
    "Keywords": 
}
- Score must be in range [-1,+1] with 2 decimal places
- Sentiment must be Positive/Neutral/Negative based on score
- Summary should be 2-3 lines focusing on company impact
- Keywords should be 3-5 most important topics"""

    user_input = f"Company: {company}\nNews Article:\n{article_content}"

    try:
        completion = client.chat.completions.create(
            model="qwen-2.5-32b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=1024,
            response_format={"type": "json_object"}  # Ensure JSON output
        )

        response_text = completion.choices[0].message.content
        
        # Validate and parse JSON response
        result = json.loads(response_text)
        
        # Validate required fields
        required_fields = {"Score", "Sentiment", "Summary", "Keywords"}
        if not all(field in result for field in required_fields):
            raise ValueError("Missing required fields in response")
            
        # Validate score range
        if not -1 <= float(result["Score"]) <= 1:
            raise ValueError("Score out of valid range [-1, 1]")
            
        return result
        
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON response")
    except KeyError as e:
        logger.error(f"Missing key in response: {str(e)}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        
    return None

# Example usage
if __name__ == "__main__":
    # Test with sample data
    test_company = input("Enter a company name: ")
    test_article = input("Enter a sample news article: ")
    
    result = analyze_sentiment(test_company, test_article)
    if result:
        print("Analysis Result:")
        print(f"Score: {result['Score']}")
        print(f"Sentiment: {result['Sentiment']}")
        print(f"Summary: {result['Summary']}")
        print(f"Keywords: {', '.join(result['Keywords'])}")
    else:
        print("Failed to analyze sentiment")
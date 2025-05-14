import random
import praw
import csv
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import emoji
import config

# nltk stuff
nltk.download('punkt')
nltk.download('stopwords')


# api
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent)

# cleaning
def preprocess_content(content):
    # remove emojis
    content = emoji.replace_emoji(content, replace='')

    # remove special characters
    content = re.sub(r'\W', ' ', content)

    # tokenize
    tokens = word_tokenize(content.lower())

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return ' '.join(filtered_tokens)

def search_reddit():
    subreddits = ['suicidewatch', 'mentalhealth', 'depression'] # update subreddits for location
    keywords = ["depressed", "addiction help", "overwhelmed", "suicidal", 
                "hopeless", "mental health", "distress", "substance use", 
                "self harm", "anxiety", "depression", "crisis", "suicide prevention", 
                "therapy", "recovery"] 
    cities = ["New York","Los Angeles","San Francisco", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]

    search_query = ' OR '.join(keywords)

    with open('mental_health_posts.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post ID', 'Timestamp', 'Title', 'URL', 'Score', 'Content', 'City'])  # Added 'City' column  

        for subreddit in subreddits:
            print(f"Searching in r/{subreddit}...\n")
            for submission in reddit.subreddit(subreddit).search(search_query, limit=300):
                cleaned_content = preprocess_content(submission.selftext)
                
                # Randomly select a city from the cities list
                city = random.choice(cities)
                
                # Write row with the city information
                writer.writerow([submission.id, submission.created_utc, submission.title, submission.url, submission.score, cleaned_content, city])

                print(f"Title: {submission.title}")
                print(f"URL: {submission.url}")
                print(f"Score: {submission.score}")
                print(f"Created: {submission.created_utc}")
                print(f"Cleaned Content: {cleaned_content}")
                print(f"Assigned City: {city}\n")

if __name__ == "__main__":
    search_reddit()


## SECONDDDD

# import praw
# import csv
# import re
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# import emoji
# import config
# from datetime import datetime
# import time

# # Initialize NLTK
# nltk.download('punkt')
# nltk.download('stopwords')

# # Initialize Reddit API
# reddit = praw.Reddit(
#     client_id=config.client_id,
#     client_secret=config.client_secret,
#     user_agent=config.user_agent
# )

# # Target cities with common alternative names
# CITY_KEYWORDS = {
#     "New York": ["new york", "nyc", "manhattan"],
#     "Los Angeles": ["los angeles", "l.a."],
#     "Chicago": ["chicago", "chi-town"],
#     "Houston": ["houston", "htx"],
#     "Phoenix": ["phoenix"],
#     "Philadelphia": ["philadelphia", "philly"],
#     "San Antonio": ["san antonio"],
#     "San Diego": ["san diego"],
#     "Dallas": ["dallas", "dtx"],
#     "San Jose": ["san jose"],
#     "San Francisco": [" sf ", " sfo ", "san francisco"],
#     "Austin":[" austin ", "atx"]
# }

# # Mental health keywords
# MENTAL_HEALTH_KEYWORDS = [
#     "depressed", "suicidal", "hopeless", "mental health",
#     "distress", "self harm", "anxiety", "depression",
#     "crisis", "therapy", "recovery", "overwhelmed"
# ]

# def preprocess_content(content):
#     """Clean and preprocess text content"""
#     content = emoji.replace_emoji(content, replace='')
#     content = re.sub(r'\W', ' ', content)
#     tokens = word_tokenize(content.lower())
#     stop_words = set(stopwords.words('english'))
#     filtered_tokens = [word for word in tokens if word not in stop_words]
#     return ' '.join(filtered_tokens)

# def contains_city(text, city_keywords):
#     """Check if text contains any city reference"""
#     text = text.lower()
#     for city, keywords in city_keywords.items():
#         if any(keyword in text for keyword in keywords):
#             return city
#     return None

# def search_reddit_posts():
#     """Search Reddit for mental health posts with city references"""
#     subreddits = ['suicidewatch', 'mentalhealth', 'depression', 'anxiety', 'offmychest']
    
#     with open('mental_health_posts.csv', mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Post ID', 'Timestamp', 'City', 'Title', 'URL', 'Score', 'Content'])
        
#         post_count = 0
#         target_posts = 100
        
#         for subreddit in subreddits:
#             print(f"Searching in r/{subreddit}...")
            
#             try:
#                 # Search by each mental health keyword separately for better results
#                 for keyword in MENTAL_HEALTH_KEYWORDS:
#                     if post_count >= target_posts:
#                         break
                        
#                     print(f"  Searching for '{keyword}'...")
                    
#                     for submission in reddit.subreddit(subreddit).search(keyword, limit=100):
#                         if post_count >= target_posts:
#                             break
                            
#                         combined_text = f"{submission.title} {submission.selftext}".lower()
#                         city = contains_city(combined_text, CITY_KEYWORDS)
                        
#                         if city:
#                             cleaned_content = preprocess_content(submission.selftext)
#                             created_date = datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                            
#                             writer.writerow([
#                                 submission.id,
#                                 created_date,
#                                 city,
#                                 submission.title,
#                                 submission.url,
#                                 submission.score,
#                                 cleaned_content
#                             ])
                            
#                             post_count += 1
#                             print(f"    Found post #{post_count} from {city}")
                            
#                             # Show progress
#                             if post_count % 10 == 0:
#                                 print(f"Collected {post_count}/{target_posts} posts")
                            
#                         # Be gentle with the API
#                         time.sleep(1)
            
#             except Exception as e:
#                 print(f"Error searching r/{subreddit}: {e}")
#                 time.sleep(10)  # Wait longer if errors occur
    
#     print(f"\nFinished! Collected {post_count} posts in total.")

# if __name__ == "__main__":
#     search_reddit_posts()

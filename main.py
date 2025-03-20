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
    subreddits = ['suicidewatch', 'mentalhealth', 'depression'] 
    keywords = ["depressed", "addiction help", "overwhelmed", "suicidal", 
                "hopeless", "mental health", "distress", "substance use", 
                "self harm", "anxiety", "depression", "crisis", "suicide prevention", 
                "therapy", "recovery"]
    
    search_query = ' OR '.join(keywords)

    with open('mental_health_posts.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post ID', 'Timestamp', 'Title', 'URL', 'Score', 'Content'])  

        for subreddit in subreddits:
            print(f"Searching in r/{subreddit}...\n")
            for submission in reddit.subreddit(subreddit).search(search_query, limit=50):  
                cleaned_content = preprocess_content(submission.selftext)
                
                writer.writerow([submission.id, submission.created_utc, submission.title, submission.url, submission.score, cleaned_content])

                print(f"Title: {submission.title}")
                print(f"URL: {submission.url}")
                print(f"Score: {submission.score}")
                print(f"Created: {submission.created_utc}")
                print(f"Cleaned Content: {cleaned_content}\n")

if __name__ == "__main__":
    search_reddit()

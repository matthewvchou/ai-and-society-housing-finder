import praw
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()

def create_praw():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent="nyc-housing-finder by u/kphan5",
    )

    return reddit

def parse_neighborhood_url_mapping(neighborhood_url_mapping):
    all_neighborhoods = list(neighborhood_url_mapping.keys())
    all_neighborhoods = ','.join(all_neighborhoods).replace('-',' ').split(',')

    all_urls = list(neighborhood_url_mapping.values())
    return all_neighborhoods, all_urls

    return all_neighborhoods, all_urls

def search_asknyc(neighborhood_url_mapping):
    reddit = create_praw()
    subreddit = reddit.subreddit("asknyc")

    neighborhoods, urls = parse_neighborhood_url_mapping(neighborhood_url_mapping)

    for index, neighborhood in enumerate(neighborhoods):
        comments = []
        query = f"how is living in {neighborhood}"
        search_results = subreddit.search(query, sort="relevance", limit=1)
        post = next(search_results, None)

        if post:
            post.comments.replace_more(limit=0)

            top_comments = post.comments[:5]
            for comment in top_comments:
                comments.append(comment.body)
        
        ask_llm(neighborhood, comments, urls[index])


def ask_llm(neighborhood, comments, url):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        openai_api_key=os.getenv('OPEN_AI_SK'),
    )

    query = f"Give me an overall sentiment analysis based on these comments {'.'.join(comments)}. Please reference specific quotes/patterns in the comments."
    print(f"For the neighborhood {neighborhood}")
    response = llm([HumanMessage(content=query)])
    print(response.content)
    print(f"This is for {url}\n\n")
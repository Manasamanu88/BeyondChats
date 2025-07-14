import os
import praw
from dotenv import load_dotenv
import requests

# Load API keys from .env file
load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "user-persona-script")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Gemini REST API endpoint
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_username_from_url(url):
    """Extracts the Reddit username from a profile URL."""
    return url.rstrip('/').split('/')[-1]

def fetch_user_content(username, limit=50):
    """Fetches the latest posts and comments from a Reddit user."""
    user = reddit.redditor(username)
    posts = [post for post in user.submissions.new(limit=limit)]
    comments = [comment for comment in user.comments.new(limit=limit)]
    return posts, comments

def build_prompt(posts=None, comments=None, mode="both", username=None):
    """Builds a prompt for the LLM to generate a user persona with citations and the user's name."""
    if mode == "posts":
        prompt = (
            f"Given the following Reddit post by the user '{username}', build a user persona. "
            "Cite the post as evidence.\n\n"
        )
        for post in posts:
            prompt += f"Post: {post.title}\n{post.selftext}\nURL: https://reddit.com{post.permalink}\n\n"
    elif mode == "comments":
        prompt = (
            f"Given the following Reddit comment by the user '{username}', build a user persona. "
            "Cite the comment as evidence.\n\n"
        )
        for comment in comments:
            prompt += f"Comment: {comment.body}\nURL: https://reddit.com{comment.permalink}\n\n"
    else:
        prompt = (
            f"Given the following Reddit posts and comments by the user '{username}', build a user persona. "
            "For each characteristic, cite the post or comment used as evidence.\n\n"
        )
        for post in posts:
            prompt += f"Post: {post.title}\n{post.selftext}\nURL: https://reddit.com{post.permalink}\n\n"
        for comment in comments:
            prompt += f"Comment: {comment.body}\nURL: https://reddit.com{comment.permalink}\n\n"
    prompt += "User Persona (with citations and name):\n"
    return prompt

def generate_persona_rest(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def main():
    url = input("Enter Reddit user profile URL: ").strip()
    username = get_username_from_url(url)
    print(f"Fetching data for user: {username}")
    posts, comments = fetch_user_content(username, limit=10)
    posts = posts[:5]
    comments = comments[:5]

    # Personas from individual comments (up to 5)
    for idx, comment in enumerate(comments):
        prompt = build_prompt(comments=[comment], mode="comments", username=username)
        print(f"Generating persona from comment {idx+1}...")
        persona = generate_persona_rest(prompt)
        output_file = f"{username}_comment_{idx+1}_persona.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Citation:\nComment: {comment.body}\nURL: https://reddit.com{comment.permalink}\n\n--- Persona ---\n{persona}")
        print(f"Persona from comment {idx+1} saved to {output_file}")

    # Personas from individual posts (up to 5)
    for idx, post in enumerate(posts):
        prompt = build_prompt(posts=[post], mode="posts", username=username)
        print(f"Generating persona from post {idx+1}...")
        persona = generate_persona_rest(prompt)
        output_file = f"{username}_post_{idx+1}_persona.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Citation:\nPost: {post.title}\n{post.selftext}\nURL: https://reddit.com{post.permalink}\n\n--- Persona ---\n{persona}")
        print(f"Persona from post {idx+1} saved to {output_file}")

if __name__ == "__main__":
    main() 
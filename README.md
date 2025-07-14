# 🤖 Reddit User Persona Generator

This project generates detailed user personas for any Reddit user based on their latest posts and comments, using Google Gemini (Generative AI). It features a beautiful Streamlit web interface for easy use.

---

## Features
- Enter a Reddit user profile URL and generate personas for up to 5 posts and 5 comments(can be increased).
- Each persona includes clear citations (the exact post/comment and its URL) and the user's name.
- Download each persona as a text file.
- Modern, user-friendly web interface (Streamlit).

---

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with the following content:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
GEMINI_API_KEY=your_gemini_api_key
```
- Get Reddit API credentials from https://www.reddit.com/prefs/apps
- Get a Gemini API key from https://aistudio.google.com/app/apikey

---

## Usage

### Run the Web App
```
streamlit run app.py
```

### How to Use
1. Enter a Reddit user profile URL (e.g., `https://www.reddit.com/user/kojied/`).Here I used https://www.reddit.com/user/JEENEETards
2. Click **Generate Personas**.Wait for some time to generate the persona
3. The app will fetch up to 5 posts and 5 comments, generate a persona for each, and display them with citations.
4. Download any persona as a text file.

---

## Project Structure
- `reddit_user_persona.py` — Backend logic for fetching Reddit data and generating personas.
- `app.py` — Streamlit frontend for user interaction.
- `requirements.txt` — Python dependencies.
- `README.md` — This file.

---

## Troubleshooting
- Make sure your `.env` file is set up and contains valid API keys.
- If you get API errors, check your credentials and API quota.
- For any issues, check the terminal output for error messages.

---

For the  quick reference the personas are given in the text files.

## License
MIT License 

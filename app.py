import streamlit as st
import os
from reddit_user_persona import get_username_from_url, fetch_user_content, build_prompt, generate_persona_rest

# --- Custom CSS for a professional, bold, high-contrast look ---
st.markdown(
    """
    <style>
    .main, .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    .persona-card {
        background: #fff;
        border-radius: 1rem;
        box-shadow: 0 2px 16px rgba(0,0,0,0.10);
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-left: 6px solid #1e293b;
    }
    .persona-label {
        color: #1e293b;
        font-weight: 900;
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    .persona-card .persona-content {
        color: #111827 !important;
        font-weight: 700;
        font-size: 1.08rem;
        background: #f1f5f9;
        border-radius: 0.5rem;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
        word-break: break-word;
    }
    .stDownloadButton>button {
        background: linear-gradient(90deg, #1e293b 0%, #6366f1 100%);
        color: white;
        border-radius: 0.5rem;
        border: none;
        font-weight: 700;
        padding: 0.5rem 1.2rem;
        margin-top: 0.5rem;
        font-size: 1rem;
    }
    .stDownloadButton>button:hover {
        background: linear-gradient(90deg, #6366f1 0%, #1e293b 100%);
        color: #fff;
    }
    .stTextInput label, .stTextInput label span, .stTextInput label div {
        color: #1e293b !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px;
    }
    .stTextInput>div>div>input {
        background: #f1f5f9;
        border-radius: 0.5rem;
        border: 2px solid #1e293b;
        font-weight: 700;
        color: #1e293b !important;
        font-size: 1.1rem;
    }
    .stTextInput>div>div>input::placeholder {
        color: #334155 !important;
        opacity: 1 !important;
        font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1e293b 0%, #6366f1 100%);
        color: white;
        border-radius: 0.5rem;
        border: none;
        font-weight: 800;
        padding: 0.5rem 1.2rem;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #6366f1 0%, #1e293b 100%);
        color: #fff;
    }
    .stSpinner {
        color: #6366f1 !important;
    }
    .stCodeBlock code, .stCodeBlock pre {
        color: #1e293b !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        background: #f1f5f9 !important;
    }
    .stMarkdown .black-label {
        color: #1e293b !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px;
        margin-bottom: 0.2rem;
        display: block;
    }
    .custom-info {
        background: #e0e7ff;
        color: #1e293b !important;
        font-weight: 900;
        font-size: 1.1rem;
        border-radius: 0.5rem;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1.2rem;
        border-left: 6px solid #6366f1;
    }
    .custom-success {
        background: #d1fae5;
        color: #065f46 !important;
        font-weight: 900;
        font-size: 1.1rem;
        border-radius: 0.5rem;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1.2rem;
        border-left: 6px solid #10b981;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Bold, professional header ---
st.markdown(
    """
    <div style="text-align:center; margin-bottom:2.2rem;">
        <h1 style="color:#1e293b; font-weight:900; font-size:2.7rem; margin-bottom:0.2rem; letter-spacing:1px;">Reddit User Persona Generator</h1>
        <div style="font-size:1.18rem; color:#334155; font-weight:600;">
            Enter a Reddit user profile URL below. The app will generate personas for each post and comment with clear citations.<br>
            <span style="color:#6366f1; font-weight:700;">View and download each persona for your analysis or reporting needs.</span>
        </div>
    </div>
    <hr style="border:1.5px solid #1e293b; margin-bottom:2rem;"/>
    """,
    unsafe_allow_html=True)

# Custom label for the input
st.markdown('<span class="black-label">🔗  Reddit user profile URL</span>', unsafe_allow_html=True)
url = st.text_input(" ", "", help="Paste a Reddit user profile URL, e.g. https://www.reddit.com/user/kojied/")

if st.button("✨ Generate Personas") and url.strip():
    username = get_username_from_url(url)
    st.markdown(f'<div class="custom-info">Fetching data for user: <b>{username}</b></div>', unsafe_allow_html=True)
    try:
        posts, comments = fetch_user_content(username, limit=10)
        posts = posts[:5]
        comments = comments[:5]
        persona_results = []
        with st.spinner("Generating personas for comments..."):
            for idx, comment in enumerate(comments):
                prompt = build_prompt(comments=[comment], mode="comments", username=username)
                persona = generate_persona_rest(prompt)
                citation = f"Citation:\nComment: {comment.body}\nURL: https://reddit.com{comment.permalink}\n"
                persona_text = f"{citation}\n--- Persona ---\n{persona}"
                persona_results.append((f"Comment {idx+1}", persona_text, f"{username}_comment_{idx+1}_persona.txt"))
        with st.spinner("Generating personas for posts..."):
            for idx, post in enumerate(posts):
                prompt = build_prompt(posts=[post], mode="posts", username=username)
                persona = generate_persona_rest(prompt)
                citation = f"Citation:\nPost: {post.title}\n{post.selftext}\nURL: https://reddit.com{post.permalink}\n"
                persona_text = f"{citation}\n--- Persona ---\n{persona}"
                persona_results.append((f"Post {idx+1}", persona_text, f"{username}_post_{idx+1}_persona.txt"))
        if persona_results:
            st.markdown('<div class="custom-success">Personas generated!</div>', unsafe_allow_html=True)
        for label, persona_text, filename in persona_results:
            with st.container():
                st.markdown(f'<div class="persona-card"><div class="persona-label">{label}</div><div class="persona-content">', unsafe_allow_html=True)
                st.code(persona_text, language="markdown")
                st.download_button(f"Download {label} Persona", persona_text, file_name=filename)
                st.markdown('</div></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}") 
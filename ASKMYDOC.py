import streamlit as st
import fitz
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
import tempfile
import os
from streamlit_lottie import st_lottie
import json
import base64


# Page configuration
st.set_page_config(page_title="AskMyDoc", layout="wide", initial_sidebar_state="expanded")

# Constants
EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = "light"

# Load embedding model
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)

embedder = load_embedding_model()
embedding_dim = 384
index = faiss.IndexFlatL2(embedding_dim)
documents = []

# Load Lottie animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_robot = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_mdf1rre2.json")
lottie_upload = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_0pvjfvif.json")
lottie_search = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_nw19osms.json")

# Theme toggle function
def toggle_theme():
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

# Apply theme styling
def apply_theme():
    if st.session_state.theme == "light":
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        text_color = "#2b2d42"
        card_bg = "white"
        sidebar_bg = "#f8f9fa"
        accent_color = "#4cc9f0"
        primary_color = "#4361ee"
        secondary_color = "#3a0ca3"
        success_bg = "#d4edda"
        success_color = "#155724"
    else:
        bg_gradient = "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)"
        text_color = "#e6e6e6"
        card_bg = "#242a38"
        sidebar_bg = "#16213e"
        accent_color = "#0078e8"
        primary_color = "#4361ee"
        secondary_color = "#7579e7"
        success_bg = "#132b15"
        success_color = "#84cc6a"
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: {bg_gradient};
            background-attachment: fixed;
            background-size: cover;
        }}
        
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --accent-color: {accent_color};
            --text-color: {text_color};
            --card-bg: {card_bg};
            --sidebar-bg: {sidebar_bg};
            --success-bg: {success_bg};
            --success-color: {success_color};
        }}
        
        /* Card styling */
        .css-1r6slb0, .css-keje6w {{
            border-radius: 12px !important;
            box-shadow: 0 6px 16px rgba(0,0,0,0.1) !important;
            background-color: var(--card-bg) !important;
        }}
        
        /* Main page styling */
        .main-header {{
            color: var(--secondary-color);
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 3.2rem;
            margin-bottom: 0;
            text-align: center;
        }}
        
        .main-subheader {{
            color: var(--text-color);
            font-size: 1.2rem;
            opacity: 0.8;
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        /* Input styling */
        .stTextInput>div>div>input {{
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            padding: 1rem !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
            border: 1px solid #e0e0e0 !important;
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
        }}
        
        /* Button styling */
        .stButton>button {{
            background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            padding: 0.6rem 2rem !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(67, 97, 238, 0.3) !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(67, 97, 238, 0.4) !important;
        }}
        
        /* Answer box styling */
        .answer-box {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
            border-left: 5px solid var(--accent-color);
            color: var(--text-color);
        }}
        
        /* Sidebar styling */  
        .css-163ttbj, .css-1d391kg {{
            background-color: var(--sidebar-bg) !important;
        }}
        
        .sidebar-header {{
            color: var(--secondary-color);
            font-weight: 700;
            margin-top: 1rem;
        }}
        
        .sidebar-text {{
            color: var(--text-color);
            opacity: 0.9;
        }}
        
        /* File uploader */
        .uploadFile {{
            border: 2px dashed #c4c4c4 !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            text-align: center !important;
            background: var(--card-bg) !important;
            transition: all 0.3s ease !important;
        }}
        
        .uploadFile:hover {{
            border-color: var(--primary-color) !important;
        }}
        
        .stProgress > div > div > div {{
            background-color: var(--primary-color) !important;
        }}
        
        /* Success message */
        .success-message {{
            background-color: var(--success-bg);
            color: var(--success-color);
            padding: 1rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            margin: 1rem 0;
        }}
        
        .success-message svg {{
            margin-right: 0.5rem;
        }}
        
        /* Progress bar */
        .stProgress > div > div > div {{
            background-color: var(--primary-color);
        }}
        
        /* Divider */
        hr {{
            margin: 2rem 0;
            border-color: #e0e0e0;
        }}
        
        /* Theme toggle button */
        .theme-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            padding: 0.5rem;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background-color: var(--card-bg);
            border: 1px solid var(--accent-color);
            color: var(--text-color);
            transition: all 0.3s ease;
        }}
        
        .theme-toggle:hover {{
            transform: rotate(30deg);
        }}
        
        /* Footer styling */
        .footer {{
            text-align: center;
            opacity: 0.8;
            padding: 1rem 0;
            color: var(--text-color);
        }}
        
        p {{
            color: var(--text-color);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: var(--secondary-color);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply the theme
apply_theme()

# Utility functions
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return "".join([page.get_text() for page in doc])

def chunk_text(text, max_length=500):
    sentences = text.split('. ')
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_length:
            chunk += sentence + '. '
        else:
            chunks.append(chunk.strip())
            chunk = sentence + '. '
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def get_embedding(text):
    return embedder.encode(text)

def add_documents_to_faiss(docs):
    global documents
    embeddings = [doc['embedding'] for doc in docs]
    index.add(np.vstack(embeddings).astype('float32'))
    documents.extend(docs)

def search_faiss(query_embedding, top_k=5):
    D, I = index.search(np.array([query_embedding]).astype('float32'), top_k)
    return [documents[i] for i in I[0] if i < len(documents)]

def generate_answer(context, question):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.text}"

# Theme toggle button
theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
st.markdown(f"""
<button onclick="document.dispatchEvent(new CustomEvent('theme_toggle'));" class="theme-toggle">{theme_icon}</button>
<script>
document.addEventListener('theme_toggle', function() {{
    setTimeout(function() {{ 
        window.parent.document.querySelector('iframe[title="streamlit_theme_toggle"]').contentWindow.document.querySelector('button').click();
    }}, 100);
}});
</script>
""", unsafe_allow_html=True)

# Hidden button for theme toggle
st.markdown("<iframe title='streamlit_theme_toggle' style='display:none;'></iframe>", unsafe_allow_html=True)
if st.button("Toggle Theme", key="theme_toggle", help="Switch between light and dark mode"):
    toggle_theme()
    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown('<h1 class="sidebar-header">About AskMyDoc</h1>', unsafe_allow_html=True)
    
    if lottie_robot:
        st_lottie(lottie_robot, height=180, key="robot_animation")
    
    st.markdown('<p class="sidebar-text">AskMyDoc uses advanced AI to help you interact with your documents intelligently.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <ul class="sidebar-text">
        <li>Upload PDF files</li>
        <li>Ask questions in plain English</li>
        <li>Get accurate, context-aware answers</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-text">Built with Streamlit, FAISS & LLMs.</p>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="sidebar-header">Upload PDFs</h2>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose PDFs", 
        type="pdf", 
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not uploaded_files:
        if lottie_upload:
            st_lottie(lottie_upload, height=150, key="upload_animation", speed=0.7)

# Main content
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown('<h1 class="main-header">AskMyDoc</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subheader">Upload a PDF, ask questions, and get accurate answers</p>', unsafe_allow_html=True)

    main_container = st.container()
    
    with main_container:
        if uploaded_files:
            with st.spinner("Processing your documents..."):
                progress_bar = st.progress(0)
                total_files = len(uploaded_files)
                
                for i, uploaded_file in enumerate(uploaded_files):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    text = extract_text_from_pdf(tmp_path)
                    chunks = chunk_text(text)
                    docs = [{"text": chunk, "embedding": get_embedding(chunk)} for chunk in chunks]
                    add_documents_to_faiss(docs)
                    os.unlink(tmp_path)
                    progress_bar.progress((i + 1) / total_files)
                
                st.markdown(f"""
                <div class="success-message">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    <span>Successfully processed {len(uploaded_files)} file(s). Ready to answer your questions</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<h2 style="font-weight: 600; margin-top: 1.5rem;">Ask a Question</h2>', unsafe_allow_html=True)
        
        question = st.text_input("", placeholder="Type your question here...", key="question_input")
        
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            search_button = st.button("Get Answer")
        
        if search_button and question and documents:
            if lottie_search:
                st_lottie(lottie_search, height=120, key="search_animation", speed=1.2)
        
        if search_button:
            if not documents:
                st.error("Please upload at least one PDF first")
            elif not question.strip():
                st.warning("Please enter a question")
            else:
                with st.spinner("Finding the best answer for you..."):
                    query_embedding = get_embedding(question)
                    top_chunks = search_faiss(query_embedding)
                    combined_context = "\n\n".join([doc['text'] for doc in top_chunks])
                    answer = generate_answer(combined_context, question)
                    
                    st.markdown(f"""
                    <div class="answer-box">
                        <h3 style="margin-top: 0;">Answer:</h3>
                        <p style="font-size: 1.1rem; line-height: 1.6;">{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="footer">
            <p>Thank you for using AskMyDoc – Your AI-powered document assistant.</p>
            <p>MINI AI PROJECT – BY KHADIJA MUSKAN</p>
            <p>All Rights Reserved</p>
        </div>
        """, unsafe_allow_html=True)
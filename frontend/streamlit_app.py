"""
Streamlit frontend for ET News Copilot.
Interactive UI for article analysis, briefing, Q&A, and related articles.
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any
import time

# Page configuration
st.set_page_config(
    page_title="ET News Copilot",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
    }
    .briefing-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .article-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    .citation {
        background-color: #fff3cd;
        padding: 10px;
        border-left: 3px solid #ff9800;
        margin: 8px 0;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# Config
API_BASE_URL = "http://localhost:8000/api"
TIMEOUT = 30

def check_api_health() -> bool:
    """Check if API is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

@st.cache_data
def init_session_state():
    """Initialize session state"""
    if "article_text" not in st.session_state:
        st.session_state.article_text = ""
    if "persona" not in st.session_state:
        st.session_state.persona = "investor"
    if "briefing_result" not in st.session_state:
        st.session_state.briefing_result = None
    if "search_result" not in st.session_state:
        st.session_state.search_result = None
    if "qa_result" not in st.session_state:
        st.session_state.qa_result = None

def display_briefing(briefing_data: Dict[str, Any]):
    """Display briefing in organized format"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💡 What Happened?")
        st.write(briefing_data.get("what_happened", ""))
        
        st.markdown("### 👥 Who's Involved?")
        st.write(briefing_data.get("who_involved", ""))
    
    with col2:
        st.markdown("### 💰 Why It Matters?")
        st.write(briefing_data.get("why_it_matters", ""))
        
        st.markdown("### 🔮 What to Watch?")
        st.write(briefing_data.get("what_next", ""))

def display_related_articles(articles: list):
    """Display related articles"""
    if not articles:
        st.info("No related articles found")
        return
    
    st.markdown("### 📰 Related Articles")
    for article in articles:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{article.get('title', 'Untitled')}**")
                st.caption(f"{article.get('source', 'Unknown')} • {article.get('date', '')}")
            with col2:
                similarity = article.get('similarity_score', 0)
                st.metric("Match", f"{int(similarity*100)}%")

def display_qa_response(answer: str, citations: list):
    """Display Q&A response with citations"""
    st.markdown("### Answer")
    st.write(answer)
    
    if citations:
        st.markdown("### 📖 Sources")
        for citation in citations:
            with st.expander(f"📄 {citation.get('title', 'Source')}"):
                st.markdown(f"**Quote:** \"{citation.get('excerpt', '')}\"")
                st.caption(f"Relevance: {int(citation.get('relevance_score', 0)*100)}%")

# Main app
def main():
    init_session_state()
    
    # Header
    st.title("📰 ET News Copilot")
    st.markdown("Transform news articles into interactive insights powered by AI")
    
    # API Health Check
    if not check_api_health():
        st.error("⚠️ API server is not running. Start it with: `python -m uvicorn backend.main:app --reload`")
        return
    
    st.success("✓ API connected")
    
    # Sidebar for article input
    with st.sidebar:
        st.markdown("## Article Input")
        article_text = st.text_area(
            "Paste article text here:",
            value=st.session_state.article_text,
            height=200,
            key="article_input"
        )
        
        persona = st.selectbox(
            "Select persona:",
            ["investor", "student", "founder", "journalist"],
            index=0,
            key="persona_select"
        )
        
        st.session_state.article_text = article_text
        st.session_state.persona = persona
        
        st.markdown("---")
        
        # Quick info
        st.markdown("### About")
        st.caption(
            "ET News Copilot uses AI to transform static articles into "
            "interactive briefings with semantic search and Q&A capabilities."
        )
    
    # Check if article is provided
    if not article_text or len(article_text.strip()) < 50:
        st.info("👈 Enter an article in the sidebar to get started")
        st.markdown("""
        ## How it works:
        
        1. **Paste Article** - Copy any news article text in the sidebar
        2. **Select Persona** - Choose your role (Investor, Student, Founder, Journalist)
        3. **Get Briefing** - AI generates a smart 4-question briefing
        4. **Find Related Articles** - Discover similar news automatically
        5. **Ask Questions** - Query the article with AI-powered Q&A with citations
        """)
        return
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Briefing",
        "🔗 Related Articles",
        "❓ Q&A",
        "📈 Stats"
    ])
    
    with tab1:
        st.markdown(f"## Smart Briefing (for {persona.title()}s)")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("_AI is analyzing the article..._")
        with col2:
            generate_briefing = st.button("🚀 Generate Briefing", key="briefing_btn")
        
        if generate_briefing or st.session_state.briefing_result:
            if generate_briefing:
                with st.spinner("Analyzing article..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/briefing",
                            json={
                                "article_text": article_text,
                                "persona": persona
                            },
                            timeout=TIMEOUT
                        )
                        if response.status_code == 200:
                            st.session_state.briefing_result = response.json()
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Failed to generate briefing: {e}")
            
            if st.session_state.briefing_result and st.session_state.briefing_result.get("status") == "success":
                briefing = st.session_state.briefing_result.get("briefing", {})
                display_briefing(briefing)
                
                # Show related articles in briefing tab
                related = st.session_state.briefing_result.get("related_articles", [])
                if related:
                    st.markdown("---")
                    st.markdown("### 🔗 Top Related Articles")
                    for article in related:
                        st.markdown(f"• **{article.get('title', 'Article')}** ({int(article.get('similarity_score', 0)*100)}% match)")
    
    with tab2:
        st.markdown("## Find Related Articles")
        
        if st.button("🔍 Search Related Articles", key="search_btn"):
            with st.spinner("Searching..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/search-related",
                        json={
                            "article_text": article_text,
                            "limit": 5
                        },
                        timeout=TIMEOUT
                    )
                    if response.status_code == 200:
                        st.session_state.search_result = response.json()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Search failed: {e}")
        
        if st.session_state.search_result and st.session_state.search_result.get("status") == "success":
            articles = st.session_state.search_result.get("related_articles", [])
            if articles:
                st.markdown(f"Found {len(articles)} related articles:")
                display_related_articles(articles)
            else:
                st.info("No related articles found")
    
    with tab3:
        st.markdown("## Ask Questions About the Article")
        
        question = st.text_input(
            "Ask a question:",
            placeholder="e.g., How will this affect my startup valuation?",
            key="question_input"
        )
        
        if question and st.button("📝 Ask AI", key="qa_btn"):
            with st.spinner("Finding answer..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/ask-question",
                        json={
                            "question": question,
                            "article_text": article_text,
                            "use_related": True,
                            "max_sources": 3
                        },
                        timeout=TIMEOUT
                    )
                    if response.status_code == 200:
                        st.session_state.qa_result = response.json()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Q&A failed: {e}")
        
        if st.session_state.qa_result and st.session_state.qa_result.get("status") == "success":
            answer = st.session_state.qa_result.get("answer", "")
            citations = st.session_state.qa_result.get("citations", [])
            display_qa_response(answer, citations)
    
    with tab4:
        st.markdown("## Statistics & Info")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Article Length", f"{len(article_text)} chars")
        
        with col2:
            word_count = len(article_text.split())
            st.metric("Word Count", f"{word_count} words")
        
        with col3:
            try:
                response = requests.get(f"{API_BASE_URL}/db-stats")
                if response.status_code == 200:
                    stats = response.json()
                    st.metric("Database Articles", stats.get("total_articles", 0))
            except:
                st.metric("Database Articles", "N/A")
        
        st.markdown("---")
        st.markdown("### System Info")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**API Status:** ✓ Connected")
            st.markdown("**Model:** Mixtral-8x7b-32768")
        
        with col2:
            st.markdown("**Embeddings:** all-MiniLM-L6-v2")
            st.markdown("**Database:** ChromaDB")

if __name__ == "__main__":
    main()

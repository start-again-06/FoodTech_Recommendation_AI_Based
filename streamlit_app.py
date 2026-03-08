import streamlit as st
import pandas as pd
import os
import sys
import logging
from typing import List, Optional


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from phase2.input_validator import InputValidator
from phase2.models import UserInput
from phase4.recommender import LLMRecommender
from phase5.feedback_collector import FeedbackCollector
from phase1.main import Phase1Pipeline
from phase1.config import DATABASE_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Zomato AI - Best Eats in Bangalore",
    page_icon="🍴",
    layout="centered"
)

GLASS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    :root {
        --primary: #FF385C;
        --secondary: #2D2D2D;
        --bg-dark: #0F0F10;
        --text-main: #FFFFFF;
        --text-dim: rgba(255, 255, 255, 0.7);
        --accent-red: #FF385C;
    }

    /* Global Styles */
    .main {
        background-color: var(--bg-dark);
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: transparent !important;
        font-family: 'Outfit', sans-serif;
    }

    /* Background Blobs */
    .background-blobs {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -2 !important;
        overflow: hidden;
        filter: blur(80px);
        background-color: #0F0F10 !important;
    }

    .blob {
        position: absolute;
        border-radius: 50%;
        opacity: 0.4 !important;
        animation: move 25s infinite alternate;
    }

    .blob-1 {
        width: 900px;
        height: 900px;
        background: radial-gradient(circle, #FF385C 0%, transparent 70%) !important;
        top: -250px;
        right: -250px;
    }

    .blob-2 {
        width: 800px;
        height: 800px;
        background: radial-gradient(circle, #3b82f6 0%, transparent 70%) !important;
        bottom: -200px;
        left: -200px;
        animation-delay: -5s;
    }

    .blob-3 {
        width: 700px;
        height: 700px;
        background: radial-gradient(circle, #9629f0 0%, transparent 70%) !important;
        top: 20%;
        left: 30%;
        animation-delay: -12s;
    }

    @keyframes move {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(80px, 60px) scale(1.1); }
        100% { transform: translate(-40px, 30px) scale(1); }
    }

    /* Main Container Styles */
    .block-container {
        padding-top: 2.5rem !important;
        max-width: 1000px !important;
    }

    .main-header {
        text-align: center;
        margin-bottom: 15px;
        padding-top: 0px;
    }

    h1 {
        font-size: 4rem !important;
        font-weight: 800 !important;
        margin-bottom: 0px !important;
        color: white !important;
        letter-spacing: -1.5px;
    }

    .highlight {
        color: var(--primary);
    }

    .tagline {
        color: var(--text-dim);
        font-size: 1.3rem;
        font-weight: 400;
        margin-bottom: 25px;
    }

    .stats-bar {
        display: inline-flex;
        align-items: center;
        gap: 20px;
        background: rgba(255, 255, 255, 0.03);
        padding: 8px 25px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 40px;
        font-size: 1rem;
        color: var(--text-dim);
        margin-bottom: 30px;
    }

    .stat-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .stat-item span {
        color: var(--primary);
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Glassmorphism Cards */
    .glass-card, [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 28px !important;
        padding: 45px !important;
        box-shadow: 0 20px 60px 0 rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 40px !important;
    }

    /* Target the specific search container block to ensure it looks like a card */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stHorizontalBlock"]) {
        /* This selector is a bit aggressive but helps style the grouping container */
    }

    .input-label {
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
        opacity: 0.95;
    }

    /* Button specific styles to match the large red button in reference */
    .stButton > button {
        height: 60px !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #FF385C, #E23744) !important;
        border-radius: 16px !important;
        border: none !important;
        margin-top: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 56, 92, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 56, 92, 0.4) !important;
        opacity: 0.9 !important;
    }

    /* Restaurant Card specific Styles */
    .restaurant-card {
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .res-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 15px;
    }

    .res-name {
        font-size: 1.4rem;
        font-weight: 600;
        color: white;
    }

    .res-rating {
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 600;
    }

    .res-meta {
        color: var(--text-dim);
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    .res-meta p {
        margin-bottom: 5px;
    }

    .res-reasoning {
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid var(--primary);
        padding: 15px;
        border-radius: 0 12px 12px 0;
        font-size: 0.95rem;
        color: #e5e7eb;
        font-style: italic;
    }

    /* Streamlit Input Overrides */
    .stSelectbox, .stMultiSelect, .stNumberInput {
        background: transparent !important;
    }
    
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"]:hover {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(255, 56, 92, 0.3) !important;
    }

    .powered-by {
        text-align: center;
        padding: 40px 0;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8) !important;
        letter-spacing: 3px;
        font-weight: 700;
        text-transform: uppercase;
        width: 100%;
        display: block;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 50px;
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        h1 {
            font-size: 2.5rem !important;
            letter-spacing: -1px;
        }

        .tagline {
            font-size: 1rem;
            margin-bottom: 20px;
        }

        .stats-bar {
            flex-direction: column;
            gap: 5px;
            padding: 12px 20px;
            border-radius: 20px;
            width: 90%;
            margin-bottom: 20px;
        }

        .stat-separator {
            display: none;
        }

        .glass-card, [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 25px !important;
            border-radius: 20px !important;
            margin-bottom: 25px !important;
        }

        .input-label {
            font-size: 0.9rem;
            margin-bottom: 10px;
        }

        .stButton > button {
            height: 50px !important;
            font-size: 1.1rem !important;
        }

        .res-name {
            font-size: 1.2rem;
        }

        .powered-by {
            font-size: 0.8rem;
            letter-spacing: 1.5px;
            padding: 25px 0;
        }
        
        /* Slow down or simplify blobs for mobile performance */
        .background-blobs {
            filter: blur(60px);
        }
    }
</style>
"""

BLOBS_HTML = """
<div class="background-blobs">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
</div>
"""

def check_setup():
    """Ensures the database is ready for the app."""
    if not os.path.exists(DATABASE_PATH):
        st.info("Welcome! It looks like this is the first time you're running the app.")
        st.info("Setting up the Zomato Bangalore dataset... this will only take a moment.")
        
        with st.spinner("Downloading and processing data..."):
            try:
                pipeline = Phase1Pipeline()
                pipeline.run()
                st.success("Setup complete! Database is ready.")
                st.rerun() # Refresh to load the data
            except Exception as e:
                st.error(f"Failed to initialize database: {e}")
                st.stop()

def main():
    # Inject CSS and Background
    st.markdown(GLASS_CSS, unsafe_allow_html=True)
    st.markdown(BLOBS_HTML, unsafe_allow_html=True)

    # Initial Setup Check
    check_setup()

    # Load Data and Models
    validator = InputValidator()
    # Cache valid localities and cuisines
    if 'localities' not in st.session_state:
        st.session_state.localities = validator.get_valid_localities()
    if 'cuisines_list' not in st.session_state:
        # Filter out 'Cafe' and 'Unknown'
        raw_cuisines = validator.get_valid_cuisines()
        st.session_state.cuisines_list = [c for c in raw_cuisines if c not in ['Cafe', 'Unknown']]

    recommender = LLMRecommender()
    feedback_collector = FeedbackCollector()

    # Header Section
    st.markdown(f"""
    <div class="main-header">
        <h1>Zomato AI <span class="highlight">Recommender</span></h1>
        <p class="tagline">Helping you find the best places to eat in <span class="highlight">Bangalore</span> city</p>
        <div class="stats-bar">
            <span class="stat-item"><span>{len(st.session_state.localities)}</span> Localities</span>
            <span class="stat-separator">|</span>
            <span class="stat-item">🍴 <span>{len(st.session_state.cuisines_list)}</span> Cuisines</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search Form Section
    # We use a container and style it via CSS to avoid the "empty div" issue caused by unclosed HTML blocks
    search_container = st.container()
    with search_container:
        # Row 1: Locality and Price Range
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            st.markdown('<div class="input-label">Select locality *</div>', unsafe_allow_html=True)
            city = st.selectbox(
                "Select locality *",
                options=[""] + st.session_state.localities,
                format_func=lambda x: "Select locality..." if x == "" else x,
                index=0,
                label_visibility="collapsed"
            )
            
        with row1_col2:
            st.markdown('<div class="input-label">💰 Price Range *</div>', unsafe_allow_html=True)
            price_range = st.selectbox(
                "Price Range *",
                options=["", "budget", "mid-range", "premium"],
                format_func=lambda x: {
                    "": "Select price range...",
                    "budget": "Budget (₹ < 500)",
                    "mid-range": "Mid-range (₹500 - ₹1500)",
                    "premium": "Premium (₹ > 1500)"
                }.get(x),
                index=0,
                label_visibility="collapsed"
            )

        # Row 2: Cuisines and Min Rating
        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            st.markdown('<div class="input-label">🍴 Cuisines (Multi-select)</div>', unsafe_allow_html=True)
            cuisines = st.multiselect(
                "Cuisines (Multi-select)",
                options=st.session_state.cuisines_list,
                placeholder="Select cuisines...",
                label_visibility="collapsed"
            )

        with row2_col2:
            st.markdown('<div class="input-label">⭐ Min Rating</div>', unsafe_allow_html=True)
            min_rating = st.number_input(
                "Min Rating",
                min_value=0.0,
                max_value=5.0,
                value=0.0,
                step=0.1,
                format="%.1f",
                label_visibility="collapsed"
            )

        st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
        submit_clicked = st.button("Get Recommendations ✨", use_container_width=True)

    # Results Section
    if submit_clicked:
        if not city:
            st.error("Locality is required! Please select a locality to continue.")
        elif not price_range:
            st.error("Price Range is required! Please select a price range to continue.")
        else:
            with st.spinner("Asking the AI for the best spots..."):
                try:
                    # Prepare input
                    user_input = UserInput(
                        city=city,
                        price_range=price_range,
                        cuisine=cuisines if cuisines else None,
                        min_rating=min_rating
                    )
                    
                    # Fetch recommendations from Phase 3 (engine)
                    engine_response = recommender.engine.get_recommendations(user_input, limit=5)
                    
                    if engine_response.count == 0:
                        st.info(f"I'm sorry, but I couldn't find any restaurants in {city} matching your criteria.")
                    else:
                        # Get AI Reasoning Summary
                        ai_summary = recommender.generate_ai_summary(user_input, engine_response.recommendations)
                        
                        # Display Summary
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 4px solid var(--accent-purple);">
                            <p style="color: #e5e7eb; font-style: italic; font-size: 1.1rem;">{ai_summary}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display Cards in columns
                        cols = st.columns(2)
                        for i, rec in enumerate(engine_response.recommendations):
                            # Generate reasoning if not present (Phase 3 recs don't have reasoning, but LLMRecommender can add it)
                            reasoning = recommender.get_individual_reasoning(user_input, rec)
                            clean_reasoning = reasoning.replace("Why you'll like it:", "<strong>Why you'll like it:</strong>")
                            
                            with cols[i % 2]:
                                st.markdown(f"""
                                <div class="glass-card restaurant-card">
                                    <div class="res-header">
                                        <div class="res-name">{rec.name}</div>
                                        <span class="res-rating">{rec.rating} ★</span>
                                    </div>
                                    <div class="res-meta">
                                        <p>🍴 {rec.cuisines}</p>
                                        <p>💰 Avg. ₹{rec.average_cost} for two</p>
                                        <p>📍 {rec.address}</p>
                                    </div>
                                    <div class="res-reasoning">
                                        {clean_reasoning}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
                    logger.error(f"Error in streamlit_app: {e}", exc_info=True)

    # Footer
    st.markdown("""
    <div class="powered-by">
        POWERED BY GROQ AI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

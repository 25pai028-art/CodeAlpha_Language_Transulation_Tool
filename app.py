import streamlit as st
from googletrans import Translator
from gtts import gTTS
import tempfile
from database import *
from sentiment import *
from pdf_generator import *
from sentiment import analyze_sentiment
from pdf_generator import generate_pdf

# Custom CSS styling
st.markdown("""
    <style>
        :root {
            --primary-color: #5a5fe0;
            --secondary-color: #764ba2;
            --accent-color: #ec4899;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        * {
            margin: 0;
            padding: 0;
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 100%);
            min-height: 100vh;
        }
        
        [data-testid="stAppViewContainer"] {
            padding: 2rem 1rem;
        }
        
        .main {
            background: #ffffff;
            border-radius: 20px;
            padding: 2rem;
        }
        
        h1 {
            background: linear-gradient(135deg, #2d2f7e 0%, #5a3a8f 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.2rem;
            font-weight: 900;
            margin-bottom: 1.5rem;
            text-align: center;
            letter-spacing: 1px;
        }
        
        h2 {
            color: #2d2f7e;
            font-size: 2.1rem;
            margin-top: 1.8rem;
            margin-bottom: 1.2rem;
            padding-bottom: 0.5rem;
            font-weight: 900;
            letter-spacing: 0.8px;
        }
        
        h3 {
            color: #2d2f7e !important;
            font-size: 1.4rem !important;
            font-weight: 800 !important;
        }
        
        h4 {
            color: #1a1a2e !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }
        
        body, p, div {
            color: #1a1a2e !important;
            font-size: 1rem;
        }
        
        .stTextArea textarea {
            border-radius: 10px !important;
            border: 2px solid #667eea !important;
            font-size: 1.05rem !important;
            padding: 1rem !important;
            color: #1a1a2e !important;
            font-weight: 500 !important;
        }
        
        .stSelectbox select {
            border-radius: 10px !important;
            border: 2px solid #667eea !important;
            font-size: 1rem !important;
            color: #1a1a2e !important;
            font-weight: 600 !important;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-size: 1.2rem !important;
            font-weight: 900 !important;
            padding: 0.85rem 2rem !important;
            transition: transform 0.2s, box-shadow 0.2s !important;
            letter-spacing: 0.5px !important;
        }
        
        .stButton button * {
            color: white !important;
        }
        
        .stButton button p {
            color: white !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        [data-testid="stDownloadButton"] button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: 900 !important;
            font-size: 1.1rem !important;
            border-radius: 10px !important;
        }
        
        [data-testid="stDownloadButton"] button * {
            color: white !important;
        }
        
        [data-testid="stDownloadButton"] {
            background: transparent !important;
            border: none !important;
        }
        
        .stDownloadButton, .stDownloadButton button, .stDownloadButton button span, .stDownloadButton button div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: 900 !important;
            font-size: 1.1rem !important;
            border: none !important;
            border-radius: 10px !important;
        }
        
        .stDownloadButton button *, .stDownloadButton * {
            color: white !important;
            background: transparent !important;
        }
        
        .stSuccess {
            background-color: rgba(34, 197, 94, 0.15) !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            color: #15803d !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
        }
        
        .stWarning {
            background-color: rgba(249, 115, 22, 0.15) !important;
            border: 2px solid #ff9800 !important;
            border-radius: 10px !important;
            color: #d97706 !important;
            font-weight: 700 !important;
        }
        
        .stInfo {
            background-color: rgba(59, 130, 246, 0.15) !important;
            border: 2px solid #3b82f6 !important;
            border-radius: 10px !important;
            color: #1e40af !important;
            font-weight: 700 !important;
        }
        
        .container-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 5px solid #667eea;
            color: #1a1a2e !important;
        }
        
        p {
            color: #1a1a2e !important;
            font-size: 1.05rem !important;
            font-weight: 500 !important;
        }
    </style>
""", unsafe_allow_html=True)

translator = Translator()

create_db()

st.markdown("<h1>🌍 AI Language Translator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #2d2f7e; font-size: 1.25rem; margin-bottom: 2rem; font-weight: 700;'>Translate, Analyze & Convert Text Across Languages</p>", unsafe_allow_html=True)

languages = {
    "English":"en",
    "Hindi":"hi",
    "Gujarati":"gu",
    "French":"fr",
    "German":"de",
    "Spanish":"es"
}

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color: #2d2f7e;'>📝 Enter Text</h3>", unsafe_allow_html=True)
    text = st.text_area(
        "Enter Text to Translate",
        height=150,
        placeholder="Type or paste text here..."
    )

with col2:
    st.markdown("<h3 style='color: #2d2f7e;'>🎯 Select Target</h3>", unsafe_allow_html=True)
    target = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Translate Now", use_container_width=True):
    if not text.strip():
        st.warning("⚠️ Please enter some text to translate!")
    else:
        detected = translator.detect(text)
        translated = translator.translate(
            text,
            dest=languages[target]
        )
        
        save_translation(
            text,
            translated.text,
            detected.lang,
            target
        )
        
        st.success("✅ Translated Successfully!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h4>🗣️ Detected</h4>
                    <h3 style='color: #fbbf24; margin-top: 0.5rem;'>{detected.lang.upper()}</h3>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h4>🎯 Target</h4>
                    <h3 style='color: #fbbf24; margin-top: 0.5rem;'>{target.upper()}</h3>
                </div>
            """, unsafe_allow_html=True)
        
        sentiment_before = analyze_sentiment(text)
        sentiment_after = analyze_sentiment(translated.text)
        
        with col3:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h4>💭 Sentiment Match</h4>
                    <h3 style='color: #fbbf24; margin-top: 0.5rem;'>{sentiment_before == sentiment_after and "✅" or "⚠️"}</h3>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Original Text
        st.markdown("<h2>📖 Original Text</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background: #f5f7fa; border-left: 5px solid #667eea; 
                        padding: 1.5rem; border-radius: 8px; font-size: 1.1rem; line-height: 1.6;'>
                {text}
            </div>
        """, unsafe_allow_html=True)
        
        # Translated Text
        st.markdown("<h2>🌐 Translated Text</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background: #f5f7fa; border-left: 5px solid #764ba2; 
                        padding: 1.5rem; border-radius: 8px; font-size: 1.1rem; line-height: 1.6;'>
                {translated.text}
            </div>
        """, unsafe_allow_html=True)
        
        # Sentiment Analysis
        st.markdown("<h2>😊 Sentiment Analysis</h2>", unsafe_allow_html=True)
        sent_col1, sent_col2 = st.columns(2)
        
        with sent_col1:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white;'>
                    <h4>Original Text Sentiment</h4>
                    <h3 style='margin-top: 0.5rem;'>{sentiment_before}</h3>
                </div>
            """, unsafe_allow_html=True)
        
        with sent_col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white;'>
                    <h4>Translated Text Sentiment</h4>
                    <h3 style='margin-top: 0.5rem;'>{sentiment_after}</h3>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Audio
        st.markdown("<h2>🔊 Listen to Translation</h2>", unsafe_allow_html=True)
        tts = gTTS(translated.text)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            st.audio(f.name)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # PDF Download
        st.markdown("<h2>📄 Download Report</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        pdf = generate_pdf(
            text,
            translated.text,
            detected.lang,
            target,
            sentiment_before,
            sentiment_after
        )
        
        with open(pdf, "rb") as file:
            col_download = st.columns([1])[0]
            with col_download:
                st.download_button(
                    "📥 Download Professional PDF",
                    file,
                    file_name="translation_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

st.markdown("<br>", unsafe_allow_html=True)

# History Section
st.markdown("<h2>📚 Translation History</h2>", unsafe_allow_html=True)
history = get_history()

if history:
    for row in history:
        st.markdown(f"""
            <div style='background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                        border-left: 4px solid #667eea; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                <strong>{row[3]} ➜ {row[4]}</strong><br>
                <small style='color: #666;'>{row[1][:50]}...</small>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("📭 No translations yet. Start by entering some text!")

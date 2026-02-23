import streamlit as st
import pandas as pd
import re
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sentiment_analyzer import SentimentAnalyzer
from youtube_client import YouTubeClient
from utils import clean_text

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="YouTube Sentiment AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- VIDEO ID EXTRACTOR ----------------
def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# ---------------- GLASS FUTURISTIC CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
}

h1 {
    text-align: center;
    font-size: 2.8rem;
    background: linear-gradient(90deg,#ff4d4d,#ff0000);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stButton>button {
    background: linear-gradient(90deg,#ff4d4d,#ff0000);
    color: white;
    border-radius: 30px;
    height: 3em;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px red;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>🚀 YouTube Sentiment Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### AI Powered Comment Analytics Platform")
st.markdown("---")

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    api_key = st.text_input("🔑 Enter YouTube API Key", type="password")

with col2:
    video_url = st.text_input("📺 Enter YouTube Video URL")

st.markdown("---")

# ---------------- RUN ANALYSIS ----------------
if st.button("🚀 Run AI Analysis"):

    if not api_key or not video_url:
        st.warning("⚠ Please enter API Key and Video URL")
    else:
        video_id = extract_video_id(video_url)

        if not video_id:
            st.error("❌ Invalid YouTube URL")
        else:

            # 🎥 LIVE VIDEO EMBED
            st.markdown("## 🎥 Live Video")
            video_embed_url = f"https://www.youtube.com/embed/{video_id}"
            st.markdown(
                f"""
                <iframe width="100%" height="400"
                src="{video_embed_url}"
                frameborder="0"
                allowfullscreen>
                </iframe>
                """,
                unsafe_allow_html=True
            )

            with st.spinner("⚡ Running AI Analysis..."):
                yt_client = YouTubeClient(api_key)
                df_comments = yt_client.get_video_comments(video_id)

                if df_comments is None or df_comments.empty:
                    st.error("❌ Could not fetch comments.")
                else:
                    df_comments['text'] = df_comments['text'].apply(clean_text)

                    analyzer = SentimentAnalyzer()
                    df_results = analyzer.perform_analysis(df_comments, method='vader')

                    positive = (df_results['sentiment'] == 'Positive').sum()
                    negative = (df_results['sentiment'] == 'Negative').sum()
                    neutral = (df_results['sentiment'] == 'Neutral').sum()

                    # ---------------- METRICS ----------------
                    m1, m2, m3 = st.columns(3)
                    m1.metric("😊 Positive", positive)
                    m2.metric("😐 Neutral", neutral)
                    m3.metric("😡 Negative", negative)

                    # ---------------- INTERACTIVE BAR CHART ----------------
                    st.markdown("## 📊 Sentiment Distribution")

                    chart_df = pd.DataFrame({
                        "Sentiment": ["Positive", "Neutral", "Negative"],
                        "Count": [positive, neutral, negative]
                    })

                    fig_bar = px.bar(
                        chart_df,
                        x="Sentiment",
                        y="Count",
                        color="Sentiment",
                        color_discrete_sequence=["#00ff99","#ffd11a","#ff4d4d"],
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig_bar, use_container_width=True)

                    # ---------------- PIE CHART ----------------
                    fig_pie = px.pie(
                        chart_df,
                        names="Sentiment",
                        values="Count",
                        color_discrete_sequence=["#00ff99","#ffd11a","#ff4d4d"],
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig_pie, use_container_width=True)

                    # ---------------- COMMENT TIMELINE ----------------
                    st.markdown("## 📈 Comment Timeline Analysis")

                    df_results['published_at'] = pd.to_datetime(df_results['published_at'])
                    timeline = df_results.groupby(
                        df_results['published_at'].dt.date
                    ).size().reset_index(name='count')

                    fig_time = px.line(
                        timeline,
                        x='published_at',
                        y='count',
                        markers=True,
                        template="plotly_dark"
                    )

                    fig_time.update_layout(
                        title="Comments Over Time",
                        xaxis_title="Date",
                        yaxis_title="Number of Comments"
                    )

                    st.plotly_chart(fig_time, use_container_width=True)

                    # ---------------- WORD CLOUD ----------------
                    st.markdown("## ☁ Trending Keywords")

                    all_text = " ".join(df_results['text'])
                    wordcloud = WordCloud(
                        width=800,
                        height=400,
                        background_color='black',
                        colormap='Reds'
                    ).generate(all_text)

                    fig_wc, ax_wc = plt.subplots(figsize=(10,5))
                    ax_wc.imshow(wordcloud, interpolation='bilinear')
                    ax_wc.axis("off")
                    st.pyplot(fig_wc)

                    # ---------------- POSITIVE vs NEGATIVE WORDS ----------------
                    st.markdown("## 🔥 Positive vs Negative Keywords")

                    positive_text = " ".join(
                        df_results[df_results['sentiment'] == 'Positive']['text']
                    )

                    negative_text = " ".join(
                        df_results[df_results['sentiment'] == 'Negative']['text']
                    )

                    colP, colN = st.columns(2)

                    with colP:
                        st.subheader("😊 Positive Words")
                        if positive_text:
                            wc_pos = WordCloud(
                                width=400,
                                height=300,
                                background_color='black',
                                colormap='Greens'
                            ).generate(positive_text)

                            fig_pos, ax_pos = plt.subplots(figsize=(5,3))
                            ax_pos.imshow(wc_pos, interpolation='bilinear')
                            ax_pos.axis("off")
                            st.pyplot(fig_pos)

                    with colN:
                        st.subheader("😡 Negative Words")
                        if negative_text:
                            wc_neg = WordCloud(
                                width=400,
                                height=300,
                                background_color='black',
                                colormap='Reds'
                            ).generate(negative_text)

                            fig_neg, ax_neg = plt.subplots(figsize=(5,3))
                            ax_neg.imshow(wc_neg, interpolation='bilinear')
                            ax_neg.axis("off")
                            st.pyplot(fig_neg)

                    # ---------------- AI SUMMARY ----------------
                    st.markdown("## 🤖 AI Insight Summary")

                    total = positive + negative + neutral
                    pos_percent = (positive/total)*100 if total else 0
                    neg_percent = (negative/total)*100 if total else 0

                    if pos_percent > neg_percent:
                        summary = "Audience sentiment is largely POSITIVE. Viewers are responding very well."
                    elif neg_percent > pos_percent:
                        summary = "Audience sentiment is mostly NEGATIVE. Improvements may be needed."
                    else:
                        summary = "Audience sentiment is balanced with mixed reactions."

                    st.success(summary)

                    # ---------------- DOWNLOAD ----------------
                    csv = df_results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "⬇ Download Full Report",
                        csv,
                        "sentiment_report.csv",
                        "text/csv"
                    )
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_vader(self, text):
        """
        Analyzes text using VADER.
        Returns compound score and sentiment label.
        """
        if not text:
            return 0, 'Neutral'
            
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            sentiment = 'Positive'
        elif compound <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        return compound, sentiment

    def analyze_textblob(self, text):
        """
        Analyzes text using TextBlob.
        Returns polarity and sentiment label.
        """
        if not text:
            return 0, 'Neutral'

        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0:
            sentiment = 'Positive'
        elif polarity < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        return polarity, sentiment

    def perform_analysis(self, df, method='vader'):
        """
        Applies sentiment analysis to a DataFrame.
        """
        if df is None or df.empty:
            return df
        
        if method == 'vader':
            df[['sentiment_score', 'sentiment']] = df['text'].apply(
                lambda x: pd.Series(self.analyze_vader(x))
            )
        elif method == 'textblob':
             df[['sentiment_score', 'sentiment']] = df['text'].apply(
                lambda x: pd.Series(self.analyze_textblob(x))
            )
            
        return df

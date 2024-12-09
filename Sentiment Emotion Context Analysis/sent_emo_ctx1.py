"""current2.py: A Streamlit-based app named 'Sentiment, Emotion, Context' for generating color PDF outputs.
This script integrates NLP and visualization tools for data processing.
Note: API keys are currently hard-coded. Update to use environment variables for production."""

import streamlit as st
import pandas as pd
import plotly.express as px
import logging
import torch
from transformers import pipeline, AutoTokenizer, BartForConditionalGeneration
import anthropic
from typing import Tuple
from datetime import datetime
from dotenv import load_dotenv
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import base64
import numpy as np  # Added to handle numpy errors

# Load environment variables
load_dotenv()

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

class SentimentEmotionAnalyzer:
    VALID_SENTIMENTS = {'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'ERROR'}
    EMOTIONS = {
        'Positive': [
            'Happy', 'Joyful', 'Content', 'Satisfied', 'Pleased', 'Grateful', 'Excited', 
            'Thrilled', 'Ecstatic', 'Elated', 'Proud', 'Hopeful', 'Optimistic', 'Inspired',
            'Amused', 'Delighted', 'Cheerful', 'Confident', 'Love', 'Affectionate', 'Warm'
        ],
        'Negative': [
            'Sad', 'Unhappy', 'Depressed', 'Disappointed', 'Frustrated', 'Angry', 'Furious',
            'Irritated', 'Annoyed', 'Jealous', 'Envious', 'Guilty', 'Ashamed', 'Regretful',
            'Fearful', 'Anxious', 'Worried', 'Nervous', 'Scared', 'Terrified', 'Lonely',
            'Embarrassed', 'Humiliated', 'Disgusted', 'Bitter', 'Displeased', 'Upset'
        ],
        'Complex': [
            'Nostalgic', 'Ambiguous', 'Ambivalent', 'Overwhelmed', 'Conflicted', 'Bored',
            'Curious', 'Surprised', 'Astonished', 'Shocked', 'Relieved', 'Skeptical',
            'Cynical', 'Meditative', 'Thoughtful', 'Introspective', 'Guarded', 'Vulnerable'
        ],
        'Neutral': [
            'Indifferent', 'Apathetic', 'Neutral', 'Unconcerned', 'Calm', 'Serene',
            'Contented', 'Poised', 'Stable', 'Balanced'
        ]
    }

    # Flatten this dictionary into a single list of all emotions
    VALID_EMOTIONS = [emotion for category in EMOTIONS.values() for emotion in category]
    # Create a string of emotions for use in prompts or other contexts
    emotions_str = ", ".join(VALID_EMOTIONS)

    def __init__(self, emotion_provider='anthropic'):
        self.emotion_provider = emotion_provider
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            self.hf_pipe = pipeline(
                "text-classification", 
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=self.device
            )
            self.summarization_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
            self.summarization_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn").to(self.device)
            if emotion_provider == 'anthropic':
                self.client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
            logger.info(f"SentimentEmotionAnalyzer initialized with {emotion_provider}")
        except Exception as e:
            logger.error(f"Error initializing analyzer: {str(e)}")
            raise

    def analyze_text(self, text: str) -> Tuple[str, str]:
        """Analyze text for sentiment and emotion."""
        try:
            sentiment = self._get_sentiment(text)
            emotion = self._get_emotion(text) if sentiment != "ERROR" else "ERROR"
            return sentiment, emotion
        except Exception as e:
            logger.error(f"Error in analyze_text: {str(e)}")
            return "ERROR", "ERROR"

    def _get_sentiment(self, text: str) -> str:
        """Get sentiment using Hugging Face pipeline."""
        try:
            result = self.hf_pipe(text)[0]
            return result["label"].upper()
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return "ERROR"

    def _get_emotion(self, text: str) -> str:
        """Get emotion using selected provider."""
        prompt = f"""Analyze this text's emotion and respond with exactly ONE word from this list: {self.emotions_str}
Important rules:
1. You MUST choose one of these exact words, nothing else.
2. For unclear or ambiguous cases, do not default to 'Void' or 'Neutral'. Instead, choose the emotion that most closely matches the text's tone.
3. Even slight emotional signals should be classified as that specific emotion.
4. The exception to this is if the text is purely factual, in which case write "unapplicable".
**Examples:**
- **Text:** "I am so thrilled about the new project!"
- **Response:** Thrilled
- **Text:** "This movie made me feel so conflicted."
- **Response:** Conflicted
- **Text:** "I'm just really annoyed by this constant noise."
- **Response:** Annoyed
- **Text:** "The weather report says it will rain tomorrow."
- **Response:** unapplicable (No emotional content, purely factual)
- **Text:** "I'm a bit skeptical about these claims."
- **Response:** Skeptical (Even though it's subtle, there's an indication of doubt)
Text to analyze: {text}
Respond with just ONE word from the list."""
        try:
            if self.emotion_provider == 'anthropic':
                message = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=15,
                    temperature=0,
                    messages=[{"role": "user", "content": prompt}]
                )
                # Correctly handle the response format from Anthropic
                emotion = message.content[0].text if isinstance(message.content, list) and len(message.content) > 0 else "unapplicable"
                # Strict validation - must be exact match
                if emotion in self.VALID_EMOTIONS:
                    return emotion
                elif emotion.lower() == "unapplicable":
                    return "unapplicable"
                # If no match, analyze sentiment to choose appropriate emotion
                sentiment = self._get_sentiment(text)
                if sentiment == 'NEGATIVE':
                    return 'Angry'  # or another negative emotion
                elif sentiment == 'POSITIVE':
                    return 'Happy'  # or another positive emotion
                else:
                    return 'unapplicable'  # Changed to match the prompt's instruction
        except Exception as e:
            logger.error(f"Emotion analysis error: {str(e)}")
            return "unapplicable"

    def generate_analysis_summary(self, df: pd.DataFrame) -> str:
        """Generate a comprehensive summary of the analysis results."""
        try:
            total_entries = len(df)
            sentiment_counts = df['Sentiment'].value_counts()
            emotion_counts = df['Emotion'].value_counts()
            sentiment_percentages = (sentiment_counts / total_entries * 100).round(1)
            top_emotions = emotion_counts.head(3)
            top_emotions_percent = (top_emotions / total_entries * 100).round(1)
            
            # Handle potential numpy.int64 type issues:
            dominant_sentiment = str(sentiment_counts.index[0]) if isinstance(sentiment_counts.index[0], np.int64) else sentiment_counts.index[0]
            most_common_emotion = str(emotion_counts.index[0]) if isinstance(emotion_counts.index[0], np.int64) else emotion_counts.index[0]
            
            summary = f"""Analysis Summary of {total_entries} Entries:
Sentiment Distribution:
{' | '.join([f"{sent}: {pct}%" for sent, pct in sentiment_percentages.items()])}
Top 3 Emotions:
{' | '.join([f"{emotion}: {pct}%" for emotion, pct in top_emotions_percent.items()])}
Key Insights:
- The dominant sentiment is {dominant_sentiment} ({sentiment_percentages.iloc[0]}% of entries)
- The most common emotion expressed is {most_common_emotion} ({(emotion_counts.iloc[0]/total_entries*100):.1f}% of entries)
- Overall emotional tone is {self._determine_overall_tone(df)}
"""
            return summary
        except Exception as e:
            logger.error(f"Summary generation error: {str(e)}")
            return "Unable to generate summary due to an error."

    def _determine_overall_tone(self, df: pd.DataFrame) -> str:
        """Determine the overall emotional tone of the analyzed texts."""
        try:
            if df['Sentiment'].value_counts().index[0] == 'POSITIVE':
                return "predominantly positive"
            elif df['Sentiment'].value_counts().index[0] == 'NEGATIVE':
                return "predominantly negative"
            else:
                return "mixed or neutral"
        except:
            return "uncertain"

    def generate_contextual_considerations(self, texts: pd.Series) -> str:
        """Generate contextual considerations based on analyzed texts."""
        try:
            # Join all texts for context analysis
            full_text = ' '.join(texts.dropna().astype(str).tolist())
            # Limit text length if necessary for API call
            if len(full_text) > 1000:  # Adjust based on API limits or your preference
                full_text = full_text[:1000] + "..."  # Truncate the text if too long
            # Prompt for Anthropic to generate contextual considerations
            prompt = f"""Analyze the following texts to generate an analysis describing contextual considerations reflecting on broader structures like culture, market, or events. This should help explain why the sentiments and emotions observed might occur. 
Texts:
{full_text}
Considerations should include:
- Cultural trends or norms
- Market conditions or economic factors
- Current or historical events
- Political bias and leanings of the text
The analysis should discuss prevalent rhetorical devices utilized in the analyzed texts.
Succinctly captures a relevant context that might influence the sentiment or emotion in these texts. Respond only with a bulleted list."""
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=300,  # Adjust based on expected response length
                temperature=0.7,  # A slight creativity for better contextual analysis
                messages=[{"role": "user", "content": prompt}]
            )
            # Extract the generated list from Anthropic's response
            considerations = message.content[0].text if isinstance(message.content, list) else "No considerations generated."
            return considerations
        except Exception as e:
            logger.error(f"Error generating contextual considerations: {str(e)}")
            return "Unable to generate contextual considerations."

def initialize_session_state():
    """Initialize session state variables."""
    default_states = {
        'data': None,
        'analyzer': None,
        'analysis_complete': False,
        'summary_generated': False,
        'original_data': None,
        'active_tab': 'single',
        'processing': False,
        'progress': 0,
        'search_query': '',
        'theme': 'light',
        'emotion_provider': 'anthropic'  # Only Anthropic now
    }
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_header():
    """Render the application header."""
    st.title("Sentiment, Emotion, Context")
    st.info("""
    Welcome to our comprehensive text analysis tool where we delve into the nuances of language. Here, you can:
    - **Analyze Sentiment and Emotion**: Understand the underlying feelings in your text data.
    - **Explore Contextual Insights**: Uncover cultural, market, or event-related factors influencing your text.

    **How to Use:**
    - Upload a CSV file for batch analysis, or
    - Input text directly for single analysis.

    Please ensure your CSV has a single column named 'text' for accurate analysis.
    """)

def render_configuration(key_suffix: str):
    """Render configuration options with unique keys."""
    st.session_state.emotion_provider = 'anthropic'
    st.write("Currently using Anthropic for emotion analysis.")

def render_file_upload():
    """Render file upload section with UI description."""
    st.subheader("Batch Analysis")
    st.write("Upload a CSV file containing your texts for batch processing.")
    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type="csv",
        key="file_uploader"
    )
    return uploaded_file

def render_text_input():
    """Render text input section with UI description."""
    st.subheader("Single Text Analysis")
    text = st.text_area(
        "Enter text here for individual analysis. One text per line for multiple entries:",
        height=150,
        key="text_input_area"
    )
    if text:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.text(f"Character Count: {len(text)}")
        with col2:
            if st.button("Clear Text", key="clear_text"):
                st.session_state.text_input_area = ""
                st.experimental_rerun()
    return text

def process_data(data: pd.DataFrame):
    """Process the input data."""
    if st.button("Analyze Texts", key="process_button"):
        try:
            st.session_state.processing = True
            st.session_state.progress = 0
            analyzer = SentimentEmotionAnalyzer()
            data['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_rows = len(data)
            progress_bar = st.progress(0)
            status_text = st.empty()
            for idx, row in enumerate(data.itertuples(), 1):
                progress = idx / total_rows
                status_text.text(f"Analyzing text {idx}/{total_rows}...")
                progress_bar.progress(progress)
                sentiment, emotion = analyzer.analyze_text(row.text)
                data.at[row.Index, 'Sentiment'] = sentiment
                data.at[row.Index, 'Emotion'] = emotion
            st.session_state.data = data
            st.session_state.analysis_complete = True
            st.session_state.processing = False
            # Generate and display summary
            summary = analyzer.generate_analysis_summary(data)
            st.success("Analysis Complete!")
            st.markdown("### Analysis Summary")
            st.markdown(summary)
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")
            logger.error(f"Processing error: {str(e)}")
        finally:
            st.session_state.processing = False

def main():
    initialize_session_state()
    render_header()
    tab1, tab2 = st.tabs(["Single Text Analysis", "Batch Analysis (CSV)"])
    with tab1:
        render_configuration("single")
        text_input = render_text_input()
        if text_input:
            data = pd.DataFrame([text_input], columns=["text"])
            process_data(data)
    with tab2:
        render_configuration("batch")
        uploaded_file = render_file_upload()
        if uploaded_file:
            try:
                data = pd.read_csv(uploaded_file)
                if len(data.columns) == 1:
                    data.columns = ["text"]
                elif 'text' not in data.columns:
                    st.error("Please upload a CSV file with a 'text' column.")
                    return
                process_data(data[['text']])
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                logger.error(f"File reading error: {str(e)}")

    if st.session_state.analysis_complete and st.session_state.data is not None:
        # Display results
        st.subheader("Analysis Results")
        st.dataframe(
            st.session_state.data,
            use_container_width=True,
            hide_index=True
        )
        
        # Display the summary in the UI
        analyzer = SentimentEmotionAnalyzer()
        summary = analyzer.generate_analysis_summary(st.session_state.data)
        st.markdown("### Analysis Summary")
        st.markdown(summary)
        
        # Visualizations in UI
        if not st.session_state.data.empty:
            col1, col2 = st.columns(2)
            with col1:
                sentiment_counts = st.session_state.data['Sentiment'].value_counts()
                fig1 = px.bar(
                    sentiment_counts,
                    title="Sentiment Distribution",
                    labels={"index": "Sentiment", "value": "Count"}
                )
                st.plotly_chart(fig1, use_container_width=True)
                
            with col2:
                emotion_counts = st.session_state.data['Emotion'].value_counts()
                fig2 = px.pie(
                    emotion_counts,
                    title="Emotion Distribution",
                    names=emotion_counts.index,
                    values=emotion_counts.values
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Generate downloadable content
            csv_data = st.session_state.data.to_csv(index=False)
            
            # Generate PDF
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Add title
            styles = getSampleStyleSheet()
            elements.append(Paragraph("Sentiment, Emotion, Context Analysis Report", styles['Title']))
            elements.append(Spacer(1, 12))
            
            # Add summary to PDF
            elements.append(Paragraph(summary, styles['BodyText']))
            elements.append(Spacer(1, 12))
            
            # Contextual Considerations
            considerations = analyzer.generate_contextual_considerations(st.session_state.data['text'])
            elements.append(Paragraph("Contextual Considerations", styles['Heading2']))
            elements.append(Paragraph(considerations, styles['BodyText']))
            elements.append(Spacer(1, 12))
            
            doc.build(elements)
            pdf_data = buffer.getvalue()
            buffer.close()
            
            # CSV Download Button
            st.download_button(
                label="Download CSV Results",
                data=csv_data,
                file_name=f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            # PDF Download Button (without graphs)
            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
            
            # Add button for contextual analysis after initial processing is done
            if st.button("Generate Contextual Considerations", key="context_button"):
                try:
                    considerations = analyzer.generate_contextual_considerations(st.session_state.data['text'])
                    st.markdown("### Contextual Considerations")
                    st.markdown(considerations)
                except Exception as e:
                    st.error(f"Error generating contextual considerations: {str(e)}")
                    logger.error(f"Contextual analysis error: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}")

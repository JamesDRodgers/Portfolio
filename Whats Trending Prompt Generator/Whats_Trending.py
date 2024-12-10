
"""What's Trending Prompt Generator"""

# Import required libraries
import pandas as pd
from datetime import datetime
from typing import List, Dict
import logging
import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from IPython.display import display
import re
import os
from flask import Flask, send_from_directory
from dotenv import load_dotenv  # Import dotenv for environment variable handling

# Load environment variables from a .env file
load_dotenv()

# Set up logging for debugging and development insights
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Function to save DataFrame to a CSV file
def save_to_csv(df: pd.DataFrame, filename: str = "prompts.csv"):
    """Save generated prompts to a CSV file. Append to the file if it exists."""
    try:
        # Check if file exists and append new data
        try:
            existing_df = pd.read_csv(filename)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            print(f"Adding {len(df)} new prompts to existing {len(existing_df)} prompts.")
        except FileNotFoundError:
            # Create new file if it doesn't exist
            combined_df = df
            print("Creating new file with generated prompts.")

        combined_df.to_csv(filename, index=False)
        print(f"✅ Saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

# Function to start a Flask server for downloading the generated CSV file
def start_download_server(filename: str):
    """Start a Flask server to allow downloading of the generated CSV file."""
    app = Flask(__name__)

    @app.route('/download/<path:filename>', methods=['GET'])
    def download_file(filename):
        return send_from_directory('.', filename, as_attachment=True)

    print(f"\n🌐 Download your file at: http://127.0.0.1:5000/download/{filename}")
    app.run(debug=False, port=5000)

# Function to allow multiple selections from a list of items
def select_multiple_items(items: Dict[str, str], prompt: str) -> List[str]:
    """Enable users to select multiple items from a dictionary."""
    print(f"\n{prompt}")
    for i, (item, desc) in enumerate(items.items(), 1):
        print(f"{i}. {item}: {desc}")

    selections = []
    while True:
        try:
            input_str = input("\nEnter numbers (comma-separated) or 'done' to finish: ").strip().lower()
            if input_str == 'done':
                if selections:
                    break
                print("Please select at least one item!")
                continue

            indices = [int(x.strip()) - 1 for x in input_str.split(',')]
            items_list = list(items.keys())
            new_selections = [items_list[i] for i in indices if 0 <= i < len(items_list)]
            selections.extend(new_selections)

            print("\nCurrent selections:")
            for sel in selections:
                print(f"- {sel}")

            if input("Add more? (y/n): ").lower() != 'y':
                break

        except (ValueError, IndexError):
            print("Please enter valid numbers!")

    return list(set(selections))  # Remove duplicates

# API handler class for managing API connections and generating prompts
class APIHandler:
    def __init__(self):
        self.anthropic = None
        self.connected = False

    def setup_anthropic(self, api_key: str) -> bool:
        """Initialize Anthropic API with error handling."""
        try:
            self.anthropic = Anthropic(api_key=api_key)
            # Validate connection with a simple test prompt
            test_prompt = "Generate a one-word response: test"
            self.anthropic.completions.create(
                model="claude-2",
                max_tokens_to_sample=10,
                prompt=f"{HUMAN_PROMPT} {test_prompt} {AI_PROMPT}"
            )
            self.connected = True
            logger.info("Anthropic API connected successfully")
            print("✅ Anthropic API connected!")
            return True
        except Exception as e:
            logger.error(f"Anthropic setup failed: {e}")
            print(f"❌ Anthropic setup failed: {e}")
            return False

    def clean_response(self, response: str) -> str:
        """Clean raw API responses to remove unnecessary text."""
        if not response:
            return None

        response = response.strip()
        prefixes = [
            "here is", "here's", "here are", "consider", "let me", "i suggest",
            "suggested question", "how about", "what about", "try this",
            "here's a question", "here is a question", "question:"
        ]
        response_lower = response.lower()
        for prefix in prefixes:
            if response_lower.startswith(prefix):
                response = response[len(prefix):].strip()

        response = response.strip(':"\'.,- \n\t')
        response = response.split('.')[0].strip()
        return response

    def generate_prompt(self, template: str, topic: str, style: str, api_type: str, max_tokens: int = 100) -> str:
        """Generate prompts using the selected API."""
        if not self.connected and api_type != "None":
            logger.warning("API not connected")
            return "Please connect to API first"

        try:
            full_prompt = f"""Role: You are a prompt engineer creating a single analytical question for an AI system.

            Topic: {topic}
            Context: {template}
            Style: {style}

            Output Rules:
            - Output ONLY the question itself
            - No introductory phrases
            - No commentary
            - No explanations
            - No "Here is..."
            - No "Consider..."
            - No quotes around the question

            Your output should be just like these examples - one direct question with no additional text."""

            if api_type == "Anthropic" and self.connected:
                completion = self.anthropic.completions.create(
                    model="claude-2",
                    max_tokens_to_sample=max_tokens,
                    prompt=f"{HUMAN_PROMPT} {full_prompt} {AI_PROMPT}",
                    temperature=0.5
                )

                response = self.clean_response(completion.completion)
                logger.debug(f"Raw response: {completion.completion}")
                logger.debug(f"Cleaned response: {response}")

                if response:
                    return response
                else:
                    return self.get_fallback_prompt(topic, template)
            else:
                return self.get_fallback_prompt(topic, template)

        except Exception as e:
            logger.error(f"Prompt generation error: {e}")
            return self.get_fallback_prompt(topic, template)

    def get_fallback_prompt(self, topic: str, template: str) -> str:
        """Provide fallback prompts in case API calls fail."""
        fallbacks = {
            "Historical Development": f"What key developments shaped {topic}'s evolution over the past decade?",
            "Economic Impact": f"How has {topic} influenced market dynamics in its sector?",
            "Social Change": f"What measurable social changes can be attributed to {topic}?",
            "Innovation": f"Which technological advances have most impacted {topic}'s development?",
            "Global Influence": f"How has {topic} affected international developments in its field?"
        }
        return fallbacks.get(template, f"What significant changes has {topic} undergone in recent years?")

# Constants for template and style selection
TEMPLATES = {
    "Historical Development": "examining documented historical developments and verifiable milestones",
    "Economic Impact": "analyzing quantifiable economic effects and market data",
    "Social Change": "exploring measurable social and cultural transformations",
    "Innovation": "investigating technical advances and methodological improvements",
    "Global Influence": "studying international impact and cross-border effects",
    "Ethical Implications": "exploring moral and ethical considerations in decision-making and outcomes"
}
STYLES = {
    "Academic": "scholarly analysis with cited evidence",
    "Data-Focused": "emphasis on statistics and metrics",
    "Historical": "chronological development analysis",
    "Comparative": "structured comparison of verifiable factors",
    "Process": "systematic examination of mechanisms"
}

def generate_prompts(api_handler, topics: List[str], templates: List[str], styles: List[str]) -> pd.DataFrame:
    """Generate prompts based on user inputs."""
    results = []
    total = len(topics) * len(templates) * len(styles)
    print(f"\nGenerating {total} prompts...")
    current = 0

    for topic in topics:
        for template in templates:
            for style in styles:
                current += 1
                print(f"Processing {current}/{total}: {topic} - {template} - {style}")
                prompt = api_handler.generate_prompt(
                    TEMPLATES[template],
                    topic,
                    STYLES[style],
                    "Anthropic",
                    max_tokens=150
                )
                if prompt and not prompt.startswith("Please connect"):
                    results.append({
                        "Topic": topic,
                        "Generated Question": prompt,
                        "Template": template,
                        "Style": style,
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

    return pd.DataFrame(results)

# Main script entry point
def run_prompt_generator():
    """Run the prompt generator interactively."""
    api_handler = APIHandler()

    print("🤖 Welcome to the Enhanced Prompt Generator")
    print("-" * 50)

    # API Setup from .env file
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ No API key found. Ensure a valid ANTHROPIC_API_KEY is in your .env file.")
        return
    if not api_handler.setup_anthropic(api_key):
        print("❌ Failed to connect to Anthropic API. Check your API key.")
        return

    # Topic Collection
    print("\n📝 Enter topics (one per line, press Enter twice when done):")
    topics = []
    while True:
        topic = input().strip()
        if not topic:
            if topics:
                break
            print("Please enter at least one topic!")
            continue
        topics.append(topic)

    # Template and Style Selection
    templates = select_multiple_items(TEMPLATES, "📋 Available templates:")
    styles = select_multiple_items(STYLES, "🎨 Available styles:")

    # Generate and Save Prompts
    print("\n⚙️ Generating prompts...")
    results_df = generate_prompts(api_handler, topics, templates, styles)

    if not results_df.empty:
        print("\n✨ Generated Prompts:")
        display(results_df)

        if input("\n💾 Save to CSV? (y/n): ").lower().startswith('y'):
            filename = input("Enter filename (default: prompts.csv): ").strip() or "prompts.csv"
            save_to_csv(results_df, filename)
            if input("\n🌐 Start a download server? (y/n): ").lower().startswith('y'):
                start_download_server(filename)
    else:
        print("\n❌ No prompts were generated. Please check your inputs and try again.")

if __name__ == "__main__":
    run_prompt_generator()

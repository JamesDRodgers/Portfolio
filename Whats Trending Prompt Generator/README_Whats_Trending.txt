
# What's Trending Prompt Generator

This project is a Python-based tool designed to generate prompts for fact-checking large language models (LLMs) and exploring trending topics on social media. It combines user input with customizable templates and styles to create well-structured analytical questions.

---

## Purpose

I developed this tool to simplify the process of creating prompts for LLM evaluation and social media trend exploration. It is designed to:
- Support the generation of targeted, fact-based questions.
- Provide flexibility with templates and styles to meet different analytical needs.
- Demonstrate integration with APIs and effective user interaction design.

---

## Key Features

- **Prompt Generation:** Create analytical prompts tailored to user-defined topics, templates, and styles.
- **Anthropic API Integration:** Uses the Anthropic Claude API for text generation.
- **Fallback Mechanism:** Ensures functionality by providing default prompts when API access is unavailable.
- **Output Management:** Saves prompts in a CSV format with an optional local download server.
- **Secure API Handling:** API keys are securely managed using a `.env` file.

---

## How to Use

1. **Setup:**
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Add your API key to a `.env` file in the following format:
     ```env
     ANTHROPIC_API_KEY=your_api_key_here
     ```

2. **Run the Script:**
   - Execute the main script:
     ```bash
     python Whats_Trending.py
     ```
   - Follow the prompts to:
     - Enter topics for analysis.
     - Select templates (e.g., Historical Development, Ethical Implications).
     - Choose styles (e.g., Academic, Data-Focused).
   - Save the generated prompts to a CSV file.

3. **Sample Output:**
   - View the included sample file `November21Trends.csv` for reference.

---

## File Overview

- `Whats_Trending.py`: Main script for generating prompts.
- `.env`: Environment file for securely storing API keys.
- `November21Trends.csv`: Sample output showcasing the generated prompts.

---

## Sample Output

| Topic       | Generated Question                                         | Template                | Style           | Timestamp           |
|-------------|------------------------------------------------------------|-------------------------|-----------------|---------------------|
| AI Ethics   | How can AI models be regulated to ensure ethical practices?| Ethical Implications    | Academic        | 2024-11-21 14:23:00|
| Climate Tech| How has renewable energy innovation impacted global policies?| Global Influence        | Data-Focused    | 2024-11-21 14:24:00|

---

## Dependencies

This project requires:
- `pandas`
- `flask`
- `openai`
- `anthropic`
- `python-dotenv`

Install them with:
```bash
pip install -r requirements.txt
```

---

## Why I Built This

I created this project as a straightforward way to:
1. Generate prompts for evaluating LLMs.
2. Analyze trending topics across social media platforms.


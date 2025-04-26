# Enneagram Text Analyzer

This tool analyzes text passages and predicts the most likely Enneagram type (1–9) for each section.  
It's useful for evaluating spiritual writings, sermons, journal entries, and more.

## 💡 Features

- Segments text into meaningful chunks
- Classifies each chunk using a fine-tuned GPT model
- Falls back to GPT-4 if the fine-tuned model fails to respond correctly
- Provides spiritual and psychological rationales for each prediction
- Displays a distribution chart of detected Enneagram types

## 🔐 Usage

1. Provide your [OpenAI API key](https://platform.openai.com/account/api-keys).
2. Paste your text content into the analyzer.
3. Click **Analyze** to view type predictions, explanations, and a visual chart.

> Note: The app runs asynchronously and processes all chunks in parallel.

## 🧠 Model Info

- Primary: `ft:gpt-3.5-turbo-1106:personal:enneagramv1`
- Backup: GPT-4 (fallback mode)

## 📊 Example Use Cases

- Spiritual direction or self-inquiry
- Sermon personality profiling
- Deep character analysis in stories
- Personality mapping across longform content

---

Built using [Gradio](https://gradio.app/), [OpenAI](https://platform.openai.com/), and [matplotlib](https://matplotlib.org/).

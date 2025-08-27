import openai
import gradio as gr
import re
import matplotlib.pyplot as plt
import io
import asyncio
import httpx
import os
from PIL import Image
from collections import Counter

# 🔢 Segment text into chunks
def segment_text(text: str):
    if len(text) < 200:
        sentences = re.split(r'(?<=[.!?])\s+', text)
    else:
        sentences = [p.strip() for p in text.split("\n\n") if p.strip()]
    
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) < 500:
            current += " " + sentence if current else sentence
        else:
            if current:
                chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]

# 🔁 Fallback to GPT-4 if fine-tuned model fails
async def fallback_classify(client, api_key: str, chunk: str) -> str:
    try:
        fallback_prompt = (
            f"Analyze this text and determine which of the 9 Enneagram types (1-9) it most strongly reflects. "
            f"Respond only with the type number (e.g., '4' or '9'):\n\n{chunk}"
        )
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": fallback_prompt}],
                "temperature": 0.3
            },
            timeout=30
        )
        result = response.json()
        prediction = result['choices'][0]['message']['content'].strip()
        return prediction
    except Exception as e:
        return f"error: {str(e)}"

# 🧠 Classify and explain
async def classify_chunk_async(client, api_key: str, chunk: str) -> (str, str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    classify_data = {
        "model": "ft:gpt-3.5-turbo-1106:personal:enneagramv1:BQ7Ro4TT",
        "messages": [{"role": "user", "content": chunk}],
        "temperature": 0.4
    }

    try:
        classify_response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=classify_data,
            timeout=30
        )
        classify_result = classify_response.json()
        prediction = classify_result['choices'][0]['message']['content'].strip()

        if not prediction.isdigit() or not (1 <= int(prediction) <= 9):
            prediction = await fallback_classify(client, api_key, chunk)

        rationale_prompt = (
            f"Explain why the following text aligns with Enneagram {prediction}:\n\n{chunk}\n\n"
            "Give a concise but detailed rationale. The output should be two sentences: "
            "(1) why the content reflects this type, (2) how it resonates with the spiritual strengths/fears of the type."
        )
        rationale_data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": rationale_prompt}],
            "temperature": 0.3
        }

        rationale_response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=rationale_data,
            timeout=30
        )
        rationale_result = rationale_response.json()
        rationale = rationale_result['choices'][0]['message']['content'].strip()

        return prediction, rationale

    except Exception as e:
        return f"error: {str(e)}", "error"

# 📋 Generate summary
async def generate_summary(client, api_key: str, counter: Counter) -> str:
    try:
        type_counts = "\n".join(f"{k}: {v} chunks" for k, v in counter.items())

        summary_prompt = (
            f"Given the following Enneagram type distribution detected from a sermon:\n\n"
            f"{type_counts}\n\n"
            "Write one paragraph summarizing how a diverse congregation might receive the message across different Enneagram types. "
            "Then, based on the 2-3 least represented of the nine total types, suggest small edits or adjustments to help reach those individuals without altering the theological or Gospel-driven core of the message. Remember to incorporate the two important elements of homiletics law and gospel or problem in the text / world and grace in the text / world. this might relate to enneagram strengths and weaknesses."
        )

        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": summary_prompt}],
                "temperature": 0.5
            },
            timeout=60
        )
        result = response.json()
        summary_text = result['choices'][0]['message']['content'].strip()

        return summary_text
    except Exception as e:
        return f"Summary generation error: {str(e)}"

# 🧪 Process all chunks
async def process_all_chunks(api_key: str, chunks):
    async with httpx.AsyncClient() as client:
        tasks = [classify_chunk_async(client, api_key, chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks)
    return results

# 🧮 Analyze input
def analyze_text(user_api_key, text_input):
    api_key = os.getenv("OPENAI_API_KEY") or user_api_key
    if not api_key or not text_input:
        return "Please provide a valid OpenAI API key and some text.", None

    chunks = segment_text(text_input)
    results = asyncio.run(process_all_chunks(api_key.strip(), chunks))

    output = ""
    counter = Counter()

    for i, (chunk, (prediction, rationale)) in enumerate(zip(chunks, results)):
        output += f"<h3>Chunk {i+1}</h3>"
        output += f"<blockquote><b>Text:</b><br>{chunk.strip()}</blockquote>"

        prediction = prediction.strip()
        if prediction.isdigit() and 1 <= int(prediction) <= 9:
            output += f"<p><b>Predicted Type:</b> Type {prediction}</p>"
            output += f"<p><b>Rationale:</b><br>{rationale.strip()}</p>"
            counter[f"Type {prediction}"] += 1
        else:
            output += f"<p><b>Prediction Error:</b> Could not determine a valid Enneagram type.</p>"
            output += f"<p><b>Rationale:</b><br>{rationale.strip()}</p>"
            counter["Unknown"] += 1

        output += "<hr>"

    # 📈 Pie chart
    fig, ax = plt.subplots()
    labels = list(counter.keys())
    sizes = list(counter.values())
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title("Enneagram Type Distribution")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    img = Image.open(buf)

    # ✨ Generate summary
    summary = asyncio.run(run_summary(api_key.strip(), counter))

    output += "<h3>Reception Summary & Recommendations</h3>"
    output += f"<p>{summary}</p>"

    return output, img

# 🏃‍♂️ Separate runner because analyze_text can't be async directly
async def run_summary(api_key, counter):
    async with httpx.AsyncClient() as client:
        return await generate_summary(client, api_key, counter)

# 🖥️ Gradio Interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## Enneagram Text Analyzer\nAnalyze spiritual reflections, sermons, and contemplative text.")

        api_input = gr.Textbox(label="OpenAI API Key", type="password", placeholder="Paste your API key here")
        text_input = gr.Textbox(label="Text to Analyze", lines=15, placeholder="Paste your spiritual content here...")
        analyze_btn = gr.Button("Analyze")

        output_text = gr.Markdown()
        output_chart = gr.Image(type="pil", label="Enneagram Type Distribution")

        analyze_btn.click(
            fn=analyze_text,
            inputs=[api_input, text_input],
            outputs=[output_text, output_chart]
        )

    return demo

# 🚀 Launch
demo = create_interface()
demo.launch()

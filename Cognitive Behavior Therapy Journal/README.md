# CBT Journal – Gradio App

## 🎯 Why this project?

This project was built to demonstrate:

- **Applied AI integration** (OpenAI API with structured prompts and safety guardrails).  
- **Data modeling & storage** (dataclasses, JSONL logging, CSV exports).  
- **Interactive UI design** (Gradio-based interface for real-world usability).  
- **Modular architecture** (clean separation of config, models, storage, AI, and UI).  

It serves as a portfolio piece showcasing how to build a complete, production-style Python application that combines machine learning APIs, structured data pipelines, and user-friendly interfaces.

---

## 🔑 Key Features

- **Modular Architecture**  
  Config management (`config.py`), data models (`journal.py`), storage utilities, AI integration, and UI are separated into clean modules.

- **Data Handling**  
  Entries saved in **JSONL** (append-only).  
  Full export to **CSV**, including timestamped snapshots.

- **Emotion Wheel**  
  Implementation of a hierarchical emotion model (primary → secondary → tertiary).  
  JSON-seeded for portability.

- **Cognitive Distortion Library**  
  Standard CBT distortion set with definitions for UI integration.

- **AI Reflection (Optional)**  
  Uses OpenAI’s API with safety guardrails.  
  Structured output: reflection, distortion explanation, evidence scan, reframing options, and small next steps.

- **User Interface**  
  Gradio UI with three tabs:  
  - **New Entry**: journaling workflow + optional AI reflection.  
  - **Journal History**: tabular display of all fields with CSV export.  
  - **About & Resources**: reference material and usage overview.

---

## 📂 Project Structure

```
app/
 ├── ai/
 │    └── reflection.py        # AI reflection logic
 ├── data_models/
 │    └── journal.py           # JournalEntry dataclass
 ├── interfaces/
 │    └── gradio_ui.py         # Gradio interface
 ├── config.py                 # Paths, CSV schema, utilities
 ├── emotions.py               # Emotion wheel utilities
 ├── distortions.py            # Cognitive distortions module
 ├── storage.py                # JSONL/CSV storage + exports
 └── main.py                   # Entry point
data/                          # Auto-created storage
exports/                       # Auto-created CSV exports
```

---

## ⚙️ Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/cbt-journal.git
cd cbt-journal

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

**Requirements:**

- `gradio>=4.44.0`  
- `pandas>=2.0.0`  
- `pydantic>=2.7.0`  
- `python-dotenv>=1.0.1`  
- `openai>=1.40.0`  
- `typing_extensions>=4.7.0`  

---

## ▶️ Run

```bash
python -m app.main
```

The app will launch with:

- **Local URL**: http://127.0.0.1:7860  
- **Public `.gradio.live` link** (when running in Colab or with `share=True`).

---

## 📊 Data

- Entries stored in `data/journal.jsonl`.  
- Exports created in `exports/journal_export_<timestamp>.csv`.  

"""
Gradio UI for the CBT Journal app (default Gradio theme).

- Simple defaults 
- Separate: " Generate AI Reflection" and " Save Entry"
- Tabs: New Entry / Journal History / About & Resources
- Date uses a manual textbox (YYYY-MM-DD) for broad compatibility
- Journal History
"""

import gradio as gr
import pandas as pd
from datetime import datetime
from app.emotions import EmotionWheel
from app.distortions import get_distortion_names, get_distortion_description
from app.data_models.journal import JournalEntry
from app.storage import save_entry_jsonl, load_entries_jsonl, export_snapshot
from app.ai.reflection import generate_reflection
from app.config import ensure_dirs, CSV_FIELDS

ABOUT_MD = """
# About & Resources

**CBT Journal** is a simple tool to capture a situation, name your thoughts and emotions, spot a common thinking habit (cognitive distortion), and practice a kinder, more balanced reframe. An optional AI reflection can offer prompts and alternatives — it is supportive, not diagnostic.

---

## How to use this app
1. **New Entry**  
   - Add the date and a brief description of what happened.  
   - Write your **Automatic Thought** (the first interpretation that popped up).  
   - Choose **Primary → Secondary → Specific** emotion and set **Intensity (1–7)**.  
   - Pick a **Cognitive Distortion** and read the short description.  
   - Write a short **Balanced Reframe**.  
   - If you want suggestions, toggle **Get AI Reflection**, paste your API key, and click **Generate AI Reflection**.  
   - When you’re ready, click **Save Entry**.

2. **Journal History**  
   - View every field from your past entries.  
   - Use **Export CSV** to save a snapshot.

3. **About & Resources**  
   - Quick CBT reminders and safety note.

---

## CBT in one minute
CBT explores how **thoughts, emotions, and behaviors** influence each other. Sometimes our thoughts follow patterns like **All-or-Nothing Thinking**, **Overgeneralization**, **Catastrophizing**, or **Mental Filter**. Naming a pattern makes it easier to test the thought and consider a fairer alternative.

**Balanced Reframe tips**
- Aim for *kind, specific, and believable* — not blindly positive.
- If it helps, start with: *“Another way to see this is…”*, *“It’s possible that…”*, or *“A fairer take might be…”*.

---

## Gentle safety note
This app is **not therapy** and doesn’t provide crisis support.  
If you feel unsafe or at risk of harming yourself or others, please seek immediate help from local emergency services or a trusted professional. Reaching out to a supportive friend or community member can also help.

Stay kind to yourself while you practice.
"""

class CBTJournalUI:
    def __init__(self):
        ensure_dirs()
        self.emotion_wheel = EmotionWheel()
        # Show ALL columns in history using the CSV export order
        self.summary_columns = CSV_FIELDS[:]  # ['date','event','thought',...,'ai_reflection']

    # ---------- Helpers ----------
    def get_secondary_emotions(self, primary_emotion):
        if not primary_emotion:
            return gr.Dropdown(choices=[], value=None)
        return gr.Dropdown(
            choices=self.emotion_wheel.get_secondary_emotions(primary_emotion),
            value=None, label="Secondary Emotion"
        )

    def get_tertiary_emotions(self, primary_emotion, secondary_emotion):
        if not primary_emotion or not secondary_emotion:
            return gr.Dropdown(choices=[], value=None)
        return gr.Dropdown(
            choices=self.emotion_wheel.get_tertiary_emotions(primary_emotion, secondary_emotion),
            value=None, label="Specific Emotion"
        )

    def show_distortion_info(self, distortion_name):
        return "" if not distortion_name else get_distortion_description(distortion_name)

    # ---------- Actions ----------
    def generate_only_reflection(
        self, date, event, thought, primary_emotion, secondary_emotion,
        tertiary_emotion, intensity, distortion, reframing, api_key, use_ai
    ):
        if not use_ai:
            return "AI is disabled. Toggle 'Get AI Reflection' on.", ""
        if not (api_key or "").strip():
            return "Please paste your OpenAI API key.", ""
        if not (event and thought and primary_emotion and distortion and reframing):
            return "Fill in all required fields (*) before generating AI reflection.", ""

        entry = JournalEntry(
            date=date or datetime.now().strftime("%Y-%m-%d"),
            event=event.strip(),
            thought=thought.strip(),
            emotion_primary=primary_emotion,
            emotion_secondary=secondary_emotion or None,
            emotion_tertiary=tertiary_emotion or None,
            emotion_intensity=int(intensity or 3),
            cbt_distortion=distortion,
            reframing=reframing.strip()
        )
        ai_text = generate_reflection(entry, api_key.strip())
        if ai_text.startswith("[AI Error]"):
            return ai_text, ""
        return "✅ AI reflection generated.", ai_text

    def save_only_entry(
        self, date, event, thought, primary_emotion, secondary_emotion,
        tertiary_emotion, intensity, distortion, reframing, ai_reflection_text
    ):
        if not (event and thought and primary_emotion and distortion and reframing):
            return "❌ Please fill in all required fields.", self.get_journal_summary()

        entry = JournalEntry(
            date=date or datetime.now().strftime("%Y-%m-%d"),
            event=event.strip(),
            thought=thought.strip(),
            emotion_primary=primary_emotion,
            emotion_secondary=secondary_emotion or None,
            emotion_tertiary=tertiary_emotion or None,
            emotion_intensity=int(intensity or 3),
            cbt_distortion=distortion,
            reframing=reframing.strip(),
            ai_reflection=(ai_reflection_text or "").strip() or None
        )
        save_entry_jsonl(entry)
        return "✅ Journal entry saved.", self.get_journal_summary()

    def get_journal_summary(self):
        """Return ALL fields for each entry as a DataFrame."""
        entries = load_entries_jsonl()
        rows = []
        for e in entries:
            rows.append({
                "date": e.date,
                "event": e.event,
                "thought": e.thought,
                "emotion_primary": e.emotion_primary,
                "emotion_secondary": e.emotion_secondary,
                "emotion_tertiary": e.emotion_tertiary,
                "emotion_intensity": e.emotion_intensity,
                "cbt_distortion": e.cbt_distortion,
                "reframing": e.reframing,
                "ai_reflection": (e.ai_reflection or "")
            })
        return pd.DataFrame(rows, columns=self.summary_columns)

    def export_journal(self):
        entries = load_entries_jsonl()
        if not entries:
            return "No entries to export.", None
        export_path = export_snapshot(entries)
        return f"✅ Journal exported: {export_path.name}", str(export_path)

def create_ui():
    ui = CBTJournalUI()

    with gr.Blocks(title="CBT Journal") as app:
        gr.Markdown("# CBT Journal")

        with gr.Tabs():
            # ----------------- New Entry -----------------
            with gr.Tab("New Entry"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("## Basic Information")
                        date_input = gr.Textbox(label="Date", value=datetime.now().strftime("%Y-%m-%d"), info="YYYY-MM-DD")
                        event_input = gr.Textbox(label="What happened? *", lines=3, placeholder="Briefly describe the situation.")
                        thought_input = gr.Textbox(label="Automatic Thought *", lines=3, placeholder="What went through your mind?")
                    with gr.Column(scale=2):
                        gr.Markdown("## Emotions")
                        primary_emotion = gr.Dropdown(choices=ui.emotion_wheel.get_primary_emotions(), label="Primary Emotion *")
                        secondary_emotion = gr.Dropdown(choices=[], label="Secondary Emotion")
                        tertiary_emotion = gr.Dropdown(choices=[], label="Specific Emotion")
                        intensity_slider = gr.Slider(minimum=1, maximum=7, value=3, step=1, label="Emotion Intensity *")

                gr.Markdown("## Cognitive Analysis")
                with gr.Row():
                    with gr.Column():
                        distortion_dropdown = gr.Dropdown(choices=get_distortion_names(), label="Cognitive Distortion *")
                        distortion_info = gr.Textbox(label="Distortion Description", interactive=False, lines=2)
                    with gr.Column():
                        reframing_input = gr.Textbox(label="Balanced Reframe *", lines=4, placeholder="Kind, fair, evidence-based.")

                gr.Markdown("## AI Assistance (Optional)")
                with gr.Row():
                    with gr.Column():
                        use_ai_checkbox = gr.Checkbox(label="Get AI Reflection", value=False)
                        api_key_input = gr.Textbox(label="OpenAI API Key", type="password", placeholder="sk-...")
                        generate_btn = gr.Button("✨ Generate AI Reflection")
                    with gr.Column():
                        ai_reflection_output = gr.Textbox(label="AI Reflection (review/edit)", interactive=True, lines=8)

                with gr.Row():
                    save_btn = gr.Button("💾 Save Entry")
                    clear_btn = gr.Button("🔄 Clear Form")
                status_output = gr.Textbox(label="Status", interactive=False, lines=1)

            # ----------------- Journal History -----------------
            with gr.Tab("Journal History"):
                gr.Markdown("## Your Journal Entries")
                with gr.Row():
                    refresh_btn = gr.Button("🔄 Refresh")
                    export_btn = gr.Button("📤 Export CSV")
                journal_summary = gr.Dataframe(
                    value=ui.get_journal_summary(),
                    label="All Entries (all columns)",
                    interactive=False,
                    wrap=True,
                )
                export_status = gr.Textbox(label="Export Status", interactive=False)
                download_file = gr.File(label="Download CSV", visible=False)

            # ----------------- About & Resources -----------------
            with gr.Tab("About & Resources"):
                gr.Markdown(ABOUT_MD)
                help_distortions = gr.Dropdown(choices=get_distortion_names(), label="Browse Distortions")
                help_text = gr.Textbox(label="Description", interactive=False, lines=4)
                help_distortions.change(ui.show_distortion_info, inputs=[help_distortions], outputs=[help_text])

        # Events
        primary_emotion.change(ui.get_secondary_emotions, inputs=[primary_emotion], outputs=[secondary_emotion])
        secondary_emotion.change(ui.get_tertiary_emotions, inputs=[primary_emotion, secondary_emotion], outputs=[tertiary_emotion])
        distortion_dropdown.change(ui.show_distortion_info, inputs=[distortion_dropdown], outputs=[distortion_info])

        generate_btn.click(
            ui.generate_only_reflection,
            inputs=[date_input, event_input, thought_input, primary_emotion, secondary_emotion, tertiary_emotion,
                    intensity_slider, distortion_dropdown, reframing_input, api_key_input, use_ai_checkbox],
            outputs=[status_output, ai_reflection_output]
        )

        save_btn.click(
            ui.save_only_entry,
            inputs=[date_input, event_input, thought_input, primary_emotion, secondary_emotion, tertiary_emotion,
                    intensity_slider, distortion_dropdown, reframing_input, ai_reflection_output],
            outputs=[status_output, journal_summary]
        )

        def _clear():
            return (
                datetime.now().strftime("%Y-%m-%d"), "", "", None,
                None, None, 3,
                None, "", "", ""
            )
        clear_btn.click(
            _clear,
            outputs=[date_input, event_input, thought_input, primary_emotion,
                     secondary_emotion, tertiary_emotion, intensity_slider, distortion_dropdown,
                     reframing_input, ai_reflection_output, status_output]
        )

        refresh_btn.click(ui.get_journal_summary, outputs=[journal_summary])

        def _export_and_show():
            status, path = ui.export_journal()
            return status, (path if path else None), gr.update(visible=bool(path))
        export_btn.click(_export_and_show, outputs=[export_status, download_file, download_file])

    return app

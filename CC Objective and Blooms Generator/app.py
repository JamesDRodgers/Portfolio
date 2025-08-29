import streamlit as st
import pandas as pd
import json
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass
from openai import OpenAI

# === SETTINGS ===
CSV_PATH = r"C:\Users\jdevi\OneDrive\Desktop\curriculum\ccc (1).csv"
DEFAULT_MODEL = "gpt-4o-mini"
LEARNING_STYLE_TAGS = "[visual, auditory, kinesthetic, reading/writing, collaborative, independent]"

st.set_page_config(page_title="Standards, Objectives, Bloom's Taxonomy of Learning by CC Standards", layout="centered")

# === TABS ===
tab1, tab2 = st.tabs(["📚 Objective and Blooms Generator", "ℹ️ About this App"])

# === ABOUT TAB ===
with tab2:
    st.markdown("""
### ℹ️ About This App


This application is designed to assist **curriculum designers**, **classroom teachers**, and **instructional leaders** in building high-quality, standards-aligned learning plans in just a few clicks.

#### 🎯 Key Features

- **Browse Standards by Grade and Subject**  
  Select from **Common Core State Standards (CCSS)** for **English Language Arts (ELA)** and **Mathematics**. You can filter by grade level and subject to quickly locate the most relevant standard for your instruction.

- **Instant Objective Generation**  
  Once a standard is selected, the app uses AI (powered by OpenAI's GPT-4o-mini) to generate:
  - **Educator-facing objectives** using the "SWBAT" (Students Will Be Able To) format
  - **Student-friendly objectives**, including “I can” statements and practical learning goals

- **Bloom’s Taxonomy Activities**  
  For each standard, the app suggests **two classroom-ready activities per level** of **Bloom’s Taxonomy** — a widely used instructional framework that categorizes learning objectives by cognitive complexity:
  - **Remembering**: recalling facts and concepts
  - **Understanding**: explaining ideas or concepts
  - **Applying**: using information in new situations
  - **Analyzing**: breaking information into parts to explore patterns
  - **Evaluating**: justifying a decision or position
  - **Creating**: producing original work or solutions

  These activities are customized with learning modalities (e.g., visual, auditory, kinesthetic) and include both **online** and **offline** options using school-friendly tools like **Google Docs, Flip, Canva, and Quizizz**.

- **Measurable Benchmarks**  
  Each objective includes **assessment methods ideas** (quizzes, rubrics, exit tickets, performance tasks) along with **success criteria** to measure student mastery.

- **Markdown Export**  
  Download a full curriculum snapshot in clean markdown format — ideal for lesson planning, sharing with colleagues, or saving to your instructional archives.

---

💡 This app is built to save time, reduce planning friction, and support high-quality instruction aligned to rigorous standards — all while honoring cognitive complexity and learner accessibility.

    """)

# === MAIN TAB ===
with tab1:
    st.title("📚 Objectives, Benchmarks, and Bloom's Taxonomy Activities Generator")
    api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

    @st.cache_data
    def load_standards(path: str):
        df = pd.read_csv(path)
        df.columns = [c.strip() for c in df.columns]
        def _norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
        canonical = {
            "grade": "Grade",
            "subject": "Subject",
            "standardcode": "StandardCode",
            "subcategory": "Subcategory",
            "description": "Description"
        }
        rename = {col: canonical[_norm(col)] for col in df.columns if _norm(col) in canonical}
        return df.rename(columns=rename)

    df = load_standards(CSV_PATH)
    grades = sorted(df["Grade"].dropna().unique())
    subjects = sorted(df["Subject"].dropna().unique())
    grade = st.selectbox("🎓 Grade", grades)
    subject = st.selectbox("📘 Subject", subjects)

    filtered_df = df[
        (df["Grade"].astype(str).str.lower() == grade.lower()) &
        (df["Subject"].astype(str).str.lower() == subject.lower())
    ]

    if not filtered_df.empty:
        filtered_df = filtered_df.sort_values("StandardCode")
        filtered_df["combo"] = filtered_df["StandardCode"].astype(str) + " – " + filtered_df["Description"]
        selected_combo = st.selectbox("📚 Choose Standard", filtered_df["combo"])
    else:
        st.warning("No standards found for this grade and subject.")
        selected_combo = None

    if st.button("🚀 Generate Plan") and api_key and selected_combo:
        with st.spinner("Generating your learning plan..."):
            row = filtered_df[filtered_df["combo"] == selected_combo].iloc[0]

            @dataclass
            class GenerationRequest:
                grade: str
                subject: str
                state: str = ""
                standard: Optional[str] = None
                standard_code: Optional[str] = None
                domain: Optional[str] = None
                strand: Optional[str] = None
                subcategory: Optional[str] = None
                description: Optional[str] = None

            JSON_TARGET = {
                "curriculum_developer": {
                    "objectives": {"knowledge": [], "skills": []},
                    "benchmarks": []
                },
                "student_friendly": {
                    "goals": [], "ican_statements": [], "how_ill_show_learning": []
                },
                "blooms_taxonomy_activities": {
                    "remembering": [], "understanding": [], "applying": [],
                    "analyzing": [], "evaluating": [], "creating": []
                }
            }

            def build_prompt(req: GenerationRequest) -> str:
                extras = []
                if req.standard_code: extras.append(f"Standard Code: {req.standard_code}")
                if req.domain: extras.append(f"Domain: {req.domain}")
                if req.strand: extras.append(f"Strand: {req.strand}")
                if req.subcategory: extras.append(f"Subcategory: {req.subcategory}")
                if req.description: extras.append(f"Description: {req.description}")
                extra_text = "\n".join(extras)

                return f"""
You are an expert curriculum developer and instructional designer.

Goal: Generate educational content tailored to {req.grade}.

Context:
Grade: {req.grade}
Subject: {req.subject}
State: {req.state}
Standard: {req.standard}
{extra_text}

OUTPUT SPECIFICATION — return ONLY valid JSON exactly matching this schema:
{json.dumps(JSON_TARGET, indent=2)}

CONTENT REQUIREMENTS
1) Objectives (SWBAT):
   - Write 3–5 objectives beginning with "SWBAT ..."
   - Each objective must include: a condition/context, a measurable Bloom-aligned verb, the specific content/knowledge, and a success criterion (e.g., "with 80% accuracy", "in a 150-word response", "using correct terminology").
   - Put knowledge elements in "knowledge" and the behaviors in "skills".

2) Benchmarks (Measurable):
   - For each objective, provide 1–2 measurable benchmarks that include the assessment method (quiz, rubric, exit ticket, performance task) and a clear threshold for success (e.g., "4/5 correct", "meets rubric level 3+").

3) Student-Friendly Version (developmentally appropriate for {req.grade}):
   - "goals": 3–5 plain-language goals.
   - "ican_statements": 4–6 "I can ..." statements aligned to the objectives.
   - "how_ill_show_learning": 4–6 ways students can demonstrate learning, including at least TWO digital artifacts.

4) Bloom’s Taxonomy Activities:
   - Provide EXACTLY 2 activities for each level: remembering, understanding, applying, analyzing, evaluating, creating.
   - Each activity must be a single concise string using this format:
     "Activity: <what students do>. Modalities: [choose from {LEARNING_STYLE_TAGS}]. Online: <platform(s) + brief directions>. Offline: <materials/alternative>."
   - Choose widely available, classroom-friendly platforms ONLY (names only, no URLs): Google Docs/Slides, Padlet, Nearpod, Pear Deck, Flip, Quizizz, Kahoot!, Edpuzzle, CommonLit, Newsela, FigJam, Miro, Canva, Smithsonian Learning Lab, Library of Congress.
   - Integrate tasteful Fine Arts options when relevant.

GENERAL RULES
- Match the developmental level of {req.grade}
- Use inclusive, accessible language
- Vary modalities
- Keep items concise (≤ 26 words)
- Output ONLY the JSON
""".strip()

            req = GenerationRequest(
                grade=grade,
                subject=subject,
                standard=row["StandardCode"],
                standard_code=row["StandardCode"],
                subcategory=row.get("Subcategory", ""),
                description=row.get("Description", "")
            )

            client = OpenAI(api_key=api_key)
            try:
                res = client.chat.completions.create(
                    model=DEFAULT_MODEL,
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    messages=[
                        {"role": "system", "content": "Return ONLY a JSON object. No markdown, no commentary."},
                        {"role": "user", "content": build_prompt(req)},
                    ],
                )
                content = res.choices[0].message.content
                plan = json.loads(content)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()

            def bullets(title, items):
                if not items:
                    return ""

                formatted = []
                for x in items:
                    if isinstance(x, dict):
                        if "Activity" in x:
                            formatted.append(f"- {x['Activity']}")
                        elif all(k in x for k in ["objective", "assessment_method"]) and ("threshold" in x or "success_criterion" in x):
                            criterion = x.get("threshold") or x.get("success_criterion")
                            formatted.append(
                                f"- {x['objective']} ({x['assessment_method']}: {criterion})"
                            )
                        else:
                            formatted.append(f"- {json.dumps(x)}")
                    else:
                        formatted.append(f"- {x}")

                return f"**{title}**\n" + "\n".join(formatted) + "\n"


            def to_md(plan: Dict[str, Any]):
                parts = []
                cd = plan.get("curriculum_developer", {})
                obj = cd.get("objectives", {})
                parts.append("# Curriculum Developer\n")
                parts.append(bullets("Knowledge Objectives", obj.get("knowledge", [])))
                parts.append(bullets("Skill Objectives", obj.get("skills", [])))
                parts.append(bullets("Benchmarks", cd.get("benchmarks", [])))

                sf = plan.get("student_friendly", {})
                parts.append("\n# Student-Friendly\n")
                parts.append(bullets("Goals", sf.get("goals", [])))
                parts.append(bullets("I can…", sf.get("ican_statements", [])))
                parts.append(bullets("How I’ll Show Learning", sf.get("how_ill_show_learning", [])))

                bt = plan.get("blooms_taxonomy_activities", {})
                parts.append("\n# Bloom’s Activities\n")
                for lvl in ["remembering", "understanding", "applying", "analyzing", "evaluating", "creating"]:
                    parts.append(bullets(lvl.capitalize(), bt.get(lvl, [])))
                return "\n".join([p for p in parts if p])

            markdown_text = to_md(plan)
            st.markdown(markdown_text)
            st.download_button("📥 Download Markdown", markdown_text, file_name="plan.md")
    else:
        st.info("Enter all inputs and click 'Generate Plan'.")

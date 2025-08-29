# 📚 Standards-Based Curriculum Generator with Bloom's Taxonomy Integration

A Streamlit-powered application for curriculum designers, instructional coaches, and educators to generate **learning objectives**, **benchmarks**, and **Bloom’s Taxonomy-aligned activities** based on the **Common Core State Standards (CCSS)** for **ELA and Math**.

---

## 🎯 Purpose

This tool is designed to streamline instructional planning by generating structured and personalized content for specific standards. It transforms CCSS entries into actionable and measurable:

- **SWBAT Objectives**  
- **Student-friendly goals and "I can" statements**  
- **Benchmarks with assessment criteria**  
- **Classroom activities using Bloom's Taxonomy**

All outputs are optimized for clarity, accessibility, and classroom implementation.

---

## 🧠 What is Bloom’s Taxonomy?

**Bloom’s Taxonomy** is a hierarchical classification of cognitive skills educators use to create effective learning objectives. It includes six levels:

1. **Remembering** – recalling information  
2. **Understanding** – explaining ideas or concepts  
3. **Applying** – using knowledge in new situations  
4. **Analyzing** – drawing connections  
5. **Evaluating** – justifying decisions  
6. **Creating** – producing original work

This app generates two custom activity ideas for each level, ensuring a diverse and well-rounded instructional approach.

---

## 🗂️ Features

- ✅ Select grade, subject, and standard from a CCSS-based dataset (ELA & Math).
- ✏️ Generate clear and measurable **SWBAT objectives**.
- 👦👧 Create **student-friendly goals**, including *“I can…”* statements.
- 🧪 Define **benchmarks** with measurable outcomes (e.g., “80% accuracy”).
- 🎲 Receive two suggested classroom activities per Bloom's level, with varied learning modalities.
- ⬇️ Download the output as a **Markdown file** for easy documentation or sharing.

---

## 🧰 Technologies Used

| Tool        | Purpose                            |
|-------------|------------------------------------|
| **Streamlit** | Interactive web app interface     |
| **Pandas**   | Data filtering and transformation |
| **OpenAI GPT-4o-mini** | Content generation        |

---

## 📁 Project Structure

project/
│
├── app.py # Main Streamlit application
├── ccc (1).csv # Standards CSV (Common Core for ELA & Math)
├── requirements.txt # Required Python libraries
└── README.md # This file

yaml
Copy code

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ccss-curriculum-planner.git
cd ccss-curriculum-planner
2. Install Dependencies
Use pip to install the required packages:

bash
Copy code
pip install -r requirements.txt
3. Add Your CSV File
Ensure your ccc (1).csv file is located in the root directory. The file should contain these columns:

Grade

Subject

StandardCode

Description

(Optional: Subcategory)

4. Launch the App
bash
Copy code
streamlit run app.py
You will be prompted to enter your OpenAI API Key in the app interface.

☁️ Streamlit Cloud Deployment
To deploy online:

Push this repo to GitHub.

Create a free account at Streamlit Cloud.

Connect your repo and deploy.

Optionally, configure the OPENAI_API_KEY via Streamlit Secrets.

🔐 API Key
This app requires an OpenAI API Key to function. You can obtain one at platform.openai.com.

The model used is gpt-4o-mini.

📄 License
This project is licensed under the MIT License.
You are free to use, modify, and share it with attribution.

🙋‍♀️ Questions or Feedback?
If you encounter issues or want to suggest improvements, feel free to open an issue or contribute via pull requests.

Built for thoughtful educators. Powered by AI. 💡

yaml
Copy code

---

### ✅ Optional: Add `.gitignore`

To avoid uploading unnecessary files:

```txt
__pycache__/
*.pyc
.env
*.csv
*.md~
.DS_Store

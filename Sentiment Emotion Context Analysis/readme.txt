# **Sentiment, Emotion, Context (SEC) Application**

The **Sentiment, Emotion, Context (SEC)** application is a user-friendly, Streamlit-based tool for analyzing text data to uncover **sentiment**, **emotion**, and **contextual insights**. This application is designed to handle both individual text inputs and batch CSV uploads, generating insights in the form of summaries, visualizations, and downloadable reports.

---

## **Key Features**

### 1. **Sentiment Analysis**
- Detect whether a text expresses **positive**, **negative**, or **neutral** sentiment using a fine-tuned **Hugging Face model** (`cardiffnlp/twitter-roberta-base-sentiment-latest`).

### 2. **Emotion Detection**
- Classify text into one of 70+ predefined emotions grouped under **Positive**, **Negative**, **Complex**, and **Neutral** categories.
- Leverages **Anthropic's Claude** for precise emotion detection with contextual understanding.

### 3. **Contextual Considerations**
- Generate a broader analysis of cultural, economic, political, or historical factors influencing text sentiment and emotion.
- Provides insights into prevalent rhetorical devices.

### 4. **Batch and Single Text Analysis**
- Analyze multiple texts via CSV upload or single texts entered manually.

### 5. **Comprehensive Reporting**
- Generate detailed reports summarizing sentiment and emotion distributions.
- Export results in **CSV** or **color PDF** formats.

### 6. **Interactive Visualizations**
- Visualize sentiment distribution (bar chart) and emotion distribution (pie chart) using **Plotly**.

---

## **Technologies Used**

- **Streamlit**: User interface and interactive experience.
- **Transformers by Hugging Face**: Sentiment analysis model.
- **Anthropic API**: Emotion detection and contextual analysis.
- **Plotly**: Data visualization.
- **ReportLab**: PDF report generation.
- **Pandas**: Data manipulation.
- **NumPy**: Data processing support.
- **Python Libraries**: Core tools include `datetime`, `os`, `dotenv`, and `logging`.

---

## **Setup and Installation**

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-repo/sentiment-emotion-context.git
cd sentiment-emotion-context
```

### 2. **Install Dependencies**
Ensure Python 3.8+ is installed, then run:
```bash
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**
Create a `.env` file in the project root and add the following keys:
```env
HUGGINGFACE_API_KEY=your_huggingface_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 4. **Run the Application**
```bash
streamlit run current2.py
```

---

## **How to Use**

### **Single Text Analysis**
1. Navigate to the **Single Text Analysis** tab.
2. Enter text in the text area and click **Analyze Texts**.
3. View results in real-time, including sentiment, emotion, and optional context considerations.

### **Batch Analysis (CSV Upload)**
1. Navigate to the **Batch Analysis (CSV)** tab.
2. Upload a CSV file with a single column named `text`.
3. Click **Analyze Texts** to process all rows.
4. Access visualizations, summaries, and downloadable reports.

---

## **Output Features**

### **Summary**
- Sentiment and emotion distribution.
- Key insights on dominant sentiment and emotion.
- Overall emotional tone.

### **Visualizations**
- **Sentiment Bar Chart**: Distribution of positive, negative, and neutral sentiments.
- **Emotion Pie Chart**: Proportion of top emotions in the dataset.

### **Downloadable Reports**
- **CSV**: Raw analysis results for all texts.
- **PDF**: Color-coded report with summaries, contextual considerations, and charts.

---

## **Customization**

### **Emotion Detection Provider**
- Default: **Anthropic's Claude API**.
- This can be updated for other providers by modifying the `SentimentEmotionAnalyzer` class.

### **API Keys**
- Update hard-coded keys to use environment variables for production environments by following the setup instructions.

---

## **Common Issues and Solutions**

### 1. **Error Initializing Sentiment Model**
- Ensure that the Hugging Face pipeline is correctly installed and configured.
- Verify `torch` is installed and GPU support is enabled if available.

### 2. **CSV Upload Issues**
- Ensure the CSV has a column named `text`.
- Remove unnecessary columns before uploading.

### 3. **Anthropic API Errors**
- Verify the `ANTHROPIC_API_KEY` is valid and has sufficient quota.

### 4. **PDF Generation Errors**
- Confirm all dependencies (`reportlab`, `io`, etc.) are installed.

---

## **Roadmap**
---

## **Contributing**

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed documentation.

---

## **Contact**

For questions, suggestions, or support, please contact:
- **Email**: jdevin.rodgers@gail.com
- **GitHub**: [Your GitHub Link](https://github.com/portfolio)

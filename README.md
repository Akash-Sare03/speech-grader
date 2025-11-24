# Speech Grader AI

An AI-powered tool that analyzes and scores student self-introductions based on communication rubrics. The tool provides detailed feedback on content, delivery, language, and engagement aspects of speech.

---

## 🚀 Live Demo

**Try the application now:** [Speech Grader AI Live Demo](https://speech-grader.streamlit.app/)

*No installation required - use directly in your browser!*

---

## 📊 Output Formats

The application provides analysis results in **two formats**:

### 1. User Interface (UI) Output
- Clean, visual display of scores and feedback
- Detailed breakdown by categories
- Improvement suggestions
- Progress indicators

### 2. JSON Output
- Structured data format for programmatic use
- Downloadable JSON file
- Contains all scores, feedback, and metadata
- Compatible with APIs and other applications

#### JSON Structure Example:
```json
{
  "overall_score": 85,
  "word_count": 150,
  "criteria": [
    {
      "criterion": "Content & Structure",
      "score": 35,
      "max_score": 40,
      "components": [
        {
          "name": "Salutation",
          "score": 4,
          "max_score": 5,
          "feedback": "Good salutation found"
        }
      ]
    }
  ],
  "improvement_suggestions": ["Suggestion 1", "Suggestion 2"]
}
```
---

## Features

- **Content Analysis**: Checks salutation, keyword presence, and flow structure
- **Speech Rate Analysis**: Calculates words per minute and provides pace feedback
- **Grammar & Vocabulary Assessment**: Evaluates spoken grammar and vocabulary diversity
- **Clarity Measurement**: Detects filler words and provides clarity scores
- **Sentiment Analysis**: Assesses positivity and engagement level
- **Detailed Feedback**: Provides specific, actionable improvement suggestions

## Scoring Formula

The tool uses a comprehensive 100-point scoring system:

### Content & Structure (40 points)
- **Salutation (5 pts)**: Greeting quality and appropriateness
- **Keyword Presence (30 pts)**: 
  - Must-have keywords (20 pts): Name, age, school/class, family, hobbies
  - Good-to-have keywords (10 pts): Family details, goals, fun facts, achievements
- **Flow (5 pts)**: Structure and organization of the introduction

### Delivery & Style (60 points)
- **Speech Rate (10 pts)**: Words per minute (111-140 WPM ideal)
- **Grammar & Language (20 pts)**:
  - Grammar (10 pts): Error rate and sentence structure
  - Vocabulary (10 pts): Type-Token Ratio (TTR) for diversity
- **Clarity (15 pts)**: Filler word rate and speech clarity
- **Engagement (15 pts)**: Sentiment analysis and positivity level

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. **Clone the repository**
    ```
   git clone https://github.com/Akash-Sare03/speech-grader.git
   cd speech-grader
    ```

2. **Create virtual environment**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install dependencies**
    ```
    pip install -r requirements.txt

    also run the setup_nltk.py (Optional helper) : pyhton setup_nltk.py
    ```
4. Run the application
    ```
    streamlit run app.py
    ```
5. Open your browser

    - Navigate to http://localhost:8501

    - The app will automatically open in your default browser

## Usage

- Paste Transcript: Copy and paste the student's self-introduction text

- Set Duration: Enter the speech duration in seconds (optional)

- Analyze: Click "Analyze Speech" to get comprehensive feedback

- Review Results: Examine scores and improvement suggestions


## 🎥 Demo Video

**Watch the complete demo video to see all features in action:**

[![Demo Video Thumbnail](https://img.shields.io/badge/🎥-Watch_Demo_Video-red?style=for-the-badge&logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1rtGjKUAclQ----agEbyM9rem44iPwsiC/view?usp=sharing)

*Click the button above to watch the full demonstration!*

## Technology Stack

- Backend: Python

- Web Framework: Streamlit

- NLP Libraries: NLTK, VADER, TextBlob, LexicalRichness

- Grammar Checking: Rule-based system with TextBlob

---

## Documentation
- [Local Deployment Guide (PDF)](DEPLOYMENT_GUIDE.pdf)

---
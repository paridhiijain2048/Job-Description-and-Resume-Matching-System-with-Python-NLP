
# 🧠 Job Description and Resume Matching System with Python NLP

This project is a web-based application that streamlines the hiring process by matching a job description with multiple uploaded resumes using both traditional NLP (TF-IDF) and deep learning embeddings (Sentence-BERT).

It extracts text from resumes in PDF, DOCX, or TXT formats and uses semantic similarity techniques to rank resumes based on how well they match the provided job description.

## 🚀 Features

- **Job Description Input**  
  Recruiters can directly input or paste a job description into the web interface.

- **Resume Upload**  
  Upload multiple resumes in various formats (.pdf, .docx, .txt) for comparison.

- **Automated Text Extraction**  
  Extracts text from uploaded resumes using PyPDF2, docx2txt, or plain text reading.

- **Similarity Matching Algorithms**  
  - **TF-IDF** vectorization for keyword-based matching  
  - **Sentence-BERT** for deep semantic similarity analysis

- **Similarity Scoring & Ranking**  
  Each resume is scored and ranked based on how well it matches the job description.

- **Result Presentation**  
  Displays ranked resumes in the UI with match percentages and filenames

---

## 🧪 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/paridhiijain2048/job-resume-matcher.git
   cd job-resume-matcher
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app**
   ```bash
   python main.py
   ```

The app will be accessible at: [http://127.0.0.1:5004/](http://127.0.0.1:5004/)

---

## 🖼️ Screenshots

### 📝 Resume Upload & Matching View

<img width="1470" alt="Screenshot 2025-05-31 at 23 06 35" src="https://github.com/user-attachments/assets/2c970ad4-1e10-4663-b82c-1048d19cfa06" />

<img width="1470" alt="Screenshot 2025-05-31 at 23 06 23" src="https://github.com/user-attachments/assets/87fdaae5-6bf5-4a52-9057-1cf489cce3f9" />

### 📊 Comparison between Sentence-BERT and TF-IDF

<img width="1141" alt="Screenshot 2025-05-31 at 23 07 37" src="https://github.com/user-attachments/assets/ba9872e2-9c35-45a1-8716-e0f2029b3583" />

---

## 🧭 Future Improvements

- Use LLMs (like GPT or LLaMA) for better document understanding  
- Add applicant tracking dashboard  
- Integrate Named Entity Recognition (NER) for better skill extraction  
- Allow parsing LinkedIn profiles or URLs  
- Allow multiple job descriptions

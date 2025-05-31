# main.py (modified to include Sentence-BERT & save both methods)

from flask import Flask, request, render_template
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model = SentenceTransformer('all-MiniLM-L6-v2')  # Load SBERT model

# Helper functions
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        return ""

@app.route("/")
def match_resume():
    return render_template('jobmatcher.html')

@app.route("/matcher", methods=['GET', 'POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description')
        resume_files = request.files.getlist('resumes')

        if not job_description.strip() or not resume_files or all(f.filename == '' for f in resume_files):
            return render_template('jobmatcher.html', message="Please upload Resumes and Job Description")

        resumes_text = []
        resume_names = []

        for resume_file in resume_files:
            if resume_file.filename == '':
                continue
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            resume_names.append(resume_file.filename)
            resumes_text.append(extract_text(filename))

        # === TF-IDF Matching ===
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([job_description] + resumes_text)
        vectors = tfidf_matrix.toarray()
        job_vector = vectors[0]
        resumes_vector = vectors[1:]
        tfidf_similarities = cosine_similarity([job_vector], resumes_vector)[0]

        # === SBERT Matching ===
        sbert_embeddings = model.encode([job_description] + resumes_text)
        job_embed = sbert_embeddings[0]
        resumes_embed = sbert_embeddings[1:]
        sbert_similarities = util.cos_sim([job_embed], resumes_embed)[0].cpu().tolist()

        # Ranking based on SBERT similarity
        top_indices = sorted(range(len(sbert_similarities)), key=lambda i: sbert_similarities[i], reverse=True)
        top_resumes = [resume_names[i] for i in top_indices]
        similarity_scores = [round(sbert_similarities[i], 2) for i in top_indices]

        # Save both results
        with open('results_tfidf.json', 'w') as f:
            json.dump(dict(zip(resume_names, map(lambda s: round(s, 2), tfidf_similarities))), f, indent=4)

        with open('results_sbert.json', 'w') as f:
            json.dump(dict(zip(resume_names, map(lambda s: round(s, 2), sbert_similarities))), f, indent=4)

        return render_template('jobmatcher.html', message="Resumes processed successfully",
                               top_resumes=top_resumes,
                               similarity_scores=similarity_scores)

    return render_template('jobmatcher.html')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5006)

# AskMyDoc

**AskMyDoc** is an AI-powered document assistant built with **Streamlit**, **FAISS**, and **Large Language Models (LLMs)**. It enables users to upload PDF documents, ask natural language questions, and receive context-aware answers instantly.


##  Features

* Upload and process multiple PDF documents.
* Extracts and chunks text intelligently for embedding.
* Vector search with **FAISS* for efficient document retrieval.
* Context-aware answers generated via **Groq API (LLaMA-3)**.
* Interactive and responsive UI built with **Streamlit**.
* Dark/Light theme toggle for personalized user experience.
* Integrated **Lottie animations** for improved user engagement.



## 🛠 Tech Stack

* **Frontend/UI**: [Streamlit](https://streamlit.io/)
* **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss)
* **Embeddings**: [Sentence Transformers (MiniLM-L6-v2)](https://www.sbert.net/)
* **Model API**: [Groq LLaMA-3](https://groq.com/)
* **PDF Parsing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)

---

## 📂 Project Structure

```
AskMyDoc/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

---

## ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/askmydoc.git
   cd askmydoc
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   * Create a `.env` file and add your **Groq API Key**:

     ```
     GROQ_API_KEY=your_api_key_here
     ```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

1. Open the app in your browser (usually at `http://localhost:8501`).
2. Upload one or more PDF documents.
3. Ask your question in plain English.
4. View accurate, context-based answers extracted from your documents.

---

## 📊 Example Workflow

1. Upload a research paper PDF.
2. Ask: *“What is the main conclusion of this study?”*
3. The app retrieves the most relevant passages and provides a concise, AI-generated answer.

---

## 🔒 Security Notice

* Your API keys must be kept private.
* Do not hard-code keys directly in the application (use `.env` or secrets manager).

---

## 🤝 Contributing

Contributions are welcome!

* Fork the repo
* Create a feature branch
* Submit a pull request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👩‍💻 Author

Developed by **Khadija Muskan**
AI/ML Developer – Passionate about applied AI solutions for real-world problems.

---

Would you like me to also prepare a **requirements.txt** file for you (listing all the libraries you used) so that setup is easier for others?

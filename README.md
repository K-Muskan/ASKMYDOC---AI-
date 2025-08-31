# Ask My Doc

Ask My Doc is an AI-powered tool that allows you to **upload documents** (PDF, DOCX, TXT, etc.) and **ask questions in natural language**. It uses state-of-the-art **Large Language Models (LLMs)** with **document embeddings** to retrieve and generate accurate answers from your documents.

---

## 🚀 Features

*  Upload and process multiple documents.
*  Ask natural language questions about the content.
*  Intelligent search powered by embeddings & retrieval.
*  Simple web interface (Streamlit).
*  Local execution – your documents remain private.
*  

----


## ⚙ Configuration

You’ll need an API key from **OpenAI** (or another LLM provider).
```
OPENAI_API_KEY=your_api_key_here
```

----


## ▶ Usage

Run the app using Streamlit:

```bash
streamlit run ASKMYDOC.py
```

Then open the link provided in your terminal (usually `http://localhost:8501`).


##  Example Workflow

1. Upload your document (e.g., `research_paper.pdf`).
2. Ask: *“What are the key findings in this paper?”*
3. The app retrieves relevant sections and generates a concise answer.


----


## Roadmap

* Support for more file types (CSV, PPTX).
* Multi-document Q\&A.
* Option to export summarized notes.



## License
This project is licensed under the **MIT License** – feel free to use and modify it.

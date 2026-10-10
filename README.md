# 📄 AI Document Intelligence System

A production-grade, hybrid client-server Document Intelligence application powered by **Mistral-7B LLM**, **FAISS Vector Store**, **LangChain Structured Output Parsers**, and **FastAPI**, with a local **Streamlit** user interface.

## 🏛️ System Architecture

- **Backend (Remote Kaggle GPU / T4 x2):**
  - **Inference & RAG Engine:** Mistral-7B-Instruct-v0.2 with `sentence-transformers/all-MiniLM-L6-v2`.
  - **Vector Storage:** FAISS vector database handling document chunking and retrieval.
  - **API Layer:** FastAPI exposed via an HTTPS tunnel (ngrok).
- **Frontend (Local Client):**
  - Interactive Streamlit dashboard for dynamic file upload, executive summary extraction, comparative analysis, and interactive Q&A.

## 🚀 Features

- **Automated Document Intelligence:** Extracts structured JSON schemas (`Document`, `Summary`, `Key Points`, `Risks`, `References`).
- **Interactive Q&A:** Grounded document question answering backed by citation snippets and evidence.
- **Comparative Analysis:** Compares sections, metrics, and criteria across documents with structured verdicts.
- **Dynamic File Processing:** On-the-fly document indexing in memory without static paths.

## 🛠️ Setup & Running
### 1. Remote Backend (Kaggle)
1. Open `notebooks/backend_kaggle.ipynb` in a Kaggle environment with GPU acceleration enabled.
2. Run all cells to launch the FastAPI server and establish the ngrok tunnel.
3. Copy the output public URL (e.g., `[https://xxxx.ngrok-free.app](https://xxxx.ngrok-free.app)`).

### 2. Local Frontend
```bash
# Clone the repository
git clone https://github.com/EyadMohamed07/ai-document-intelligence.git
cd ai-document-intelligence

# Install requirements
pip install -r requirements.txt

# Run the client
streamlit run local_app.py 

```
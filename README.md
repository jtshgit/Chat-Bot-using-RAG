# 🧠 Retrieval-Augmented Generation (RAG) Chatbot

This is a full-stack RAG application powered by **LangChain**, **Groq LLM**, **FAISS vector store**, and **React** frontend. It allows you to upload PDF documents, index them with semantic search, and query them via an interactive chat interface.

---

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── app.py                      # Flask API entry point
│   ├── connect_memory_with_llm.py # LangChain chain that connects vector DB with Groq LLM
│   ├── create_memory_for_llm.py   # PDF ingestion and vector store creation
│   ├── data/                       # Directory for input PDFs
│   ├── vectorstore/db_faiss/      # FAISS index storage
│   ├── .env                       # Environment variables
│   ├── requirements.txt           # Backend dependencies
│   ├── Pipfile / Pipfile.lock     # Optional: pipenv dependency management
│   └── vercel.json                # Optional: deployment config for Vercel
└── frontend/
    └── ...                        # React application (Chat UI)
```

---

## 🛠️ Backend Setup (Python + Flask)

### 🔧 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or use pipenv:

```bash
pipenv install
pipenv shell
```

### 🔐 Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
GROK_API=your_groq_api_key_here
```

### 📄 Step 1: Ingest PDF Documents

Run this to process and chunk PDF files and store in FAISS:

```bash
python create_memory_for_llm.py
```

> Ensure your PDFs are placed in the `backend/data/` directory.

### 🤖 Step 2: Start the Flask API

```bash
python app.py
```

The API will be live at: `http://localhost:5001/api/chat`

---

## 💬 Frontend Setup (React)

### 📦 Install Dependencies

```bash
cd frontend
npm install
```

### 🌐 Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
REACT_APP_API=http://localhost:5001
```

### 🚀 Run the App

```bash
npm start
```

Navigate to `http://localhost:3000` in your browser to use the chat UI.

---

## ✨ Features

* Upload and index PDFs using HuggingFace embeddings and FAISS
* Ask natural language questions and retrieve answers grounded in the uploaded documents
* Groq LLM handles question answering with a custom prompt
* Sources of each answer are returned for transparency
* React-based interactive chat interface

---

## 🧠 Technologies Used

* **Backend**

  * Python, Flask
  * LangChain
  * Groq API (LLM)
  * HuggingFace Transformers (embeddings)
  * FAISS (vector store)

* **Frontend**

  * React
  * Axios
  * Tailwind CSS (optional for styling)

---

## 🚀 Deployment

### Backend on Vercel (Optional)

You can deploy `app.py` via `vercel.json` using Vercel’s Python support.

### Frontend on Vercel/Netlify

Set your environment variable `REACT_APP_API` to your deployed backend API URL.

---

## 📸 Demo Video



https://github.com/user-attachments/assets/d2aaab5a-b121-4827-bb6b-4dda1dd87c52


---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

Let me know if you'd like:

* Docker support
* Markdown formatting for source links
* Advanced RAG strategies like MapReduce or HyDE

I'm happy to help!

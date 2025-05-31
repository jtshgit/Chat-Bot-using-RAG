import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.language_models.llms import LLM
from groq import Groq
from pydantic import Field
from typing import Optional, List

class GroqLLM(LLM):
    model: str = "compound-beta-mini"
    api_key: str = Field(..., exclude=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = Groq(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content


GROQ_API_KEY = os.environ.get("GROK_API")
if not GROQ_API_KEY:
    raise ValueError("Please set the GROK_API environment variable.")

llm = GroqLLM(api_key=GROQ_API_KEY, model="compound-beta-mini")

custom_prompt_template = """
Use the pieces of information provided in the context to answer the user's question.
If you don't know the answer, just say that you don't know; don't try to make up an answer.
Don't provide anything outside of the given context.

Context: {context}
Question: {question}

Start the answer directly. No small talk, please.
"""

def set_custom_prompt(template):
    return PromptTemplate(template=template, input_variables=["context", "question"])

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
DB_FAISS_PATH = "vectorstore/db_faiss"
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": set_custom_prompt(custom_prompt_template)},
)

# user_query = input("Write Query Here: ")
# response = qa_chain.invoke({"query": user_query})

# print("RESULT: ", response["result"])
# print("\nSOURCE DOCUMENTS:")
# for doc in response["source_documents"]:
#     print("-", doc.metadata.get("source", "Unknown source"))


app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    query = data.get("query") or request.args.get("query")

    if not query:
        return jsonify({"error": "Query is missing"}), 400

    response = qa_chain.invoke({"query": query})
    return jsonify({
        "result": response["result"],
        "sources": [doc.metadata.get("source", "Unknown source") for doc in response["source_documents"]],
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
# rag_chain.py
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate

import pandas as pd

# Load the video metadata CSV and create a mapping from ID to filename
metadata_df = pd.read_csv("video_metadata.csv")
video_id_to_filename = dict(zip(metadata_df["id"], metadata_df["file_name"]))

class RAGSystem:
    def __init__(self):
        self.setup_rag()

    def setup_rag(self):
        custom_prompt = PromptTemplate(
            template="""
Answer the question using *only* the context provided below.
If the answer is not contained in the context, respond with "I don't know."

Context:
{context}

Question:
{question}

Answer:
""",
            input_variables=["context", "question"]
        )

        # Load LLaMA model
        self.llm = LlamaCpp(
            model_path=r"D:\audio_rec1\rag_vector\models\tinyllama-1.1b-chat-v1.0.Q4_0.gguf",
            temperature=0.5,
            max_tokens=512,
            top_p=1,
            n_ctx=1024,
            n_threads=8
        )

        embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectordb = Chroma(
            persist_directory="./chroma_db",
            collection_name="transcriptions",
            embedding_function=embedding_function
        )

        retriever = self.vectordb.as_retriever(search_kwargs={"k": 3})

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": custom_prompt},
            return_source_documents=True
        )

    def answer(self, query):
        result = self.qa_chain(query)
        video_ids = {doc.metadata.get("video_id") for doc in result["source_documents"]}
        # Convert to file names
        file_names = [video_id_to_filename.get(video_id, "unknown.mp4") for video_id in video_ids]  
        return {
            "answer": result["result"],
            "sources": file_names
        }

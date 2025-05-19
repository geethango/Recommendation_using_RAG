from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate

# Custom prompt
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
llm = LlamaCpp(
    model_path=r"D:\audio_rec\rag_vector\models\tinyllama-1.1b-chat-v1.0.Q4_0.gguf",
    temperature=0.5,
    max_tokens=512,
    top_p=1,
    n_ctx=1024,
    n_threads=8
)

# Load embeddings
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
persist_directory = "./chroma_db"

vectordb = Chroma(
    persist_directory=persist_directory,
    collection_name="transcriptions", 
    
    embedding_function=embedding_function
)

# Optional: Check how many documents are present
try:
    print("Number of documents in ChromaDB:", vectordb._collection.count())
except Exception as e:
    print("Error checking document count:", e)

# Set up retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Set up RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": custom_prompt},
    return_source_documents=True
)

# Run query
query = "How variables used in javascript and java"
result = qa_chain(query)

# Print the unified answer (LangChain combines source context internally)
print("\nAnswer:\n", result["result"])
# Print all unique video IDs used as sources
print("\n--- Source Videos Used ---")
video_ids = {doc.metadata.get("video_id") for doc in result["source_documents"]}
for i, vid in enumerate(video_ids, 1):
    print(f"Source {i} - Video ID: {vid}")
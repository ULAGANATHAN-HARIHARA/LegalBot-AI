import pickle
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load IPC chunks
with open("ipc_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS DB
db = FAISS.from_texts(chunks, embeddings)

# Save FAISS DB
db.save_local("ipc_vector_db")

print("🔥 FAISS Vector DB created successfully!")

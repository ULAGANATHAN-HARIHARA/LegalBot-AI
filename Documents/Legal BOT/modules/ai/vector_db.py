# modules/ai/vector_db.py
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_retriever(db_dir: str = "ipc_vector_db", k: int = 3):
    """
    Load FAISS DB from given directory and return a retriever.
    """
    # Resolve absolute path (avoid OneDrive issues)
    base = os.path.abspath(os.getcwd())
    db_path = os.path.join(base, db_dir)

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"FAISS directory not found: {db_path}")

    # Initialize embeddings (local sentence-transformers)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Load FAISS; allow dangerous deserialization so local indexes load
    db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": k})
    return retriever

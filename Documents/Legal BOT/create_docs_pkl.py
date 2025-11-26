import pickle
from langchain.docstore.document import Document

# Load chunks
with open("ipc_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Convert each chunk into a LangChain Document object
docs = [Document(page_content=chunk, metadata={"source": "IPC"}) for chunk in chunks]

# Save docs.pkl
with open("docs.pkl", "wb") as f:
    pickle.dump(docs, f)

print("✅ docs.pkl created successfully!")
print(f"Total documents saved: {len(docs)}")

import fitz  
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle

pdf_path = r"C:\Users\Hari\OneDrive\Legal BOT\Indian Code Book.pdf"

doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text("text")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_text(text)

with open("ipc_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"✅ Extracted {len(chunks)} chunks from IPC dataset.")

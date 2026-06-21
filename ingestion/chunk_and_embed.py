import os
import uuid
from glob import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "knowledge_base"

def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def main():
    print(f"Connecting to Qdrant at {QDRANT_URL}")
    client = QdrantClient(url=QDRANT_URL)
    
    # Create collection if it doesn't exist
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        print(f"Creating collection '{COLLECTION_NAME}'")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists. Re-creating to clear old data...")
        client.delete_collection(collection_name=COLLECTION_NAME)
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    embeddings_model = get_embeddings_model()
    
    # Load all markdown files
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "infra", "seed"))
    policy_files = glob(os.path.join(base_dir, "policies", "*.md"))
    notes_files = glob(os.path.join(base_dir, "historical_notes", "*.md"))
    
    files_to_process = [("policy", f) for f in policy_files] + [("historical_note", f) for f in notes_files]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )

    points = []
    
    for category, filepath in files_to_process:
        print(f"Processing {category} file: {filepath}")
        loader = TextLoader(filepath)
        documents = loader.load()
        chunks = text_splitter.split_documents(documents)
        
        for i, chunk in enumerate(chunks):
            text = chunk.page_content
            vector = embeddings_model.embed_query(text)
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": text,
                    "category": category,
                    "source": os.path.basename(filepath),
                    "chunk_index": i
                }
            )
            points.append(point)
            
    if points:
        print(f"Upserting {len(points)} chunks into Qdrant...")
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print("Done!")
    else:
        print("No documents found to process.")

if __name__ == "__main__":
    main()

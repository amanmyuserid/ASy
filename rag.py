import re
import spacy
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


def build_vector_database(file_path, max_tokens=200, overlap=1):

    # Load models
    nlp = spacy.load('en_core_web_sm')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Read text from file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
    
    # Clean text
    text = re.sub(r'<[^>]+>', '', text)  # remove HTML tags
    text = re.sub(r'\[\d+\]|\[note \d+\]', '', text)  # remove citations
    text = re.sub(r'/[^/]+/', '', text)  # remove pronunciation marks
    text = re.sub(r'[^A-Za-z0-9\s.,!?]', '', text)  # remove special chars
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split text into sentences using SpaCy
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    # Create chunks
    chunks = []
    current_chunk = []
    current_token_count = 0
    for sentence in sentences:
        # Approx token count: 1 word ~ 1.3 tokens
        token_count = len(sentence.split()) * 1.3
        if current_token_count + token_count <= max_tokens:
            current_chunk.append(sentence)
            current_token_count += token_count
        else:
            chunks.append(" ".join(current_chunk))
            # Maintain overlap
            current_chunk = current_chunk[-overlap:] + [sentence]
            current_token_count = sum(len(s.split()) * 1.3 for s in current_chunk)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    # Generate embeddings for chunks
    embeddings = model.encode(chunks)
    
    # Build FAISS index using cosine similarity (normalize embeddings)
    embeddings_np = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings_np)
    d = embeddings_np.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings_np)
    
    vector_db = {
        'chunks': chunks,
        'embeddings': embeddings_np,
        'index': index,
        'model': model
    }
    return vector_db

def query_vector_database(vector_db, query, top_k=2):
    """
    Given a vector database (as returned by build_vector_database) and a query,
    yeh function:
      1. Encodes the query using the same SentenceTransformer model.
      2. Normalizes the query embedding.
      3. Uses FAISS index to search top_k relevant chunks.
    Returns: retrieved_chunks and their corresponding scores.
    """
    model = vector_db['model']
    chunks = vector_db['chunks']
    index = vector_db['index']
    
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")
    faiss.normalize_L2(query_embedding)
    distances, indices = index.search(query_embedding, top_k)
    retrieved_chunks = [chunks[i] for i in indices[0]]
    scores = distances[0]
    return retrieved_chunks, scores

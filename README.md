# ASy

## Problem

Extract web content (text) from multiple URLs and answer questions based solely on that content. The LLM will generate responses strictly from the website content.

## To run 
1. I have doockerize it  and pushed to docker hub so that you do not need to focus on installing and getting any error 
2. Prerequisite 
      1. Docker should be installed
3. Just use this single line command in terminal: docker run -p 8501:8501 amanmyuserid/my_streamlit_app:latest
4. Open your browser: use http://localhost:8501


## Solution

1. **Extract Content from URLs (3 websites)**
   - Use the `trafilatura` library to extract content from each URL.
   - Save each URL's content in separate text files (e.g., `url1_text.txt`, `url2_text.txt`, `url3_text.txt`).

2. **Save to Vector Database (FAISS)**
   - Convert the text files into chunks using `sentenceTransformer`.
   - Save these chunks into a vector database (FAISS).
   - For a given query, retrieve similar chunks from the vector database.
   - Pass the query along with the retrieved chunks to the LLM (LLAMA 3.3 70B from Groq) to generate the response.


      
      

import streamlit as st
from web_scrap import extract_website_content
from rag import build_vector_database, query_vector_database
from llm import generate_contextual_answer





st.set_page_config(layout="wide")

# Custom CSS for bigger font
st.markdown(
    """
    <style>
    body, .css-18e3th9, .css-10trblm, .stTextInput label, .stTextArea label {
        font-size: 20px !important;
    }
    textarea, input {
        font-size: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Web Content Q&A Tool")

# Initialize session state variables once
if "answer" not in st.session_state:
    st.session_state["answer"] = ""
if "prev_url1" not in st.session_state:
    st.session_state["prev_url1"] = ""
if "prev_url2" not in st.session_state:
    st.session_state["prev_url2"] = ""
if "prev_url3" not in st.session_state:
    st.session_state["prev_url3"] = ""
if "url1_db" not in st.session_state:
    st.session_state["url1_db"] = None
if "url2_db" not in st.session_state:
    st.session_state["url2_db"] = None
if "url3_db" not in st.session_state:
    st.session_state["url3_db"] = None
if "result1" not in st.session_state:
    st.session_state["result1"] = None 
if "result2" not in st.session_state:
    st.session_state["result2"] = None 
if "result3" not in st.session_state:
    st.session_state["result3"] = None            

# Create two columns: left for URL + Question + Get Answer, right for Answer
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("URL Input")
    
    
    
    url1 = st.text_input("URL 1", placeholder="Enter first URL here")
    url2 = st.text_input("URL 2", placeholder="Enter second URL here")
    url3 = st.text_input("URL 3", placeholder="Enter third URL here")
    
    st.subheader("Question")
    question = st.text_area("Your Question", height=250)

    if st.button("Get Answer"):
        

        # Process URL1 only if changed
        if url1 and url1 != st.session_state["prev_url1"]:
            print("Processing URL 1")
            try:
                st.session_state["result1"] = extract_website_content(url1, "url1_text.txt")
                st.session_state["prev_url1"] = url1
                if st.session_state["result1"]:
                    
                    st.session_state["url1_db"] = build_vector_database("url1_text.txt")
            except Exception as e:
                st.error(f"Error in processing URL 1: {e}")

        # Process URL2 only if changed
        if url2 and url2 != st.session_state["prev_url2"]:
            try:
                st.session_state["result2"] = extract_website_content(url2, "url2_text.txt")
                st.session_state["prev_url2"] = url2
                if st.session_state["result2"]:
                    
                    st.session_state["url2_db"] = build_vector_database("url2_text.txt")
                

            except Exception as e:
                st.error(f"Error in processing URL 2: {e}")

        # Process URL3 only if changed
        if url3 and url3 != st.session_state["prev_url3"]:
            try:
                st.session_state["result3"] = extract_website_content(url3, "url3_text.txt")
                st.session_state["prev_url3"] = url3
                if st.session_state["result3"]:
                    
                    st.session_state["url3_db"] = build_vector_database("url3_text.txt")
            except Exception as e:
                st.error(f"Error in processing URL 3: {e}")

        try:
            combined_context = ""
            # Query each database if available
            if st.session_state["url1_db"] and st.session_state["result1"]:
                results, _ = query_vector_database(st.session_state["url1_db"], question, top_k=2)
                combined_context += "\n".join(results) + "\n"
            if st.session_state["url2_db"] and st.session_state["result2"]:
                results, _ = query_vector_database(st.session_state["url2_db"], question, top_k=2)
                combined_context += "\n".join(results) + "\n"
            if st.session_state["url3_db"] and st.session_state["result3"]:
                results, _ = query_vector_database(st.session_state["url3_db"], question, top_k=2)
                combined_context += "\n".join(results) + "\n"
            
            answer = generate_contextual_answer(question, combined_context)
            st.session_state["answer"] = answer
        except Exception as e:
            st.session_state["answer"] = f"Error in generating answer: {e}"

with col_right:
    st.subheader("Answer")
    st.text_area("Results will be displayed here", value=st.session_state["answer"], height=400)

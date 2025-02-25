from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()

def generate_contextual_answer(query: str, context: str):
    system_prompt = """
    You are an expert at answering queries strictly based on the provided context.
    Your response should be concise, professional, and use only the exact information from the context.
    Do not add any extra explanation or general knowledge.
    If the provided context does not explicitly contain the information required to accurately answer the query,
    respond with exactly: "Insufficient information provided to generate an answer."
    """
    
    initial_prompt = f"""
    Context:
    {context}
    
    Query: {query}
    
    Provide a concise answer strictly using the provided context.
    """
    
    try:
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        client = Groq(api_key=groq_api_key)
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": initial_prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
            stream=False
        )
        
        answer = completion.choices[0].message.content.strip()
        
        return answer
        
    except Exception as e:
        print("Error generating answer:", e)
        return None

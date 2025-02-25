# # example_usage.py
# from rag3 import EmbeddingRetriever

# # Instance create karo
# retriever = EmbeddingRetriever(max_tokens=200, overlap=1)

# # Apni file process karo; baaki sab automatic ho jayega
# retriever.process_file('url1_text.txt')

# # Query run karo aur results retrieve karo
# query = "Where was Einstein born?"
# results, scores = retriever.retrieve(query, top_k=2)

# print("Query Results:")
# for i, (chunk, score) in enumerate(zip(results, scores), 1):
#     print(f"{i}. Score: {score:.4f}\n{chunk}\n")





# from llm import generate_contextual_answer

# def main():
#     # English query pooch rahe hain:
#     query = "Tree can sing?"
    
#     # Yeh wrong story hai jisme sab kuch galat information hai:
#     context = """
#     Once upon a time in the land of Bizarro World, all birds were born with fins instead of wings.
#     The sky was filled with water, so birds swam gracefully in the clouds.
#     Trees could sing, and the sun set in the north.
#     Everything in this world defied normal logic and reality.
#     """
    
#     # Function call karke answer prapt karte hain:
#     answer = generate_contextual_answer(query, context)
    
#     # Answer print kar rahe hain:
#     print("Answer from LLM:", answer)

# if __name__ == '__main__':
#     main()



# from rag3 import EmbeddingRetriever
# from llm import generate_contextual_answer

# def main():
#     # EmbeddingRetriever ka instance create karo aur file process karo
#     retriever = EmbeddingRetriever(max_tokens=200, overlap=1)
#     retriever.process_file('url1_text.txt')
    
#     # Query run karo aur context chunks retrieve karo
#     query = "When was Einstein born?"
#     results, scores = retriever.retrieve(query, top_k=2)
    
#     print("Query Results:")
#     for i, (chunk, score) in enumerate(zip(results, scores), 1):
#         print(f"{i}. Score: {score:.4f}\n{chunk}\n")
    
#     # Retrieved context chunks ko merge karke ek combined context banao
#     combined_context = "\n".join(results)
    
#     # Combined context ke basis par LLM se answer generate karo
#     answer = generate_contextual_answer(query, combined_context)
    
#     print("\nAnswer from LLM:")
#     print(answer)

# if __name__ == '__main__':
#     main()

import numpy as np 
print("numpy version ", np.version.version)
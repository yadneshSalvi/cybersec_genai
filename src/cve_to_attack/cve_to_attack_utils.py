from langchain.prompts import PromptTemplate
from ..embeddings.chroma import chroma_openai_cwe_collection, chroma_openai_attack_collection

cve_to_attack_prompt = PromptTemplate(
	input_variables=["query"],
	template="""
You are a cyber-security expert and will answer the following question.
Question: '''{query}'''
"""
    )

def make_cve_to_attack_prompt(query):
    similar_cves = chroma_openai_cwe_collection.query(
			query_texts=query, 
			n_results=5
		)
    print(similar_cves)
    return cve_to_attack_prompt
    
from langchain.prompts import PromptTemplate

ask_gpt_prompt = PromptTemplate(
        input_variables=["question"],
        template="""
You are a cyber-security expert and will answer the following question.
Question: '''{question}'''
"""
    )
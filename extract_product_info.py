from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

# Prompt the user to paste multiline product catalog text
def get_multiline_input(prompt="Paste product specification info (end with a blank line):"):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)
   
# Extract product info from pasted catalog text using LLM
def product_info():
    url_content = get_multiline_input()

    print ("\n--- URL content provided ---\n")
    print(url_content)

    # Define the prompt for extracting product lines
    product_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert product data extractor. Return all extracted lines as a JSON array of strings. Return ONLY raw JSON array, without any extra explanation or text."),
        ("human", "Extract and return JSON object based on the catalog information here:\n{catalog_text}")
    ])

    # Format the message and send them to the LLM 
    product_formatted_messages = product_prompt.format_messages(catalog_text=url_content)
    llm = ChatOllama(
        model="llama3.2", 
        temperature=0.0, 
        format="json"
    )
    product_response = llm.invoke(product_formatted_messages)

    print("\n------ Product Info Output ------\n")
    product_info_json = json.loads(product_response.content)
    print(product_info_json)

    return product_info_json

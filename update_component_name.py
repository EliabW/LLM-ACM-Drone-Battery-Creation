from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import re
import json

# Update the <Component> tag's Name attribute using the JSON Model value
def update_component(acm_path, final_json):
    # load the reference ACM XML content from the file (default reading mode)
    with open(acm_path) as file:
        xml_content = file.read()
 
    # Extract the opening tag
    component_tag_match = re.search(r'<Component\b[^>]*>', xml_content)
    component_tag = component_tag_match.group()
        
    # Prompt guide the LLM to update the Name attribute
    component_prompt = ChatPromptTemplate.from_messages([
        ("system", """
         Update ONLY the <Component> tag's Name attribute to the JSON MODEL value. 
         Format it so the name uses only underscores between words (remove all symbols or extra spaces).
         Output ONLY the updated opening <Component> tag, no explanations.
         """),

        ("human",
        """
        <Component> opening tag:
        {component_xml}

        JSON MODEL value:
        {json_model}
        """)
    ])

    # Format the message using the catalog input and reference baseline
    component_formatted_messages = component_prompt.format_messages(
        component_xml=component_tag,
        json_model=json.dumps(final_json.get("MODEL"))
        )
    llm = ChatOllama(
        model="llama3.2", 
        temperature=0.0
    )
    component_response = llm.invoke(component_formatted_messages)

    print("\n------ Updated component Name ACM ------\n")
    updated_component_tag = component_response.content
    print(updated_component_tag)

    return updated_component_tag
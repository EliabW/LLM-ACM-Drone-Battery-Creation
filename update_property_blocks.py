from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import re
import json

# Update the ACM <Property> blocks using JSON data via LLM
def update_property(acm_path, final_json):
    # load the reference ACM XML content from the file (default reading mode)
    with open(acm_path) as file:
        xml_content = file.read()
 
    # Extract all property block
    property_blocks = re.findall(r'(<Propert[^>]*>.*?</Property>)', xml_content, flags=re.DOTALL)
        
    # prompt to guide the LLM 
    property_system_prompt = """
    You will be given one XML <Property> block and a JSON object.

    1. Find the Name attribute in the <Property> block (e.g., Name="LENGTH").
    2. Match this name to a key in the JSON object.
    3. If a match is found, update the content inside the <Value> tag with the corresponding JSON value.
    4. If no match is found, return the original XML block unchanged.
    5. If the JSON value is null or empty, replace the <Value> tag with a self-closing <Value /> (no whitespace inside).
    6. Remove any extra characters like braces from the JSON value (e.g., {{LiPo}} -> LiPo).
    7. Return only the updated <Property> XML block as raw XML — no explanations, comments, or extra text.
    """


    property_human_prompt = """
    <Property> block:
    {property_xml}

    JSON data for this property:
    {json_data}
    """

    llm = ChatOllama(
        model="llama3.2", 
        temperature=0.0)

    property_prompt = ChatPromptTemplate.from_messages([
        ("system", property_system_prompt),
        ("human", property_human_prompt)
    ])

    # Update the Property blocks 
    updated_properties = []
    for prop_xml in property_blocks:
        # Extract property name attribute
        name_match = re.search(r'Name="([^"]+)"', prop_xml)
        if not name_match:
            updated_properties.append(prop_xml)
            continue
        prop_name = name_match.group(1)

        # Prepare JSON for this property only 
        prop_json_value = final_json.get(prop_name)
        if prop_json_value is None:
            # No update available
            updated_properties.append(prop_xml)
            continue

        # If the value is a dictionary (like ROTATION), send it as is
        prop_json = {prop_name: prop_json_value}

        # give the LLM the matching <Property> block and its JSON key-value to update
        formatted_property_prompt = property_prompt.format(
            property_xml=prop_xml,
            json_data=json.dumps(prop_json, separators=(",", ":")) # compacts JSON to use fewer LLM tokens
        )

        response = llm.invoke(formatted_property_prompt)
        updated_properties.append(response.content)

    print("--- Updated property ACM XML ---")
    for i in range(len(updated_properties)):
        print(updated_properties[i])

    return updated_properties
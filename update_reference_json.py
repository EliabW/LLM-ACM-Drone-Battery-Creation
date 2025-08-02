from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

# Use LLM to update a reference battery JSON using catalog data 
def update_reference_json_from_catalog(catalog_json, reference_json):
    # Prompt guide the LLM to match values from catalog to the reference structure
    json_prompt = ChatPromptTemplate.from_messages([
        ("system", 
        """
        You are an expert data extractor and transformer. Given a reference JSON, update its keys using catalog data, ensuring exact data type and format matches.
        1. Dimensions:
            - Split sizes (e.g. 34x23x12) by "x"
            - LENGTH = longest, WIDTH = mid, HEIGHT/THICKNESS = shortest
        2. Identification:
            - MODEL: use exact name or brand provided from the catalog data; only use dash (-) as separator
            - NUMBER_OF_CELLS: extract configs like "2S1P".
        3. Numeric (units removed, properly formatted):
            - VOLTAGE: remove "V" (8.2 V -> 8.2).
            - CAPACITY: remove "mAh" (e.g. 4,200 mAH -> 4200).
            - COST: remove currency symbols "$". (e.g., $12.99 -> 12.99)
            - WEIGHT: convert to kg (e.g., 50 -> .50) 
            - CONT_DISCHARGE_RATE, PEAK_DISCHARGE_RATE: remove "C".
        4. Complex:
            - ROTATION: keep as is unless catalog provides matching nested data.

        If no match, keep original value. 
        All numeric conversions must match reference data type and format
        """),


        ("human",
        """
        You are given Two JSON objects:
        Reference JSON:
        {ref_data}

        Catalog Data:
        {catalog_data}

        Update the Reference JSON by mapping values from the Catalog Data as per the system instructions.
        """)
    ])

    # Format the message using the catalog input and reference baseline
    json_formatted_messages = json_prompt.format_messages(
        ref_data=json.dumps(reference_json, separators=(",",":")),
        catalog_data=json.dumps(catalog_json, separators=(",",":"))
        )
    llm = ChatOllama(
        model="llama3.2", 
        temperature=0.0, 
        format="json"
    )
    json_response = llm.invoke(json_formatted_messages)

    print("\n------ Final Updated JSON ------\n")
    final_json = json.loads(json_response.content)
    print(final_json)

    return final_json
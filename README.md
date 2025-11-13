
# Automated Product Data Integration and ACM File Generation

This project automates the process of integrating **battery product catalog data** into **ACM XML files**, updating both the **component name** and its **property blocks** using an **LLM driven pipeline**.

The workflow simplifies the creation and maintenance of product data within an **ACM (Aerospace Component Model)** framework.  
The generated `.acm` files are compatible with the **Generic Modeling Environment (GME)** and CyPhyML based workflows.

## Workflow

The notebook (**`main.ipynb`**) performs the following steps to generate an updated ACM file:

1. **Product Info Extraction**  
   - Prompts the user for multiline product catalog text.  
   - An LLM extracts product specifications into a structured JSON (`catalog_json`).

2. **Reference JSON Update**  
   - Combines the `catalog_json` with a predefined `reference_json` (battery defaults).  
   - Produces a cleaned and standardized `final_json`.

3. **Component Name Update**  
   - Reads the reference ACM XML (e.g., `battery_test.acm`).  
   - Updates the component’s `Name` attribute based on the `MODEL` in `final_json`.

4. **Property Block Update**  
   - Iterates through all `<Property>` blocks in the ACM XML.  
   - Updates values using `final_json` (empty values -> self-closing tags).

5. **ACM File Assembly and Output**  
   - Combines the updated component name and property blocks.  
   - Writes the final `.acm` file, named after the product model.

## Dependencies

- `langchain_ollama` – Interface for Ollama LLMs  
- `langchain_core.prompts.ChatPromptTemplate` – Prompt templating for JSON and XML transformations  
- `re` – Pattern matching for XML parsing and cleaning  
- `json` – JSON parsing and serialization  

**LLM Model:** `llama3.2` (Ollama)  

## Usage

1. **Prepare Your Files**  
   - Place your reference ACM XML file (e.g., `battery_test.acm`) in the project directory.  
   - Ensure you have a valid `reference_json` for the product type.  
     
   > **Note:**  
   > - The notebook currently defaults to `battery_test.acm` as the input file.  
   > - A predefined `reference_json` for a LiPo battery is included in the notebook but can be modified.

2. **Run the Notebook**  
   - Open and execute the notebook, which handles all steps in the workflow.  
   - Ensure Ollama is running with the `llama3.2` model.

3. **Provide Product Data**  
   - When prompted, paste the multiline product catalog text.  
   - The notebook extracts and processes the data into JSON.

4. **Review Outputs**  
   - The notebook will display:  
     - Extracted JSON (`catalog_json`)  
     - Transformed JSON (`final_json`)  
     - Updated ACM component tag and property blocks  
   - A new `.acm` file is written, named after the `MODEL` in `final_json`.  

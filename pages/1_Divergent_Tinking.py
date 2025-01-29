# GUI DIVERGENT THINKING CODE

# IMPORT LIBRARIES
import streamlit as st
import json
import pandas as pd
from XAI_APP_utils import generate_design_output

st.set_page_config(layout="wide")  # Set wide layout for the entire app

# API Keys Setup
if st.session_state.openai_key:
    try:
        from openai import OpenAI
        st.session_state.client = OpenAI(api_key=st.session_state.openai_key)  # Store client in session_state to be able to access it from other pages
    except Exception as e:
        st.error(f"Failed to initialize API: {e}")
else:
    st.error("Please provide your OpenAI API key.")

# DEFINE THE PAGE INITIAL INFORMATION

st.title("Divergent Thinking")

st.markdown("""
<div style="color: #1E90FF; font-size:16px;">
    <h5>Important: Workflow Disclaimer</h5>
    The <b>Divergent Thinking</b> page is where where you generate solutions for your design problem, so please make sure to define your problem in the <b>Main</b> page before proceeding, to do so write your query and press enter.<br>
    Once solutions are generated, you can proceed to the <b>Divergent Thinking Filtering</b> page to visualize, analyze, and select the most relevant options.<br>
    If no solutions have been generated in this page, the <b>Filtering</b> page will not work. Please ensure solutions exist before continuing.<br>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## How to Use:

1. **Select requirements**:
   - Select the requirements you wish to take into account for your design problem in addition to those already described in the initial problem.
   - You do not need to choose any if you do not want to.

2. **Generate solutions**:
   - Click on the "Generate New FBS Ontology Data" button to generate LLM solutions to your design problem.
   - Once the solutions have been generated, you will not be able to see them again in this page, but you can access them at any time from the **Filtering** page.

3. **Regenerate solutions**:
   - If the generated solutions do not convince you, you can regenerate new solutions by clicking on the "Reset" button at the bottom of the page.
   - **Note**: If you click on this button, the previously generated information will be lost.
   - Before regenerating solutions, note that in the **Convergent Thinking** page it will be possible to add data manually if you wish to do so.
""")


# MAIN CODE OF THE DIVERGENT THINKING PART, HERE NUMEROUS FBS SOLUTIONS ARE GENERATED FOR THE DEFINED DESIGN PROBLEM

# Check if the OpenAI client and design problem exist in session state
if "client" in st.session_state and "design_problem" in st.session_state:
    design_problem = st.session_state.design_problem
    role_description = st.session_state.role_description_divergent
    
    # Make the user select the requirements of the design problem to be used

    # Define available requirements
    available_requirements = [
        "Address buyer needs", "Innovation", "Ensure technical feasibility", 
        "Minimize cost", "Scalability", "Compliance with safety regulations", 
        "Compliance with energy regulations", "Sustainability", "Time efficiency"
    ]

    # Normal multiselect widget
    selected_requirements = st.multiselect(
        "Select the requirements for your design problem:",
        options=available_requirements,
        default=available_requirements,  # Start with all options selected to save time for those users who want them all
        help="By clicking each requirement you are selecting it as part of the prompt information for ChatGPT, make sure to only select those ones you want, it cannot be modified later unless you reset the data generation process.",
    )

    # Store the selected requirements in session state
    st.session_state.selected_requirements = selected_requirements

    # Display the selected requirements (optional, for user feedback)
    if st.session_state.selected_requirements:
        st.write(f"Selected Requirements: {', '.join(st.session_state.selected_requirements)}")
    else:
        st.warning("No requirements selected. Please choose at least one.")
    
    # Button to generate FBS data
    if st.button("Generate New FBS Ontology Data"):
        with st.spinner("Generating FBS ontology data..."):
            try:
                # Generate FBS elements for the single design problem
                fbs_entry = {
                    "Design Goal": design_problem,
                    "Requirements": selected_requirements,
                    "Functions_1": generate_design_output(design_problem, "functions", role_description, "Functions define the **purpose** of the design, describing **what it is for**.", "increase engine power output, improve fuel efficiency, reduce emissions..."),
                    "Behaviors_1": generate_design_output(design_problem, "behaviors", role_description, "Behaviors describe the **attributes** that can be derived from the design object’s structure, describing **what it does**.", "rotates at high speed using exhaust gases, compresses air to increase air mass flow, generates heat due to friction and pressure..."),
                    "Structures_1": generate_design_output(design_problem, "structures", role_description, "Structures define the **physical components, materials, or topology** that make up the design, describing **what it consists of**. They should be tangible elements, NOT descriptions of behavior.", "compressor, turbine, rotating shaft, steel housing, ball bearings, intercooler pipes..."),
                }
                
                # Save the entry to a JSON file
                file_name = "fbs_ontology_data.json"
                with open(file_name, "w") as file:
                    json.dump(fbs_entry, file, indent=4)

                # Display the generated FBS ontology data in a structured format
                st.success("FBS ontology data generation complete!")

                # Display the design problem and selected requirements
                st.markdown(f"### Design Problem:\n{fbs_entry['Design Goal']}")
                st.markdown("### Selected Requirements:")
                st.write(", ".join(fbs_entry["Requirements"]))

                # Create the FBS table and a brief explanation of its elements
                st.markdown("""
                            ### FBS Ontology Elements
                            The table below shows the proposed Functions, Behaviors, and Structures for your design problem. Each column represents a specific aspect of the FBS ontology:
                            - **Functions**: What the design is for (teleology).
                            - **Behaviors**: What the design does.
                            - **Structures**: What the design consists of (elements, topology, materials).
                            """)

                functions = fbs_entry["Functions_1"]
                behaviors = fbs_entry["Behaviors_1"]
                structures = fbs_entry["Structures_1"]

                # Display FBS elements as a table
                data = {
                    "Functions": functions,
                    "Behaviors": behaviors,
                    "Structures": structures,
                }

                # Ensure all columns have the same number of rows
                max_len = max(len(functions), len(behaviors), len(structures))
                functions += [""] * (max_len - len(functions))
                behaviors += [""] * (max_len - len(behaviors))
                structures += [""] * (max_len - len(structures))

                # Display the table
                fbs_table = pd.DataFrame(data)
                st.dataframe(fbs_table, height=400, use_container_width=True)

                # Store the table in session state to use in other pages
                st.session_state.fbs_table = fbs_table

                # Provide a download link for the JSON file
                with open(file_name, "r") as file:
                    json_data = file.read()
                st.download_button(
                    label="Download FBS Ontology Data as JSON",
                    data=json_data,
                    file_name=file_name,
                    mime="application/json",
                )

            except Exception as e:
                st.error(f"An error occurred during FBS ontology data generation: {e}")

    # Add a reset button outside the try-except block
    if st.button("Reset", help="Click here to reset the divergent thinking process and start fresh. Please take into account that if you click here all your data will be lost unless you download it."):
        for key in st.session_state.keys():
            del st.session_state[key]

else:
    st.error("Please provide your design problem and ensure the OpenAI client is initialized on the main page.")
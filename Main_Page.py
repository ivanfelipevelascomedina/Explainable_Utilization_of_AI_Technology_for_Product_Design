# GUI MAIN CODE

# IMPORT LIBRARIES
import streamlit as st

# DEFINE THE PAGES THAT THE GUI WILL HAVE
st.set_page_config(
    page_title="Homepage", # Set this page as the main page of the app
    layout="wide" # Set wide layout for the entire app
)

#DEFINE THE SIDEBAR INFORMATION

st.sidebar.success("Select the stage of the design process you want to work on.")

# API Keys Setup
# 1. Check if the key is already in session state and initialize it if it's not
if "openai_key" not in st.session_state:
    st.session_state.openai_key = ""  # Use a session_state to be able to access it from the other pages
# 2. API Key Input
openai_key = st.sidebar.text_input("OpenAI API Key", type="password", value=st.session_state.openai_key)
# 3. Update session state with the entered key
if openai_key:
    st.session_state.openai_key = openai_key
# 4. Initialize APIs if the key is provided in session state
if st.session_state.openai_key:
    try:
        from openai import OpenAI
        st.session_state.client = OpenAI(api_key=st.session_state.openai_key)  # Store client in session_state to be able to access it from other pages
        st.success("API initialized successfully!")
    except Exception as e:
        st.error(f"Failed to initialize API: {e}")
else:
    st.error("Please provide your OpenAI API key.")

# DEFINE THE PAGE INITIAL INFORMATION

st.title("Main Page")

st.markdown("""
<div style="color: #1E90FF; font-size:16px;">
    <h5>Important: Use of LLMs in the Design Process Disclaimer</h5>
    This design process incorporates the use of large language models (LLMs) to generate suggestions, calculations, and other outputs. While these models provide valuable assistance, the results are generated based on probabilistic algorithms and may not always be accurate, optimal, or complete. Users are advised to:
    <ol>
        <li><b>Review all Outputs:</b> Carefully evaluate all suggestions and calculations provided by the LLM.</li>
        <li><b>Exercise Professional Judgment:</b> Rely on personal expertise and domain knowledge to make final decisions.</li>
        <li><b>Verify Critical Data:</b> Independently validate any critical calculations or data before implementation.</li>
        <li><b>Acknowledge Limitations:</b> Understand that the LLM does not account for all possible variables, constraints, or nuances specific to the task.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## How to Use:

1. **Define a design problem**:
   - To start with the design process write your design problem and press enter.
   - Make sure that the small text at the right of the text panel that says "Press enter to apply" has disappeared, if not the change will not be effective.
   - If by mistake you did not write your design problem properly you can rewrite it by reloading the page. Make sure to do this, since the following pages depend on this value it cannot be modified later.

2. **Continue with the design process**:
   - After defining the design process move to the next pages.
   - If you want further information of the theoretical base of this app or how to use it, you can always click the **Information** page to get a detailed explanation.
            
""")

if "client" in st.session_state:
    # Store role descriptions in session state
    if "role_description_divergent" not in st.session_state:
        st.session_state.role_description_divergent = "You are an experienced designer that is able to propose numerous innovative design proposals for FBS ontology design problems."
    if "role_description_convergent" not in st.session_state:
        st.session_state.role_description_convergent = "You are a design expert able to classify design proposals as bad, poor, regular, good or excellent."
    # Get the design problem description and store it in session state only once, to avoid its value being modified if the user comes back to this page
    if "design_problem" not in st.session_state:
        # Ask for input only if not set
        input_value = st.text_input("Enter your design problem:")
        if input_value:  # Only set session state if the user provides input
            st.session_state.design_problem = input_value
    else:
        # Display the stored value without modification
        st.write(f"**Design problem**: {st.session_state.design_problem}")

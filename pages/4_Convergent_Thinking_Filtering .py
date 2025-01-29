# GUI FILTERING CODE

# IMPORT LIBRARIES
import streamlit as st
from XAI_APP_utils import answer_generation, extract_probs_information, substitute_tokens, calculate_prob_difference, visualize_scores, clean_tokens, calculate_stopping_condition, calculate_feature_importance
from transformers import RobertaTokenizer, RobertaForMaskedLM
from openai import OpenAI

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

st.title("Final Results")

st.markdown("""
<div style="color: #1E90FF; font-size:16px;">
    <h5>Important: Workflow Disclaimer</h5>
    The <b>Convergent Thinking Filtering</b> page is where you can understand how does the LLM rate each of your proposals and what is it taking into account to do so. After choosing the <b>Functions</b>, <b>Behaviors</b>, and <b>Structures</b> that you want to include in your final design, here you can undertand them better to make any necessary modifications.<br>        
    Ensure that the <b>Functions</b>, <b>Behaviors</b>, and <b>Structures</b> lists have been properly chosen in the <b>Convergent Thinking</b> page before proceeding. If these lists have not been chosen this page will not function as intended.<br>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## How to Use:

1. **View the LLM's opinion on one of the chosen options**:
   - To see how the LLM interprets your selected option, choose that option from the drop-down list below the table it belongs to.
   - Make sure you select only one option at a time (a function, a behaviour or a structure), if you choose more than one the result will not be displayed.
   - To display the results click on the ‘Display selection feature importance’ button at the bottom of the page. This may take a few minutes, so do not worry and wait for the result to load. Once calculated for the first time, the results will be automatically displayed the rest of the times you select this option. 
""")

# CHECK IF ROBERTA IS ALREADY LOADED IN THE SESSION STATE AND DO IT IN CASE IT IS NOT

if "roberta_tokenizer" not in st.session_state or "roberta_model" not in st.session_state:
    st.write("Loading RoBERTa model and tokenizer. This may take a few seconds...")
    # Load pre-trained RoBERTa model and tokenizer
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    model = RobertaForMaskedLM.from_pretrained('roberta-base')
    model.eval()  # Set the model to evaluation mode

    # Store the model and tokenizer in session state
    st.session_state["roberta_tokenizer"] = tokenizer
    st.session_state["roberta_model"] = model
    st.write("RoBERTa model and tokenizer loaded successfully!")
else:
    st.write("RoBERTa model and tokenizer already loaded.")
    tokenizer = st.session_state["roberta_tokenizer"]
    model = st.session_state["roberta_model"]

# LOAD THE CHOSEN DATA AND LET THE USERS CHOOSE FOR WHICH ONE THEY WANT TO SEE THE REAGENT FEATURE IMPORTANCE

# FUNCTIONS
# Check if the convergent thinking data exists in session state and load it in case it does not
if "convergent_thinking_functions_data" in st.session_state:
    # Access the stored DataFrame
    convergent_thinking_functions_data = st.session_state["convergent_thinking_functions_data"]
    
    # Filter rows where `is_widget` is True
    convergent_thinking_filtered_functions_data = convergent_thinking_functions_data[convergent_thinking_functions_data["Selection"] == True]
    
    # Display the filtered rows
    st.write("Selected Functions")
    st.write(convergent_thinking_filtered_functions_data)

    # Allow user to choose one of the selected rows
    if not convergent_thinking_filtered_functions_data.empty:
        convergent_thinking_filtered_functions_data_with_empty = [""] + convergent_thinking_filtered_functions_data["Option"].tolist()
        selected_function = st.selectbox(
            "Choose a function:",
            convergent_thinking_filtered_functions_data_with_empty
        )
        st.write(f"You selected: {selected_function}")
    else:
        st.write("No selected functions available.")

else:
    # Inform the user if the data is not available
    st.write("No data found. Please complete the convergent thinking table on the other page.")

# BEHAVIORS
# Check if the convergent thinking data exists in session state and load it in case it does not
if "convergent_thinking_behaviors_data" in st.session_state:
    # Access the stored DataFrame
    convergent_thinking_behaviors_data = st.session_state["convergent_thinking_behaviors_data"]
    
    # Filter rows where `is_widget` is True
    convergent_thinking_filtered_behaviors_data = convergent_thinking_behaviors_data[convergent_thinking_behaviors_data["Selection"] == True]
    
    # Display the filtered rows
    st.write("Selected Behaviors")
    st.write(convergent_thinking_filtered_behaviors_data)

    # Allow user to choose one of the selected rows
    if not convergent_thinking_behaviors_data.empty:
        convergent_thinking_filtered_behaviors_data_with_empty = [""] + convergent_thinking_filtered_behaviors_data["Option"].tolist()
        selected_behavior = st.selectbox(
            "Choose a behavior:",
            convergent_thinking_filtered_behaviors_data_with_empty
        )
        st.write(f"You selected: {selected_behavior}")
    else:
        st.write("No selected functions available.")

else:
    # Inform the user if the data is not available and load it in case it does not
    st.write("No data found. Please complete the convergent thinking behaviors table on the other page.")

# STRUCTURES
# Check if the convergent thinking data exists in session state
if "convergent_thinking_structures_data" in st.session_state:
    # Access the stored DataFrame
    convergent_thinking_structures_data = st.session_state["convergent_thinking_structures_data"]
    
    # Filter rows where `is_widget` is True
    convergent_thinking_filtered_structures_data = convergent_thinking_structures_data[convergent_thinking_structures_data["Selection"] == True]
    
    # Display the filtered rows
    st.write("Selected Structures")
    st.write(convergent_thinking_filtered_structures_data)

    # Allow user to choose one of the selected rows
    if not convergent_thinking_filtered_structures_data.empty:
        convergent_thinking_filtered_structures_data_with_empty = [""] + convergent_thinking_filtered_structures_data["Option"].tolist()
        selected_structure = st.selectbox(
            "Choose a structure:",
            convergent_thinking_filtered_structures_data_with_empty
        )
        st.write(f"You selected: {selected_structure}")
    else:
        st.write("No selected functions available.")

else:
    # Inform the user if the data is not available
    st.write("No data found. Please complete the convergent thinking structures table on the other page.")


# DISPLAY THE REAGENT FEATURE IMPORTANCE OF THE FINAL DATA TO ALLOW THE USERS UNDERSTAND WHAT IS THE LLM (CHAT GPT IN THIS CASE) TAKING INTO ACCOUNT TO GENERATE THOSE SOLUTIONS

# We define a condition to run the Reagent method only when one of the selections has been selected
selections = [selected_function, selected_behavior, selected_structure]
non_empty_selections = []
for s in selections:
    if s:
        non_empty_selections.append(s)

if st.button("Display selection feature importance"):
        
    if len(non_empty_selections) == 1:
        # Define the type of input
        selected_item = non_empty_selections[0]
        
        # Determine the type of selection
        if selected_item == selected_function:
            type_of_input = "functional"
            selected_item = selected_function
        elif selected_item == selected_behavior:
            type_of_input = "behavioral"
            selected_item = selected_behavior
        elif selected_item == selected_structure:
            type_of_input = "structural"
            selected_item = selected_structure

        role_description = st.session_state["role_description_convergent"]
        design_problem = st.session_state["design_problem"]
        original_input = f"In one word how good is {selected_item} as a {type_of_input} solution for {design_problem}?"

        # Generate unique keys for session state with the type of input and the selected item
        input_key = f"{type_of_input}_{selected_item}_original_input"
        tokens_key = f"{type_of_input}_{selected_item}_cleaned_tokens"
        scores_key = f"{type_of_input}_{selected_item}_token_scores_normalized"

        if input_key not in st.session_state or tokens_key not in st.session_state or scores_key not in st.session_state:
            # Calculate feature importance
            with st.spinner("Calculating feature importance, please wait..."):
                original_first_token, cleaned_tokens, token_scores_normalized = calculate_feature_importance(original_input, role_description, tokenizer, model)
            # Save to session state
            st.session_state[input_key] = original_first_token
            st.session_state[tokens_key] = cleaned_tokens
            st.session_state[scores_key] = token_scores_normalized

            st.write("Score: ", st.session_state[input_key])
            html_output = visualize_scores(st.session_state[tokens_key], st.session_state[scores_key])
            st.markdown(html_output, unsafe_allow_html=True)
        else:
            # Retrieve and display existing data
            st.write("Score: ", st.session_state[input_key])
            html_output = visualize_scores(st.session_state[tokens_key], st.session_state[scores_key])
            st.markdown(html_output, unsafe_allow_html=True)

    elif len(non_empty_selections) == 0:
            st.warning("Please select at least one option from the tables, either a function a behavior or a structure, if you do not choose any of them the results cannot be computed.")

    else:
        st.warning("Please select only one of the options from the tables, either a function a behavior or a structure, if you choose more the results cannot be computed.")
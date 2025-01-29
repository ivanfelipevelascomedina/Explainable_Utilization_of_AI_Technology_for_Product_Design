# GUI CONVERGENT THINKING CODE

# IMPORT LIBRARIES
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")  # Set wide layout for the entire app

# DEFINE THE PAGE INITIAL INFORMATION

st.title("Convergent Thinking")

st.markdown("""
<div style="color: #1E90FF; font-size:16px;">
    <h5>Important: Workflow Disclaimer</h5>
    The <b>Convergent Thinking</b> page is where you can refine and filter the generated solutions for your design problem. After checking the <b>Divergent Thinking Filtering</b> and analyzing each of the design solutions here you can select those that seem more interesting for you or even add new ones.<br>        
    Ensure that the <b>Functions</b>, <b>Behaviors</b>, and <b>Structures</b> lists are properly initialized in the <b>Divergent Thinking</b> page before proceeding. If these lists are not initialized in this page will not function as intended.<br>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## How to Use:

1. **Select options**:
   - To select the options you wish to include in your final design, click on the "Selection" box on the right-hand side of each option.

2. **Add new options**:
   - To add new rows to each table, click on the "Add a Row" button below each table.
   - If by mistake you add a row that you do not want to modify, do not worry. As long as the "Selection" box on the right-hand side of the row is unchecked, that row will have no effect on the final result.
   - To edit a row, either added or existing, click on it and write the content you wish to edit.

3. **Make the changes effective**:
   - To make the changes effective, click on the "Update Data" button at the bottom of the page; otherwise, the changes made will not be taken into account.
   - Remember that you can verify this by going to the Final Results tab and checking if the options shown correspond to what you have selected.
""")

# Step 1: Check if data exists in session state for functions, behaviors and structures
if "convergent_thinking_functions_data" in st.session_state:
    functions_data = st.session_state["convergent_thinking_functions_data"]
else:
    # Initialize from `functions_list` if available
    if "functions_list" in st.session_state:
        functions_data = pd.DataFrame({
            "Option": st.session_state["functions_list"],
            "Selection": [False] * len(st.session_state["functions_list"])  # Default widget values to False
        })
        # Save the initialized data to session state
        st.session_state["convergent_thinking_functions_data"] = functions_data
    else:
        st.error(f"The functions list is missing in session state. Please initialize it before proceeding.")

if "convergent_thinking_behaviors_data" in st.session_state:
    behaviors_data = st.session_state["convergent_thinking_behaviors_data"]
else:
    # Initialize from `functions_list` if available
    if "behaviors_list" in st.session_state:
        behaviors_data = pd.DataFrame({
            "Option": st.session_state["behaviors_list"],
            "Selection": [False] * len(st.session_state["behaviors_list"])  # Default widget values to False
        })
        # Save the initialized data to session state
        st.session_state["convergent_thinking_behaviors_data"] = behaviors_data
    else:
        st.error(f"The behaviors list is missing in session state. Please initialize it before proceeding.")

if "convergent_thinking_structures_data" in st.session_state:
    structures_data = st.session_state["convergent_thinking_structures_data"]
else:
    # Initialize from `functions_list` if available
    if "structures_list" in st.session_state:
        structures_data = pd.DataFrame({
            "Option": st.session_state["structures_list"],
            "Selection": [False] * len(st.session_state["structures_list"])  # Default widget values to False
        })
        # Save the initialized data to session state
        st.session_state["convergent_thinking_structures_data"] = structures_data
    else:
        st.error(f"The structures list is missing in session state. Please initialize it before proceeding.")

# Step 2: Display the DataFrame using st.data_editor for the functions, behaviors and structures and add a row with default `selection=False` in any of the chosen tables
# Step 2.1: Functions
st.write("Functions table")
edited_functions_data = st.data_editor(functions_data, num_rows="dynamic", use_container_width=True, key="functions_table_editor")
if st.button("Add a Row for Functions"):
    # Add a new row to the DataFrame
    new_functions_row = pd.DataFrame([{"Option": "", "Selection": False}])
    functions_data = pd.concat([edited_functions_data, new_functions_row])

    # Store the updated DataFrame in session state
    st.session_state["convergent_thinking_functions_data"] = functions_data
    st.write("The new functions row has been added")

# Step 2.2: Behaviors
st.write("Behaviors table")
edited_behaviors_data = st.data_editor(behaviors_data, num_rows="dynamic", use_container_width=True, key="behaviors_table_editor")
if st.button("Add a Row for Behaviors"):
    # Add a new row to the DataFrame
    new_behaviors_row = pd.DataFrame([{"Option": "", "Selection": False}])
    behaviors_data = pd.concat([edited_behaviors_data, new_behaviors_row])

    # Store the updated DataFrame in session state
    st.session_state["convergent_thinking_behaviors_data"] = behaviors_data
    st.write("The new behaviors row has been added")

# Step 2.3 Structures
st.write("Structures table")
edited_structures_data = st.data_editor(structures_data, num_rows="dynamic", use_container_width=True, key="structures_table_editor")
if st.button("Add a Row for Structures"):
    # Add a new row to the DataFrame
    new_structures_row = pd.DataFrame([{"Option": "", "Selection": False}])
    structures_data = pd.concat([edited_structures_data, new_structures_row])

    # Store the updated DataFrame in session state
    st.session_state["convergent_thinking_structures_data"] = structures_data
    st.write("The new structures row has been added")

# Step 3: Button to force display updated data
if st.button("Update Data"):
    # Store the updated DataFrame in session state for functions behaviors and structures
    st.session_state["convergent_thinking_functions_data"] = edited_functions_data
    st.session_state["convergent_thinking_behaviors_data"] = edited_behaviors_data
    st.session_state["convergent_thinking_structures_data"] = edited_structures_data
    st.write("The data has been updated")
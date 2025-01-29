# GUI FILTERING CODE

# IMPORT LIBRARIES
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from XAI_APP_utils import generate_embeddings, reduce_and_cluster, plot_interactive_clusters, rank_by_similarity, normalize_embeddings, enrich_with_wordnet

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

st.title("Filtering")

st.markdown("""
<div style="color: #1E90FF; font-size:16px;">
    <h5>Important: Workflow Disclaimer</h5>
    The <b>Divergent Thinking Filtering</b> page is where you can visualize, analyze, and select the most relevant options.<br>
    If no solutions have been generated on the <b>Divergent Thinking</b> page, this page will not work as intended.
    Please ensure solutions exist before proceeding.<br>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## How to Use:
            
1. **Generate visualization results**:       
   - The first time this page is opened you will have to wait a bit while the visualization results are being calculated, but for future iterations you will be able to directly access them.
            
2. **Select a visualization mode**:
   - Choose a visualization mode from the drop-down list.
   - Both, the vizualization and the explanation of what each mode consists of will be displayed after the selection. 

""")

# MAIN CODE OF THE FILTERING PART, HERE THE GPT-GENERATED FBS SOLUTIONS ARE VISUALIZED IN A 3D SPACE TO HELP THE DESIGNER UNDERSTAND THEM AND CHOOSE THE BEST ONES ACCORDING TO HIS OWN CRITERIA. HERE DESIGNERS ARE ALSO ALLOWED TO INCLUDE THEIR OWN FBS SOLUTIONS INTO THE DESIGN CYCLE
# Check if the OpenAI client, the design problem and the GPT-generated FBS solutions exist in session state
if "client" in st.session_state and "design_problem" in st.session_state and "fbs_table" in st.session_state and "selected_requirements" in st.session_state:

    # Retrieve the FBS data from session state and assure there are no empty entries (some could have been created during the data display in the divergent thinking)
    # Check if the lists are already calculated
    if (
        "functions_list" not in st.session_state or
        "behaviors_list" not in st.session_state or
        "structures_list" not in st.session_state
    ): 
        fbs_categories = ["Functions", "Behaviors", "Structures"]
        fbs_lists = {}

        for category in fbs_categories:
            # Clean the entries in each category, removing empty strings and non-strings
            fbs_lists[category] = [
                entry for entry in st.session_state.fbs_table[category]
                if isinstance(entry, str) and entry.strip()
            ]

        # Define the FBS lists
        functions_list = fbs_lists["Functions"]
        behaviors_list = fbs_lists["Behaviors"]
        structures_list = fbs_lists["Structures"]
        # Save cleaned lists in session state
        st.session_state["functions_list"] = functions_list
        st.session_state["behaviors_list"] = behaviors_list
        st.session_state["structures_list"] = structures_list
        # Define the FBS lists with WordNet enrichment
        #functions_list_enriched = enrich_with_wordnet(fbs_lists["Functions"])
        #behaviors_list_enriched = enrich_with_wordnet(fbs_lists["Behaviors"])
        #structures_list_enriched = enrich_with_wordnet(fbs_lists["Structures"])
        # Save enriched lists in session state
        #st.session_state["functions_list_enriched"] = functions_list_enriched
        #st.session_state["behaviors_list_enriched"] = behaviors_list_enriched
        #st.session_state["structures_list_enriched"] = structures_list_enriched

    # Check if embeddings and clustering results are already calculated
    if (
        "functions_embeddings" not in st.session_state or
        "behaviors_embeddings" not in st.session_state or
        "structures_embeddings" not in st.session_state or
        "functions_umap" not in st.session_state or
        "behaviors_umap" not in st.session_state or
        "structures_umap" not in st.session_state
    ):        
        # Generate embeddings
        st.write("Preparing functions visualization")
        functions_embeddings = generate_embeddings(functions_list)
        st.write("Preparing behaviors visualization")
        behaviors_embeddings = generate_embeddings(behaviors_list)
        st.write("Preparing structures visualization")
        structures_embeddings = generate_embeddings(structures_list)

        # Save embeddings in session state
        st.session_state["functions_embeddings"] = functions_embeddings
        st.session_state["behaviors_embeddings"] = behaviors_embeddings
        st.session_state["structures_embeddings"] = structures_embeddings

        # Dimensionality reduction and clustering
        functions_umap, functions_clusters, functions_silhouette, functions_ch = reduce_and_cluster(functions_embeddings)
        st.session_state["functions_umap"] = functions_umap
        st.session_state["functions_clusters"] = functions_clusters
        st.session_state["functions_silhouette"] = functions_silhouette
        st.session_state["functions_ch"] = functions_ch

        behaviors_umap, behaviors_clusters, behaviors_silhouette, behaviors_ch = reduce_and_cluster(behaviors_embeddings)
        st.session_state["behaviors_umap"] = behaviors_umap
        st.session_state["behaviors_clusters"] = behaviors_clusters
        st.session_state["behaviors_silhouette"] = behaviors_silhouette
        st.session_state["behaviors_ch"] = behaviors_ch

        structures_umap, structures_clusters, structures_silhouette, structures_ch = reduce_and_cluster(structures_embeddings)
        st.session_state["structures_umap"] = structures_umap
        st.session_state["structures_clusters"] = structures_clusters
        st.session_state["structures_silhouette"] = structures_silhouette
        st.session_state["structures_ch"] = structures_ch
    #else:
    #    st.write("Visualization preparation complete")

    # Give the user the option to select what kind of output to display to better understand the generated solutions
    # Initialize session state for the selectbox if not already set
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Display All the Solutions"  # Default value

    # Create a selectbox tied to session state using the `key` parameter
    st.selectbox(
        "Choose an option:",
        ["Display All the Solutions", "Solution Space Visualization", "Order Solutions by Similarity to the Design Problem", "Order Solutions by Similarity to a Given Requirement", "Display Each Solution's Most Similar Requirement"],
        key="selected_option",  # Automatically syncs with session_state
        help="Select an analysis or visualization option to explore the generated solutions."
    )

    if st.session_state.selected_option == "Display All the Solutions":
        # Visualize the generated data
        st.write("### Visualizing all the AI-generated solutions")

        with st.expander("What is Display All the Solutions?"):
            st.write("""
            This option allows you to revisualize all the AI-generated solutions in case you couldn't do it properly in the previous design step (Divergent Thinking).
            """)

        # Visualize all the solutions
        st.dataframe(st.session_state.fbs_table, height=400, use_container_width=True)

    elif st.session_state.selected_option == "Solution Space Visualization":
        # Visualize the embeddings
        st.write("### Visualizing the Solution Space")

        # Add a short explanation of the selected option
        with st.expander("What is Solution Space Visualization?"):
            st.write("""
            This option displays the generated FBS solutions (Functions, Behaviors, and Structures)
            in an interactive 2D space that shows how text solutions relate to each other. Each point represents a solution, 
            and the closer two points are, the more similar their ideas. Use this visualization to identify similar solutions, 
            spot unique ideas, and explore the variety of responses.
            """)

        # Display the embedding space for each of the FBS solution spaces
        fbs_categories = ["Functions", "Behaviors", "Structures"]
        for category in fbs_categories:
            # Retrieve data from session state
            umap_embeddings = st.session_state[f"{category.lower()}_umap"]
            clusters = st.session_state[f"{category.lower()}_clusters"]
            data_list = st.session_state[f"{category.lower()}_list"]  # Use cleaned list
            silhouette_score = st.session_state[f"{category.lower()}_silhouette"]
            ch_index = st.session_state[f"{category.lower()}_ch"]

            # Plot interactive clusters
            #st.write(f"#### {category} Space:")
            plot_interactive_clusters(
                umap_embeddings,
                clusters,
                data_list,
                f"{category} Space"
            )
            #st.write("Silhouette: ", silhouette_score)
            #st.write("CH: ", ch_index)

    elif st.session_state.selected_option == "Order Solutions by Similarity to the Design Problem":
        # Order solutions based on their similarity to the given design problem
        st.write("### Ranking Solutions by Similarity to the Design Problem")

        # Add a short explanation of the selected option
        with st.expander("What is Ranking by Similarity to the Design Problem?"):
            st.write("""
            This option ranks the solutions based on how well they align with the design problem. 
            The ranking uses the cosine similarity score to measure how closely each solution matches 
            the design goal, helping you quickly identify the most relevant ideas.
            """)

        # Generate embedding for the design problem
        design_problem_embedding = generate_embeddings([st.session_state.design_problem])[0]
        design_problem_embedding = normalize_embeddings([design_problem_embedding])[0]

        fbs_categories = ["Functions", "Behaviors", "Structures"]
        for category in fbs_categories:
            st.write(f"#### Ranking {category}:")
            embeddings = st.session_state[f"{category.lower()}_embeddings"]
            data_list = st.session_state[f"{category.lower()}_list"]  # Use cleaned list
            rank_by_similarity(design_problem_embedding, embeddings, data_list)
        
    elif st.session_state.selected_option == "Order Solutions by Similarity to a Given Requirement":
        # Order solutions based on their similarity with a chosen requirement
        st.write("### Ranking Solutions by Similarity to a Given Requirement")

        # Add a short explanation of the selected option
        with st.expander("What is Ranking by Similarity to a Given Requirement?"):
            st.write("""
            This option allows you to select a specific requirement and rank the FBS solutions based on
            their similarity to that requirement. It helps you understand how well solutions meet individual criteria.
            """)

        # Select a requirement
        selected_requirement = st.selectbox(
            "Select a Requirement:",
            st.session_state.selected_requirements
        )

        if selected_requirement:
            # Generate embedding for the selected requirement
            requirement_embedding = generate_embeddings([selected_requirement])[0]
            requirement_embedding = normalize_embeddings([requirement_embedding])[0]

            fbs_categories = ["Functions", "Behaviors", "Structures"]
            for category in fbs_categories:
                st.write(f"#### Ranking {category} for Requirement: {selected_requirement}")
                embeddings = st.session_state[f"{category.lower()}_embeddings"]
                data_list = st.session_state[f"{category.lower()}_list"]  # Use cleaned list
                rank_by_similarity(requirement_embedding, embeddings, data_list)

    elif st.session_state.selected_option == "Display Each Solution's Most Similar Requirement":
        # Display each solution's most similar requirement
        st.write("### Displaying Each Solution's Most Similar Requirement")

        # Add a short explanation of the selected option
        with st.expander("What is Displaying Each Solution's Most Similar Requirement?"):
            st.write("""
            This option matches each FBS solution to its most similar requirement using cosine similarity.
            It provides insights into how solutions align with the overall set of selected requirements.
            """)

        # Generate embeddings for all requirements
        requirement_embeddings = generate_embeddings(st.session_state.selected_requirements)
        requirement_embeddings = normalize_embeddings(requirement_embeddings)

        fbs_categories = ["Functions", "Behaviors", "Structures"]
        for category in fbs_categories:
            st.write(f"#### Most Similar Requirements for {category}:")
            embeddings = st.session_state[f"{category.lower()}_embeddings"]
            data_list = st.session_state[f"{category.lower()}_list"]  # Use cleaned list

            most_similar_requirements = []
            for i, solution_embedding in enumerate(embeddings):
                similarities = cosine_similarity([solution_embedding], requirement_embeddings)[0]
                most_similar_index = similarities.argmax()
                most_similar_requirement = st.session_state.selected_requirements[most_similar_index]
                most_similar_requirements.append((data_list[i], most_similar_requirement, similarities[most_similar_index]))

            # Display the table
            df = pd.DataFrame(most_similar_requirements, columns=["Solution", "Most Similar Requirement", "Similarity"])
            st.dataframe(df, use_container_width=True)
        
        else:
            st.write("Choose the option you want for visualization")


    # Add a reset button outside the try-except block
    if st.button("Reset", help="Click here to reset the filtering process and start fresh. Please take into account that if you click here all your data will be lost."):
        for key in st.session_state.keys():
            del st.session_state[key]

else:
    st.error("Please provide your design problem and ensure the OpenAI client is initialized on the main page.")
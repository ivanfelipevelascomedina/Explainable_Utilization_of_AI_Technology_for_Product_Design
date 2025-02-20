# GUI FILTERING CODE

# IMPORT LIBRARIES
import streamlit as st

st.set_page_config(layout="wide")  # Set wide layout for the entire app

# DEFINE THE PAGE INITIAL INFORMATION

st.title("Information Page")

# Give user's information on how to use the APP
# Introduction
st.write("""
Designing requires both creativity and precision. This app will guide you through the process, 
helping you generate innovative ideas and refine them into effective solutions. To make the most of this tool, 
it is essential to understand two key concepts: **Divergent and Convergent Thinking** and the **Function–Behavior–Structure (FBS) Ontology**.
""")

# Divergent and Convergent Thinking
st.header("Divergent and Convergent Thinking")
st.write("""
The design process alternates between two modes of thinking:

- **Divergent Thinking**: here is where the designer generates a wide range of ideas 
  without limitations, fostering creativity and innovation.
- **Convergent Thinking**: here is where the designer focuses on refining and evaluating those ideas to identify the most viable and effective solutions.

Think of the design process as a cyclical journey. Each iteration involves a combination of divergent thinking and convergent thinking, where you start by dreaming big (divergent thinking) and then choose the best outcomes (convergent thinking). By repeating this type of iteration for a number of times, you can move from the initial problem to its final solution.
""")

# Example: Chair Design
st.subheader("Example: Designing a Chair")
st.write("""
Imagine designing a chair:
- **Divergent Thinking**: You might brainstorm dozens of ideas, such as chairs made of recycled materials, 
  inflatable chairs or even chairs with built-in massagers.
- **Convergent Thinking**: From these ideas, you evaluate which options are feasible, cost-effective 
  and functional, narrowing down to the best design.
""")

# Add an explainatory image
st.image("images/Convergent_and_Divergent_Thinking.png", caption="Divergent and Convergent thinking for a chair design", use_container_width=True)

# FBS Ontology
st.header("The Function–Behavior–Structure (FBS) Ontology")
st.write("""
Design can also be understood through the **Function–Behavior–Structure (FBS)** framework, which breaks down a design into three layers:

- **Function**: What is the design meant to achieve? (Its purpose or teleology)
- **Behavior**: How does the design do? (Its actions or effects)
- **Structure**: What does the design consist of? (Its components and their relationships)

A typical design often includes multiple functions, with each of them supported by several behaviors, and many structural components working together. The FBS framework simplifies this complexity by breaking designs into manageable parts, making it easier to analyze, refine and improve them.
""")

# Example: Chair Design
st.subheader("Example: Designing a Chair")
st.write("""
Imagine designing a chair:
- **Function**: A chair's function is to provide seating.
- **Behavior**: The chair supports a person’s weight and provides comfort.
- **Structure**: The chair consists of legs, a seat, and a backrest made of materials like wood, metal, or fabric.         
""")

# Add an explainatory image
st.image("images\Simplified_function_behavior_structure.png", caption="Jiao, J., Pang, S., Chu, J., Jing, Y., and Zhao, T., 2021, An Improved FFIP Method Based on Mathematical Logic and SysML, Applied Sciences, 11(8), p. 3534. [Online]. Available: http://dx.doi.org/10.3390/app11083534.", width=400)

# How the App Helps
st.header("How This App Works")
st.write("""
This application focuses on the early stages of the design process, where the focus is on exploring a wide range of ideas and identifying the most promising ones. The app supports this process by generating the Function-Behaviour-Structure (FBS) ontology all at once, allowing you to see multiple possibilities for functions, behaviours and structures from the outset. Using divergent thinking, you can explore creative solutions, and with convergent thinking, you can evaluate and choose the best options.
While iterative refinement is often important in later stages of design, we are currently focusing on creativity and decision making from the outset, providing a solid foundation for future iterations if necessary and creating an approach that is ideal for brainstorming and conceptual design, where exploration is key. 

The process to be followed is as follows:

1. **Main page**: define the design problem you are going to work with and press enter.  
2. **Divergent Thinking page**: choose the extra requirements you consider appropriate for your design problem and generate the FBS ontology according to them. It is important to emphasise that, since the fundamental requirements have already been defined in the initial design problem, it is not necessary to select any further requirements if the designer does not want to. The selection or not of extra requirements is left to the designer's choice. 
3. **Divergent Thinking Filtering page**: visualise how the LLM establishes the different relationships between all solutions, with respect to the defined design problem and with respect to the chosen requirements in order to assess which may be more useful.  
4. **Convergent Thinking page**: choose those solutions that you consider most appropriate according to the information seen in the Filtering page and add others manually if you wish to do so. It is recommended to choose a maximum of 5-7 solutions for each element of the FBS ontology.  
5. **Convergent Thinking Filtering Results page**: visualise how the LLM evaluates each of your alternatives and what it takes into account to determine how good are your final design proposals for the given problem.  
""")

# Add an explainatory image
st.image("images\Design_process_workflow.png", caption="Workflow Overview", use_container_width=True)

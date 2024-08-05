import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

def generate_gpt_response(prompt):
    try:
        llm = ChatOpenAI(model='gpt-4', temperature=0.7)
        
        prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template="{prompt}"
        )
        
        chain = LLMChain(llm=llm, prompt=prompt_template)
        
        response = chain.run(prompt=prompt)
        return response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

def main():
    load_dotenv()
    st.set_page_config(page_title="Add Context Component Prompt", page_icon="🤖")

    st.title("Add Context Component Prompt")

    # Introduction section with red and bold formatting
    st.markdown("""
    <style>
    .red-bold {
        color: red;
        font-weight: bold;
    }
    </style>
    <p><span class="red-bold">[ Context ]:</span> Marketing manager at a software company with a new product.</p>
    <p><span class="red-bold">[ Task ]:</span> Introduce the product to clients and offer a discount.</p>
    """, unsafe_allow_html=True)

    # Initialize session state for the prompt if it doesn't exist
    if 'prompt' not in st.session_state:
        st.session_state.prompt = """
[ Context ]: Marketing manager at a software company with a new product.
[ Task ]: Introduce the product to clients and offer a discount.

Write an email to potential clients introducing our new software product and offering a special discount for early adopters.
"""

    # Text area for the prompt with pre-filled text
    prompt = st.text_area("Customize your prompt if needed:", 
                          value=st.session_state.prompt,
                          height=200)

    # Update session state when the prompt changes
    if prompt != st.session_state.prompt:
        st.session_state.prompt = prompt

    # Custom CSS for the red button with white text
    st.markdown("""
        <style>
        .stButton > button {
            color: white;
            background-color: red;
            border-color: red;
        }
        .stButton > button:hover {
            color: white;
            background-color: darkred;
            border-color: darkred;
        }
        </style>
    """, unsafe_allow_html=True)

    # Run button
    if st.button("Generate Email"):
        if st.session_state.prompt:
            with st.spinner("Generating email..."):
                response = generate_gpt_response(st.session_state.prompt)
                if response:
                    st.subheader("Generated Email:")
                    st.write(response)
        else:
            st.warning("Please enter a prompt before generating the email.")

if __name__ == '__main__':
    main()
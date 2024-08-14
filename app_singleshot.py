import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

def generate_gpt_response(prompt):
    try:
        llm = ChatOpenAI(model='gpt-4o', temperature=0.7)
        
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
    st.set_page_config(page_title="Demo", page_icon="🤖",layout="wide")
    if 'prompt' not in st.session_state:
        st.session_state.prompt = """Schreiben Sie eine kurze E-Mail.
"""

    # Text area for the prompt with pre-filled text
    prompt = st.text_area("Bitte klicken Sie Los", 
                          value=st.session_state.prompt,
                          height=100)

    # Update session state when the prompt changes
    if prompt != st.session_state.prompt:
        st.session_state.prompt = prompt

    # Custom CSS for the red button with white text
    st.markdown("""
        <style>
        .reportview-container .main .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
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
    if st.button("Los"):
        if st.session_state.prompt:
            with st.spinner("Antwort wird generiert...."):
                response = generate_gpt_response(st.session_state.prompt)
                if response:
                    st.write(response)
        else:
            st.warning("Please enter a prompt before running.")

if __name__ == '__main__':
    main()
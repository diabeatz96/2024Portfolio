import streamlit as st
import streamlit_lottie as st_lottie
import streamlit_timeline as timeline
import openai
from dotenv import load_dotenv
import os



def main():
    load_dotenv()
    
    st.set_page_config(page_title="Adam Kostandy's Portfolio", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")
    open_api_key = openai.OpenAI(api_key=os.getenv("API_KEY"))

    st.title("Adam Kostandy's Portfolio")
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = open_api_key.chat.completions.create(
                model = st.session_state.openai_model,
                messages = [ 
                        {
                            "role": m["role"],
                            "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                stream = True
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})    

    
if __name__ == "__main__":
    main()
    
    



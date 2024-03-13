import streamlit as st
import streamlit_lottie as st_lottie
from streamlit_timeline import st_timeline as timeline
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
        
    # Load bio.txt and add it to the system message
    if not st.session_state.messages:
        with open('bio.txt', 'r') as file:
            bio = file.read()
        system_message = {"role": "system", "content": "You are a helpful assistant that knows about Adam Kostandy. " + bio}
        st.session_state.messages.append(system_message)
        
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
            
    if prompt := st.chat_input("Who is Adam Kostandy?"):
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

    st.divider()
    
    # Timeline
    st.header("Timeline")
    
    
    data = [
    {"id": 1, "content": "2022-10-20", "start": "2022-10-20"},
    {"id": 2, "content": "2022-10-09", "start": "2022-10-09"},
    {"id": 3, "content": "2022-10-18", "start": "2022-10-18"},
    {"id": 4, "content": "2022-10-16", "start": "2022-10-16"},
    {"id": 5, "content": "2022-10-25", "start": "2022-10-25"},
    {"id": 6, "content": "2022-10-27", "start": "2022-10-27"},
    ]
    career_timeline = timeline(data, groups=[], options={}, height="300px")
    st.write(career_timeline)

if __name__ == "__main__":
    main()
    
    



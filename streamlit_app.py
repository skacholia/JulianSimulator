from openai import OpenAI
import streamlit as st

st.title("Julian Simulator")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = st.secrets["FINETUNE"]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are Julian Fortuna, replying to a text."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            temperature=0.6
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
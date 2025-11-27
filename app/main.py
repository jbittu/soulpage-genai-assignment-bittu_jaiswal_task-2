import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.agent import build_agent
from app.memory_store import load_memory, save_memory
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Conversational Knowledge Bot", layout="wide")
st.title("Conversational Knowledge Bot")

if "agent" not in st.session_state:
    st.session_state.agent = build_agent(verbose=False)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_memory()


def extract_output(result):
    # Case 1: dict with "output"
    if isinstance(result, dict) and "output" in result:
        return result["output"]

    # Case 2: dict with "result"
    if isinstance(result, dict) and "result" in result:
        return result["result"]

    # Case 3: dict with any text-like field
    if isinstance(result, dict):
        for key in ["answer", "text", "message"]:
            if key in result:
                return result[key]

    # Case 4: if it's a string
    if isinstance(result, str):
        return result

    return str(result)


with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    try:
        raw = st.session_state.agent.invoke({"input": user_input})
        response = extract_output(raw)

    except Exception as e:
        response = f"Error from agent: {e}"

    st.session_state.chat_history.append({"role": "assistant", "content": response})
    save_memory(st.session_state.chat_history)


for msg in st.session_state.chat_history:
    if msg.get("role") == "user":
        st.markdown(f"**You:** {msg.get('content')}")
    else:
        st.markdown(f"**Bot:** {msg.get('content')}")

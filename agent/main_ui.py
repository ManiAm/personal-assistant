
# invoke with: python3 -m streamlit run main_ui.py

import asyncio
import streamlit as st
from langchain_core.messages import AIMessage
from agent_setup import build_agent

st.set_page_config(page_title="Personal Agent", layout="wide")
st.title("Personal Assitant")
st.markdown("Chat with your AI personal assistant for real-time answers (stocks, news, weather, and web search).")

if "agent" not in st.session_state:
    st.session_state.agent = asyncio.run(build_agent())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your question:", placeholder="e.g. What is ticker symbol for Microsoft?")
submit = st.button("Submit")

if submit and user_input.strip():

    with st.spinner("Thinking..."):

        async def _run():
            return await st.session_state.agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={"recursion_limit": 10}
            )

        response = asyncio.run(_run())

        messages = response["messages"]

        # For debugging
        # for m in messages:
        #     print(f"[{m.__class__.__name__}] {m.content}")
        #     if hasattr(m, 'tool_calls'):
        #         print(f"Tool Calls: {m.tool_calls}")
        #     if hasattr(m, 'additional_kwargs'):
        #         print(f"Additional: {m.additional_kwargs}")

        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                content = msg.content.strip()
                if content:
                    st.session_state.chat_history.append((user_input, content))
                    break

if st.session_state.chat_history:

    st.markdown("## Chat History")

    for question, answer in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {question}")
        st.markdown(f"**Agent:** {answer}")

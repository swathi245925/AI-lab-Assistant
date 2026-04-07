import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
import os

# 🔑 Get API KEY securely (NO hardcoding)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key not found! Please set GROQ_API_KEY in environment variables.")
    st.stop()

# ✅ LLM Model

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=api_key   
)

# 🧮 Calculator tool
def calculator_tool(query):
    try:
        return str(eval(query))
    except:
        return "Error in calculation"

tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for math calculations"
    )
]

# 🤖 Agent
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=False,
    max_iterations=3
)

# -------- STREAMLIT UI --------
st.title("🤖 AI Lab Assistant")
st.write("Ask anything (DSA, AI, coding, math...)")

# Chat memory
if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:")

if st.button("Ask"):
    if user_input:

        # ✅ Smart math handling
        if any(op in user_input for op in ["+", "-", "*", "/"]):
            try:
                answer = str(eval(user_input))
            except:
                answer = "Invalid calculation"
        else:
            try:
                response = agent.invoke({"input": user_input})
                answer = response.get("output", str(response))
            except Exception as e:
                answer = f"Error: {str(e)}"

        # Save chat
        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("AI", answer))

# Display chat
for role, msg in st.session_state.chat:
    if role == "You":
        st.write(f"🧑 You: {msg}")
    else:
        st.write(f"🤖 AI: {msg}")
import os
import warnings
import logging

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

# 🔕 Remove warnings & debug logs
warnings.filterwarnings("ignore")
logging.getLogger("langchain").setLevel(logging.ERROR)

# 🔑 Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key not found! Set GROQ_API_KEY in terminal.")

# ✅ LLM
llm = ChatGroq(
    temperature=0,
    model="llama-3.1-8b-instant",
    groq_api_key=api_key
)

# 🧮 Calculator tool
def calculator_tool(query):
    try:
        return str(eval(query))
    except:
        return "Invalid calculation"

tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for math calculations"
    )
]

# 🧠 Memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 🤖 Agent (UPDATED)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="conversational-react-description",
    memory=memory,
    verbose=False,
    handle_parsing_errors=True   # ✅ added
)

print("🤖 AI Lab Assistant Ready! (type 'exit' to quit)")

# 🔁 Chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    try:
        response = agent.invoke({
            "input": user_input
        })
        print("AI:", response["output"])
    except Exception as e:
        print("Error:", str(e))
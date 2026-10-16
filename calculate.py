# i am adding some valuable things now
import os
import streamlit as st
from google import genai

st.set_page_config(page_title="OmniAssist AI", page_icon="⚡", layout="wide")

# API Setup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

client = genai.Client(api_key=api_key) if api_key else None

# Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- CORNER / SIDEBAR GENAI ASSISTANT ---
with st.sidebar:
    st.header("💬 Corner GenAI Assistant")
    st.caption("Ask questions, clarify bills, or brainstorm anytime.")
    
    chat_container = st.container(height=320)
    for msg in st.session_state.chat_history:
        chat_container.chat_message(msg["role"]).write(msg["text"])

    user_query = st.chat_input("Ask assistant anything...")
    if user_query:
        if not client:
            st.error("Please supply a Gemini API Key first.")
        else:
            st.session_state.chat_history.append({"role": "user", "text": user_query})
            with chat_container.chat_message("user"):
                st.write(user_query)

            bot_prompt = f"""
            You are a sharp, helpful assistant inside OmniAssist AI.
            Answer briefly, clearly, and concisely:
            User: {user_query}
            """
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=bot_prompt
            )
            bot_reply = res.text
            st.session_state.chat_history.append({"role": "assistant", "text": bot_reply})
            with chat_container.chat_message("assistant"):
                st.write(bot_reply)

# --- MAIN WORKSPACE ---
st.title("⚡ OmniAssist AI")
st.caption("Dual-Utility Workspace: Smart Shopkeeper Khata & Student Study Synthesizer")

tab_shop, tab_student = st.tabs(["🛒 Shopkeeper Expense & Bill Organizer", "📝 Student SmartNote Synthesizer"])

# 1. SHOPKEEPER BILL & EXPENSE CALCULATOR
with tab_shop:
    st.subheader("Messy List to Itemized Khata / Invoice")
    default_shop_text = "5 kg sugar 220\n2 packets refined oil 260\n10 bread packets 400\n1 kg tea powder 340"
    shop_input = st.text_area("Messy Bill / Inventory Log:", value=default_shop_text, height=130)

    if st.button("Calculate & Organize Bill", use_container_width=True):
        if not client:
            st.error("Please provide an API key in the sidebar.")
        elif not shop_input.strip():
            st.warning("Please enter some items.")
        else:
            with st.spinner("AI parsing items and calculating totals..."):
                shop_prompt = f"""
                You are a smart merchant billing & ledger assistant.
                Extract all items, quantities, and their total cost from this messy entry:
                \"\"\"{shop_input}\"\"\"

                Output format:
                1. Clean Markdown Table with columns: | Item | Quantity | Subtotal (INR) |
                2. Calculate the Final Total Bill amount.
                3. A brief 1-sentence cashflow tip.
                """
                shop_res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=shop_prompt
                )
                st.markdown(shop_res.text)

# 2. STUDENT SMARTNOTE ORGANIZER
with tab_student:
    st.subheader("Lecture Notes to Study Kit")
    default_student_text = (
        "In C, pointers hold memory addresses. malloc() allocates raw memory from heap, "
        "calloc() allocates and initializes to zero, and free() prevents memory leaks. "
        "Dangling pointers occur when memory is freed but the pointer is not set to NULL. "
        "Segmentation fault happens if you access memory not assigned to your process."
    )
    
    student_notes = st.text_area(
        "Paste messy lecture transcript, slides, or lab notes:",
        value=default_student_text,
        height=140
    )

    mode = st.radio(
        "Conversion Mode:",
        ["Executive Summary & Key Points", "Formulas & Code Cheatsheet", "Active Recall Viva Quiz"],
        horizontal=True
    )

    if st.button("Synthesize Study Kit", use_container_width=True):
        if not client:
            st.error("Please provide an API key in the sidebar.")
        elif not student_notes.strip():
            st.warning("Please paste some notes.")
        else:
            with st.spinner("AI restructuring academic material..."):
                student_prompt = f"""
                You are an expert academic tutor.
                Convert the following raw content into {mode}:
                \"\"\"{student_notes}\"\"\"

                Rules:
                - Keep it structured, clear, and high-yield.
                - If Quiz: provide 3 multiple choice or viva questions and hide answers at the bottom.
                """
                student_res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=student_prompt
                )
                st.markdown(student_res.text)


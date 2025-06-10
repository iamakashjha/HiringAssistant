"""
Main Streamlit application for the TalentScout Hiring Assistant.
"""

import streamlit as st
from chatbot import HiringAssistant
from utils import save_conversation

# Set page config
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.assistant {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = HiringAssistant()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    if "last_input" not in st.session_state:
        st.session_state.last_input = None

def display_chat_message(role: str, content: str):
    """Display a chat message with custom styling."""
    with st.container():
        st.markdown(f"""
            <div class="chat-message {role}">
                <div>{content}</div>
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.title("🤖 TalentScout Hiring Assistant")
    st.markdown("Welcome to the TalentScout Hiring Assistant! I'll help you through the initial screening process.")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This chatbot will:
        1. Collect your basic information
        2. Ask about your technical skills
        3. Assess your technical knowledge
        4. Guide you through the screening process
        """)
        
        if st.button("Start New Conversation"):
            st.session_state.messages = []
            st.session_state.chatbot = HiringAssistant()
            st.session_state.conversation_started = False
            st.session_state.last_input = None
            st.rerun()
    
    # Main chat interface
    if not st.session_state.conversation_started:
        initial_message = st.session_state.chatbot.get_initial_greeting()
        st.session_state.messages.append({"role": "assistant", "content": initial_message})
        st.session_state.conversation_started = True
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])
    
    # Chat input
    user_input = st.text_input("Your response:", key="user_input")
    
    # Process input only if it's new and not empty
    if user_input and user_input != st.session_state.last_input:
        # Update last input
        st.session_state.last_input = user_input
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        display_chat_message("user", user_input)
        
        # Get chatbot response
        response = st.session_state.chatbot.process_message(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        display_chat_message("assistant", response)

if __name__ == "__main__":
    main() 
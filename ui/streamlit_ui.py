import streamlit as st
import requests
import json
import sseclient

# Set page config
st.set_page_config(page_title="LangGraph Chat", page_icon="💬", layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main chat interface
st.title("Chat with LangGraph")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "human", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        try:
            content = ''
            # Use a stream request to get SSE events
            response = requests.post("http://localhost:8000/generate", 
                                     json={"messages": st.session_state.messages}, 
                                     headers={"Content-Type": "application/json"}, 
                                     stream=True)

            # Create SSE client
            client = sseclient.SSEClient(response)

            placeholder = st.empty()
            for event in client.events():
                data = json.loads(event.data)
                if data.get('type', 'agent') == 'agent':
                    content += data.get("content", "")
                    placeholder.markdown(content)

            # Save the complete response to chat history
            st.session_state.messages.append(
                {"role": "ai", "content": content}
            )

        except Exception as e:
            st.error(f"Error connecting to server: {str(e)}")

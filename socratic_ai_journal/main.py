import streamlit as st
import time

# Local Imports
from src.database import init_db, save_entry, fetch_history, save_chat_message, fetch_chat_history, fetch_previous_entries, delete_chat_history, fetch_entry, delete_entry
from src.audio import transcribe_audio
from src.sentiment import analyze_sentiment
from src.llm import stream_chat_response
from src.ui.visuals import render_sentiment_chart, render_chat_sentiment_trajectory
from src.config import SOCRATIC_SYSTEM_PROMPT

# Page Configuration
st.set_page_config(
    page_title="Local Socratic Journal",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Infrastructure
init_db()

# Session State Initialization
if "active_entry_id" not in st.session_state:
    st.session_state.active_entry_id = None
if "transcription_buffer" not in st.session_state:
    st.session_state.transcription_buffer = ""
if "audio_key_counter" not in st.session_state:
    st.session_state.audio_key_counter = 0
if "chat_audio_counter" not in st.session_state:
    st.session_state.chat_audio_counter = 0
if "selected_entries" not in st.session_state:
    st.session_state.selected_entries = set()

def main():
    st.title("🦉 Socratic AI Journal")
    st.markdown("*A Local-First Cognitive Augmentation System*")
    st.divider()

    # --- Sidebar: Historical Data ---
    with st.sidebar:
        st.header("Journal History")
        
        # New Chat Button
        if st.button("🆕 New Chat", type="primary", help="Start a new journal entry and conversation"):
            st.session_state.active_entry_id = None
            st.session_state.transcription_buffer = ""
            st.rerun()
        
        st.divider()
        
        # Reload Trajectory Button
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            if st.button("🔄 Reload Trajectory", help="Refresh the emotional trajectory chart", use_container_width=True):
                st.rerun()
        
        st.divider()
        
        # Always fetch fresh history (no caching)
        history = fetch_history()
        
        # Visualization
        if history:
            fig = render_sentiment_chart(history)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
        st.divider()
        
        # History List
        if history:
            st.subheader("Select & Delete")
            
            # Toggle all checkbox
            select_all = st.checkbox("Select All Entries", key="select_all_checkbox")
            
            # If select all is toggled, update selected entries
            if select_all:
                st.session_state.selected_entries = set(e['id'] for e in history)
            
            col1, col2 = st.columns([0.7, 0.3])
            with col2:
                # Delete selected button
                if st.button("🗑️ Delete Selected", type="secondary", use_container_width=True):
                    if st.session_state.selected_entries:
                        num_to_delete = len(st.session_state.selected_entries)
                        for entry_id in list(st.session_state.selected_entries):
                            delete_entry(entry_id)
                            if st.session_state.active_entry_id == entry_id:
                                st.session_state.active_entry_id = None
                        st.success(f"✓ Deleted {num_to_delete} entry/entries!")
                        st.session_state.selected_entries = set()
                        st.rerun()
                    else:
                        st.warning("No entries selected for deletion")
            
            st.divider()
            
            # Entry list with checkboxes
            for entry in history:
                col1, col2 = st.columns([0.12, 0.88])
                
                with col1:
                    # Checkbox for each entry
                    is_selected = st.checkbox(
                        "Delete",
                        value=entry['id'] in st.session_state.selected_entries,
                        key=f"select_{entry['id']}",
                        label_visibility="collapsed"
                    )
                    
                    # Update selection set
                    if is_selected:
                        st.session_state.selected_entries.add(entry['id'])
                    else:
                        st.session_state.selected_entries.discard(entry['id'])
                
                with col2:
                    date_str = entry['timestamp'][:16].replace('T', ' ')
                    label = entry['sentiment_label']
                    icon = "🟢" if label == "Positive" else "🔴" if label == "Negative" else "⚪"
                    
                    with st.expander(f"{icon} {date_str} - Score: {entry['sentiment_score']:.2f}"):
                        st.write(entry['content'][:150] + ("..." if len(entry['content']) > 150 else ""))
                        if st.button("Load Chat", key=f"btn_{entry['id']}", use_container_width=True):
                            st.session_state.active_entry_id = entry['id']
                            st.session_state.transcription_buffer = entry['content']
                            st.rerun()
        else:
            st.info("No entries yet. Create your first journal entry!")

    # --- Main Area: Dynamic Content ---
    if st.session_state.active_entry_id:
        # Show Chat Interface
        chat_interface(st.session_state.active_entry_id)
        
        # New Entry Button
        st.divider()
        if st.button("➕ Start New Entry", help="Create a new journal entry"):
            st.session_state.active_entry_id = None
            st.session_state.transcription_buffer = ""
            st.rerun()
    else:
        # Show Entry Creation Interface
        create_new_entry()

@st.fragment
def create_new_entry():
    """Fragment for creating new journal entries."""
    st.subheader("Deep Reflection")
    
    # 1. Audio Recording Widget
    audio_input = st.audio_input("Record Voice Note", key=f"audio_entry_{st.session_state.audio_key_counter}")
    
    if audio_input:
        try:
            # Transcribe only if we have new audio
            with st.spinner("Transcribing..."):
                text = transcribe_audio(audio_input)
                st.session_state.transcription_buffer = text
                st.success("Audio processed.")
                st.session_state.audio_key_counter += 1  # Increment to refresh widget
                st.rerun()  # Refresh to reset audio input widget
        except Exception as e:
            st.error(f"Audio processing failed: {str(e)}")
            st.session_state.audio_key_counter += 1
            st.rerun()

    # 2. Text Editor (Manual or Transcribed)
    entry_content = st.text_area(
        "Your Thoughts:",
        value=st.session_state.transcription_buffer,
        height=200,
        placeholder="Speak or type your thoughts here..."
    )

    # Memory Option
    use_memory = st.checkbox("Include memory from previous entries", value=True, 
                            help="When enabled, the AI will have context from your past reflections for more personalized questioning.")

    # 3. Save & Analyze Action
    if st.button("Commit Entry", type="primary"):
        if entry_content.strip():
            # Analyze
            sent_data = analyze_sentiment(entry_content)
            
            # Save Entry
            entry_id = save_entry(
                entry_content, 
                sent_data['score'], 
                sent_data['label'],
                1 if use_memory else 0
            )
            
            # Update State
            st.session_state.active_entry_id = entry_id
            st.session_state.transcription_buffer = entry_content
            
            # Save initial user message to chat log
            save_chat_message(entry_id, "user", entry_content)
            
            st.toast(f"Entry Saved! Sentiment: {sent_data['label']}")
            st.rerun()  # This will refresh entire page including sidebar trajectory
        else:
            st.warning("Journal entry cannot be empty.")

@st.fragment
def chat_interface(entry_id):
    """
    Renders the chat interface independently.
    Using @st.fragment prevents the whole page (and audio widget) from reloading
    during the chat loop.
    """
    st.subheader("Socratic Dialogue")
    
    # Get entry details
    entry = fetch_entry(entry_id)
    if not entry:
        st.error("Entry not found.")
        return
    
    # Top controls: Delete Chat and Reload Trajectory
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    with col2:
        if st.button("🗑️ Delete", key=f"delete_{entry_id}", help="Delete all chat messages", use_container_width=True):
            delete_chat_history(entry_id)
            st.success("Chat deleted!")
            st.rerun()
    with col3:
        if st.button("🔄 Reload", key=f"reload_{entry_id}", help="Reload the trajectory", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Load Chat History from DB
    db_messages = fetch_chat_history(entry_id)
    
    # Show Chat Emotional Trajectory
    if db_messages:
        trajectory_fig = render_chat_sentiment_trajectory(db_messages, entry['sentiment_score'])
        if trajectory_fig:
            st.plotly_chart(trajectory_fig, use_container_width=True)
        st.divider()
    
    # Display Chat History
    for msg in db_messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['message'])

    # Check if we need to trigger an AI response (if last message was user)
    last_role = db_messages[-1]['role'] if db_messages else None
    
    if last_role == 'user':
        with st.chat_message("assistant"):
            # Prepare context for LLM
            # We convert DB format to Ollama format
            llm_messages = [{"role": m["role"], "content": m["message"]} for m in db_messages]
            
            # Add previous entries context for the first AI response if memory enabled
            if len(db_messages) == 1 and entry['use_memory']:  # Only the initial entry message and memory enabled
                previous_entries = fetch_previous_entries(entry_id, limit=3)
                if previous_entries:
                    context = "For context, here are your previous reflections:\n\n"
                    for prev_entry in reversed(previous_entries):  # Show oldest first
                        date = prev_entry['timestamp'][:10]
                        content_snippet = prev_entry['content'][:150] + "..." if len(prev_entry['content']) > 150 else prev_entry['content']
                        context += f"• {date}: {content_snippet} (Sentiment: {prev_entry['sentiment_label']})\n\n"
                    context += "Use this context to provide continuity in your Socratic questioning.\n\n"
                    # Add current entry's emotional state
                    context += f"Current entry emotional state: {entry['sentiment_label']} (score: {entry['sentiment_score']:.2f})\n\n"
                    llm_messages.insert(0, {"role": "system", "content": context + SOCRATIC_SYSTEM_PROMPT})
                else:
                    # Add current entry's emotional state even without previous
                    context = f"Current entry emotional state: {entry['sentiment_label']} (score: {entry['sentiment_score']:.2f})\n\n"
                    llm_messages.insert(0, {"role": "system", "content": context + SOCRATIC_SYSTEM_PROMPT})
            elif len(db_messages) == 1:
                # No memory, but still add current emotional state
                context = f"Current entry emotional state: {entry['sentiment_label']} (score: {entry['sentiment_score']:.2f})\n\n"
                llm_messages.insert(0, {"role": "system", "content": context + SOCRATIC_SYSTEM_PROMPT})
            
            # Stream Response
            response_generator = stream_chat_response(llm_messages)
            full_response = st.write_stream(response_generator)
            
            # Save generated response to DB
            save_chat_message(entry_id, "assistant", full_response)
            
            # Rerun fragment to update state
            st.rerun()

    # Voice Response Input (available even during AI response)
    audio_response = st.audio_input("Voice Response", key=f"audio_resp_{entry_id}_{st.session_state.chat_audio_counter}")
    if audio_response:
        try:
            with st.spinner("Transcribing voice response..."):
                text = transcribe_audio(audio_response)
            if text.strip():
                save_chat_message(entry_id, "user", text)
                st.session_state.chat_audio_counter += 1
                st.rerun()
            else:
                st.session_state.chat_audio_counter += 1
                st.rerun()  # Refresh even if no text
        except Exception as e:
            st.error(f"Voice response processing failed: {str(e)}")
            st.session_state.chat_audio_counter += 1
            st.rerun()

    # Chat Input
    # Note: Streamlit fragments allow independent interaction here
    if prompt := st.chat_input("Respond to the inquiry..."):
        # Save user message
        save_chat_message(entry_id, "user", prompt)
        st.rerun()

if __name__ == "__main__":
    main()
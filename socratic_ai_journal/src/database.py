import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
from src.config import DB_PATH, DATA_DIR

def init_db():
    """Initializes the database schema and enables WAL mode."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # check_same_thread=False is required for Streamlit, but we manage locks via WAL
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    # Enable Write-Ahead Logging for concurrency 
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Create Entries Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            content TEXT NOT NULL,
            sentiment_score REAL,
            sentiment_label TEXT,
            use_memory INTEGER DEFAULT 1
        )
    ''')
    
    # Create Chat Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY(entry_id) REFERENCES entries(id)
        )
    ''')
    
    # Add use_memory column if it doesn't exist (for migration)
    try:
        cursor.execute("ALTER TABLE entries ADD COLUMN use_memory INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """Yields a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def save_entry(content: str, sentiment_score: float, sentiment_label: str, use_memory: int = 1) -> int:
    """Saves a journal entry and returns its ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO entries (timestamp, content, sentiment_score, sentiment_label, use_memory) VALUES (?,?,?,?,?)",
            (timestamp, content, sentiment_score, sentiment_label, use_memory)
        )
        conn.commit()
        return cursor.lastrowid

def save_chat_message(entry_id: int, role: str, message: str):
    """Logs a chat message for a specific entry."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_logs (entry_id, role, message) VALUES (?,?,?)",
            (entry_id, role, message)
        )
        conn.commit()

def fetch_history():
    """Retrieves all entries sorted by date."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries ORDER BY timestamp DESC")
        return [dict(row) for row in cursor.fetchall()]

def fetch_entry(entry_id: int):
    """Retrieves a specific entry by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries WHERE id = ?", (entry_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def fetch_chat_history(entry_id: int):
    """Retrieves chat logs for a specific entry."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, role, message FROM chat_logs WHERE entry_id = ? ORDER BY id ASC", 
            (entry_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def fetch_previous_entries(current_entry_id: int, limit: int = 3):
    """Retrieves previous entries for context, excluding the current one."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, timestamp, content, sentiment_label, use_memory FROM entries WHERE id < ? ORDER BY timestamp DESC LIMIT ?",
            (current_entry_id, limit)
        )
        return [dict(row) for row in cursor.fetchall()]

def delete_chat_history(entry_id: int):
    """Deletes all chat messages for a specific entry."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_logs WHERE entry_id = ?", (entry_id,))
        conn.commit()

def delete_entry(entry_id: int):
    """Deletes a journal entry and all its associated chat messages."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Delete chat logs first (due to foreign key constraint)
        cursor.execute("DELETE FROM chat_logs WHERE entry_id = ?", (entry_id,))
        # Then delete the entry
        cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        conn.commit()
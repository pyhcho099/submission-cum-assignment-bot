import sqlite3
import os
from datetime import datetime

def init_db():
    conn = sqlite3.connect('data/tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT NOT NULL,
            chapter TEXT NOT NULL,
            stage TEXT NOT NULL,
            assigned_to TEXT,
            status TEXT DEFAULT 'Waiting',
            progress TEXT,
            deadline DATE,
            notes TEXT,
            created_at DATE DEFAULT CURRENT_TIMESTAMP,
            updated_at DATE DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('data/tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

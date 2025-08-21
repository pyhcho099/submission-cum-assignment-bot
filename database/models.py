# database/models.py
import sqlite3
import re
from datetime import datetime, timedelta
import pytz
from config import Config

class Database:
    def __init__(self, db_path="staff_bot.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize()

    def _initialize(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute('PRAGMA foreign_keys = ON')
        cursor = self.conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT NOT NULL,
            chapter TEXT NOT NULL,
            stage TEXT NOT NULL CHECK(stage IN ('CTL', 'JTL', 'KTL', 'PR', 'CLRD', 'TS', 'QC', 'Release')),
            assigned_to TEXT,
            status TEXT NOT NULL CHECK(status IN ('Waiting', 'InProgress', 'Done', 'Blocked')),
            progress TEXT,
            deadline DATETIME,
            notes TEXT CHECK(length(notes) <= 500),
            source_channel TEXT,
            file_url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            timezone TEXT NOT NULL DEFAULT 'UTC',
            reminder_pref TEXT NOT NULL DEFAULT 'morning',
            onboarded BOOLEAN NOT NULL DEFAULT 0,
            last_active DATETIME
        )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_project_chapter ON tasks (project, chapter)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assigned ON tasks (assigned_to)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_project_status ON tasks (project, status)')

        self.conn.commit()

    def _validate_progress(self, progress_str):
        """Helper to validate progress string format."""
        return bool(re.match(r'^\d+/\d+$', progress_str))

    def add_task(self, project, chapter, stage, assigned_to=None, status="Waiting",
                 progress=None, deadline=None, notes=None, source_channel=None, file_url=None):
        """Add a new task"""
        if progress and not self._validate_progress(progress):
            raise ValueError("Invalid progress format. Expected 'done/total' (e.g., '3/10').")
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO tasks (
            project, chapter, stage, assigned_to, status, progress,
            deadline, notes, source_channel, file_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project, chapter, stage, assigned_to, status, progress,
              deadline, notes, source_channel, file_url))
        self.conn.commit()
        return cursor.lastrowid

    def update_task(self, task_id, **kwargs):
        """Update task fields"""
        if 'progress' in kwargs and kwargs['progress'] and not self._validate_progress(kwargs['progress']):
            raise ValueError("Invalid progress format. Expected 'done/total' (e.g., '3/10').")

        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [task_id]

        cursor = self.conn.cursor()
        cursor.execute(f'''
        UPDATE tasks SET {set_clause}, updated_at = CURRENT_TIMESTAMP
        WHERE task_id = ?
        ''', values)
        self.conn.commit()
        return cursor.rowcount > 0

    def get_task(self, task_id=None, project=None, chapter=None, stage=None):
        """Get task(s) by criteria"""
        cursor = self.conn.cursor()
        conditions, params = [], []

        if task_id is not None:
            conditions.append("task_id = ?")
            params.append(task_id)
        if project:
            conditions.append("project = ?")
            params.append(project)
        if chapter:
            conditions.append("chapter = ?")
            params.append(chapter)
        if stage:
            conditions.append("stage = ?")
            params.append(stage)

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        cursor.execute(f'''
        SELECT task_id, project, chapter, stage, assigned_to, status, progress,
               deadline, notes, source_channel, file_url, created_at, updated_at
        FROM tasks
        {where_clause}
        ''', params)

        rows = cursor.fetchall()
        if not rows:
            return None
        return [self._row_to_task_dict(row) for row in rows] if len(rows) > 1 else self._row_to_task_dict(rows[0])

    def get_user_tasks(self, user_id, project=None):
        """Get all tasks for a user"""
        cursor = self.conn.cursor()
        conditions, params = ["assigned_to = ?"], [user_id]
        if project:
            conditions.append("project = ?")
            params.append(project)

        where_clause = "WHERE " + " AND ".join(conditions)
        cursor.execute(f'''
        SELECT task_id, project, chapter, stage, assigned_to, status, progress,
               deadline, notes, source_channel, file_url, created_at, updated_at
        FROM tasks
        {where_clause}
        ORDER BY created_at DESC
        ''', params)

        rows = cursor.fetchall()
        return [self._row_to_task_dict(row) for row in rows]

    def get_idle_tasks(self, stage, threshold_hours):
        """Get tasks that are InProgress and haven't been updated in threshold_hours."""
        cursor = self.conn.cursor()
        # Calculate the cutoff datetime in Python for SQLite compatibility
        cutoff_time = datetime.utcnow() - timedelta(hours=threshold_hours)
        cutoff_time_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            SELECT * FROM tasks
            WHERE stage = ? AND status = 'InProgress'
            AND updated_at < ?
        ''', (stage, cutoff_time_str))

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def get_user(self, user_id):
        """Get user profile"""
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT user_id, timezone, reminder_pref, onboarded, last_active
        FROM users
        WHERE user_id = ?
        ''', (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "user_id": row[0], "timezone": row[1], "reminder_pref": row[2],
            "onboarded": bool(row[3]), "last_active": row[4]
        }

    def update_user(self, user_id, **kwargs):
        """Update user profile"""
        if not self.get_user(user_id):
            self.conn.execute('''
            INSERT INTO users (user_id, timezone, reminder_pref, onboarded)
            VALUES (?, ?, ?, ?)
            ''', (user_id, "UTC", "morning", False))

        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]

        cursor = self.conn.cursor()
        cursor.execute(f'''
        UPDATE users SET {set_clause}
        WHERE user_id = ?
        ''', values)
        self.conn.commit()
        return cursor.rowcount > 0

    def _row_to_task_dict(self, row):
        """Convert row to dict"""
        return {
            "task_id": row[0], "project": row[1], "chapter": row[2], "stage": row[3],
            "assigned_to": row[4], "status": row[5], "progress": row[6], "deadline": row[7],
            "notes": row[8], "source_channel": row[9], "file_url": row[10],
            "created_at": row[11], "updated_at": row[12]
        }

    def close(self):
        if self.conn:
            self.conn.close()

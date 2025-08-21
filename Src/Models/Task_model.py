from database import get_db_connection

class Task:
    def __init__(self, task_id=None, project=None, chapter=None, stage=None, 
                 assigned_to=None, status='Waiting', progress=None, 
                 deadline=None, notes=None):
        self.task_id = task_id
        self.project = project
        self.chapter = chapter
        self.stage = stage
        self.assigned_to = assigned_to
        self.status = status
        self.progress = progress
        self.deadline = deadline
        self.notes = notes

    @staticmethod
    def create(project, chapter, stage, assigned_to=None, deadline=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (project, chapter, stage, assigned_to, deadline)
            VALUES (?, ?, ?, ?, ?)
        ''', (project, chapter, stage, assigned_to, deadline))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return Task.get_by_id(task_id)

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE task_id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Task(**dict(row))
        return None

    @staticmethod
    def get_by_project_chapter_stage(project, chapter, stage):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE project = ? AND chapter = ? AND stage = ?
        ''', (project, chapter, stage))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Task(**dict(row))
        return None

    @staticmethod
    def get_user_tasks(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE assigned_to = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Task(**dict(row)) for row in rows]

    @staticmethod
    def get_all_projects():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT project FROM tasks')
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]

    def update_status(self, status):
        self.status = status
        self._update_field('status', status)

    def update_progress(self, progress):
        self.progress = progress
        self._update_field('progress', progress)

    def assign_to(self, user_id):
        self.assigned_to = user_id
        self._update_field('assigned_to', user_id)

    def _update_field(self, field, value):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            UPDATE tasks 
            SET {field} = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE task_id = ?
        ''', (value, self.task_id))
        
        conn.commit()
        conn.close()

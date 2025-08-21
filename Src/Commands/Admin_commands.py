import discord
from discord.ext import commands
import csv
import io
from models.task_model import Task

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="assign", description="Assign a task to a user")
    @commands.has_role("Admin")  # Replace with your admin role name
    async def assign(self, ctx, task_id: int, user: discord.Member):
        task = Task.get_by_id(task_id)
        
        if not task:
            await ctx.respond("Task not found.")
            return
        
        task.assign_to(str(user.id))
        task.update_status('In Progress')
        
        await ctx.respond(f"Task {task_id} assigned to {user.mention}")

    @commands.slash_command(name="release", description="Mark a project chapter as released")
    @commands.has_role("Admin")
    async def release(self, ctx, project: str, chapter: str):
        # Create release task if it doesn't exist
        task = Task.get_by_project_chapter_stage(project, chapter, 'Release')
        
        if not task:
            task = Task.create(project, chapter, 'Release')
        
        task.update_status('Done')
        await ctx.respond(f"{project} Chapter {chapter} marked as released!")

    @commands.slash_command(name="export", description="Export tasks to CSV")
    @commands.has_role("Admin")
    async def export(self, ctx):
        import sqlite3
        
        conn = sqlite3.connect('data/tasks.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        conn.close()
        
        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(column_names)
        writer.writerows(rows)
        
        # Send as file
        output.seek(0)
        file = discord.File(io.BytesIO(output.getvalue().encode()), filename="tasks.csv")
        await ctx.respond("Here's the task database:", file=file)

def setup(bot):
    bot.add_cog(AdminCommands(bot))

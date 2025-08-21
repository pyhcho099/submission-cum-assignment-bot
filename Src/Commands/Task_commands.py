import discord
from discord.ext import commands
from models.task_model import Task
from utils.embed_utils import create_task_embed

class TaskCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="claim", description="Claim a task")
    async def claim(self, ctx, project: str, chapter: str, stage: str):
        stage = stage.upper()
        valid_stages = ['TL', 'CL', 'TS', 'QC']
        
        if stage not in valid_stages:
            await ctx.respond("Invalid stage. Valid stages: TL, CL, TS, QC")
            return

        task = Task.get_by_project_chapter_stage(project, chapter, stage)
        
        if task:
            if task.assigned_to:
                await ctx.respond(f"This task is already assigned to <@{task.assigned_to}>")
                return
            else:
                task.assign_to(str(ctx.author.id))
                task.update_status('In Progress')
        else:
            task = Task.create(project, chapter, stage, str(ctx.author.id))
            task.update_status('In Progress')
        
        embed = create_task_embed(task)
        await ctx.respond(f"Task claimed!", embed=embed)

    @commands.slash_command(name="submit", description="Submit a completed task")
    async def submit(self, ctx, project: str, chapter: str, stage: str):
        stage = stage.upper()
        task = Task.get_by_project_chapter_stage(project, chapter, stage)
        
        if not task:
            await ctx.respond("Task not found. Please claim it first.")
            return
        
        if task.assigned_to != str(ctx.author.id):
            await ctx.respond("You are not assigned to this task.")
            return
        
        task.update_status('Done')
        
        embed = create_task_embed(task)
        await ctx.respond(f"Task submitted!", embed=embed)

    @commands.slash_command(name="tasks", description="Show your assigned tasks")
    async def tasks(self, ctx, user: discord.Member = None):
        target_user = user or ctx.author
        user_tasks = Task.get_user_tasks(str(target_user.id))
        
        if not user_tasks:
            await ctx.respond(f"No tasks found for {target_user.mention}")
            return
        
        embeds = [create_task_embed(task) for task in user_tasks]
        
        for embed in embeds:
            await ctx.send(embed=embed)
        
        await ctx.respond(f"Showing {len(embeds)} tasks for {target_user.mention}")

    @commands.slash_command(name="status", description="Show task status")
    async def status(self, ctx, project: str, chapter: str):
        tasks = []
        stages = ['TL', 'CL', 'TS', 'QC', 'Release']
        
        for stage in stages:
            task = Task.get_by_project_chapter_stage(project, chapter, stage)
            if task:
                tasks.append(task)
        
        if not tasks:
            await ctx.respond("No tasks found for this project/chapter.")
            return
        
        for task in tasks:
            embed = create_task_embed(task)
            await ctx.send(embed=embed)
        
        await ctx.respond(f"Showing status for {project} Chapter {chapter}")

def setup(bot):
    bot.add_cog(TaskCommands(bot))

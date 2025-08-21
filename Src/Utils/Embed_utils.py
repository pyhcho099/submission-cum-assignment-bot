import discord
from datetime import datetime

def create_task_embed(task):
    embed = discord.Embed(
        title=f"[{task.stage}] {task.project} - Chapter {task.chapter}",
        color=get_stage_color(task.stage)
    )
    
    embed.add_field(name="Status", value=task.status, inline=True)
    
    if task.progress:
        embed.add_field(name="Progress", value=task.progress, inline=True)
    
    if task.assigned_to:
        embed.add_field(name="Assigned To", value=f"<@{task.assigned_to}>", inline=True)
    
    if task.deadline:
        embed.add_field(name="Deadline", value=task.deadline, inline=True)
    
    embed.add_field(name="Task ID", value=task.task_id, inline=True)
    
    return embed

def get_stage_color(stage):
    colors = {
        'TL': 0x3498db,  # Blue
        'CL': 0xe67e22,  # Orange
        'TS': 0x9b59b6,  # Purple
        'QC': 0xf1c40f,  # Yellow
        'Release': 0x2ecc71  # Green
    }
    return colors.get(stage, 0x95a5a6)

def create_progress_bar(current, total):
    if total == 0:
        return "⬜⬜⬜⬜⬜"
    
    progress = current / total
    filled = int(progress * 5)
    empty = 5 - filled
    
    return "🟩" * filled + "⬜" * empty

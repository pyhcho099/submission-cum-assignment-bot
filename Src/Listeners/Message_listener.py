import re
import discord
from models.task_model import Task
from utils.embed_utils import create_task_embed

async def handle_message(bot, message):
    # Only listen to assignment and submission channels
    if message.channel.id not in [bot.config.ASSIGNMENTS_CHANNEL, bot.config.SUBMISSION_CHANNEL]:
        return

    content = message.content.lower()
    
    # Claim pattern: "claim chapter 5 tl project fire train"
    claim_match = re.search(r'claim\s+chapter\s+(\S+)\s+(\w+)\s+project\s+(.+)', content)
    if claim_match and message.channel.id == bot.config.ASSIGNMENTS_CHANNEL:
        chapter = claim_match.group(1)
        stage = claim_match.group(2).upper()
        project = claim_match.group(3).title()
        
        await handle_claim(bot, message, project, chapter, stage)
        return

    # Submit pattern: "submit chapter 5 ts project fire train"
    submit_match = re.search(r'submit\s+chapter\s+(\S+)\s+(\w+)\s+project\s+(.+)', content)
    if submit_match and message.channel.id == bot.config.SUBMISSION_CHANNEL:
        chapter = submit_match.group(1)
        stage = submit_match.group(2).upper()
        project = submit_match.group(3).title()
        
        await handle_submit(bot, message, project, chapter, stage)
        return

async def handle_claim(bot, message, project, chapter, stage):
    # Check if valid stage
    valid_stages = ['TL', 'CL', 'TS', 'QC']
    if stage not in valid_stages:
        await message.reply("Invalid stage. Valid stages: TL, CL, TS, QC")
        return

    # Check if task already exists
    task = Task.get_by_project_chapter_stage(project, chapter, stage)
    
    if task:
        if task.assigned_to:
            await message.reply(f"This task is already assigned to <@{task.assigned_to}>")
            return
        else:
            # Assign existing task
            task.assign_to(str(message.author.id))
            task.update_status('In Progress')
            
            embed = create_task_embed(task)
            await message.reply(f"Task claimed!", embed=embed)
            
            # Auto-ping next role if needed
            await ping_next_role(bot, task)
    else:
        # Create new task
        task = Task.create(project, chapter, stage, str(message.author.id))
        task.update_status('In Progress')
        
        embed = create_task_embed(task)
        await message.reply(f"New task created and claimed!", embed=embed)

async def handle_submit(bot, message, project, chapter, stage):
    task = Task.get_by_project_chapter_stage(project, chapter, stage)
    
    if not task:
        await message.reply("Task not found. Please claim it first.")
        return
    
    if task.assigned_to != str(message.author.id):
        await message.reply("You are not assigned to this task.")
        return
    
    # Update task status
    task.update_status('Done')
    
    embed = create_task_embed(task)
    await message.reply(f"Task submitted!", embed=embed)
    
    # Auto-ping next role
    await ping_next_role(bot, task)

async def ping_next_role(bot, task):
    guild = bot.get_guild(bot.config.GUILD_ID)
    
    if task.stage == 'CL':
        role = guild.get_role(bot.config.TS_ROLE)
        channel = bot.get_channel(bot.config.SUBMISSION_CHANNEL)
        await channel.send(f"{role.mention} Cleaning for {task.project} Chapter {task.chapter} is done!")
    
    elif task.stage == 'TS':
        role = guild.get_role(bot.config.QC_ROLE)
        channel = bot.get_channel(bot.config.SUBMISSION_CHANNEL)
        await channel.send(f"{role.mention} Typesetting for {task.project} Chapter {task.chapter} is done!")
    
    elif task.stage == 'QC':
        role = guild.get_role(bot.config.ADMIN_ROLE)
        channel = bot.get_channel(bot.config.SUBMISSION_CHANNEL)
        await channel.send(f"{role.mention} QC for {task.project} Chapter {task.chapter} is done!")

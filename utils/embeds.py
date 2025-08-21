# utils/embeds.py
import discord
from datetime import datetime
from utils.parsers import format_deadline_display

def create_task_embed(task, user_timezone="UTC"):
    """Create rich embed for task"""
    status_emojis = {"Waiting": "🔴", "InProgress": "🟡", "Done": "✅", "Blocked": "⚠️"}
    stage_emojis = {
        "CTL": "🇨🇳", "JTL": "🇯🇵", "KTL": "🇰🇷",
        "PR": "📝", "CLRD": "🧹", "TS": "✒️", "QC": "🔍"
    }

    embed = discord.Embed(
        title=f"{stage_emojis.get(task['stage'], '❓')} [{task['stage']}] {task['project']} - {task['chapter']}",
        color=discord.Color.blue() if task['status'] != 'Done' else discord.Color.green()
    )

    status_line = f"{status_emojis.get(task['status'], '❓')} {task['status']}"
    if task['progress']:
        status_line += f" | Progress: {task['progress']}"

    embed.add_field(name="Status", value=status_line, inline=False)
    embed.add_field(name="Assigned", value=f"<@{task['assigned_to']}>" if task['assigned_to'] else "Unassigned", inline=True)

    deadline_display = format_deadline_display(task['deadline'], user_timezone)
    embed.add_field(name="Soft Target", value=deadline_display, inline=True)

    if task['progress']:
        try:
            done, total = map(int, task['progress'].split("/"))
            if total > 0:
                percent = int((done / total) * 100)
                bar_length = 10
                filled_length = int(bar_length * done // total)
                progress_bar = "⬛" * filled_length + "⬜" * (bar_length - filled_length)
                embed.add_field(name="Progress", value=f"{progress_bar} ({percent}%)", inline=False)
        except (ValueError, ZeroDivisionError):
            pass # Silently ignore malformed progress

    if task['notes']:
        notes = task['notes'][:40] + "..." if len(task['notes']) > 40 else task['notes']
        embed.add_field(name="Notes", value=notes, inline=False)

    if user_timezone == "UTC":
        embed.set_footer(text="💡 Use /profile to set your timezone for local times.")

    return embed

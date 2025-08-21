# cogs/notifications.py
import discord
from discord.ext import tasks, commands
from datetime import datetime
import pytz
from database.models import Database
from config import Config
from utils.embeds import create_task_embed

class NotificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.config = Config
        self.check_idle_tasks.start()

    def cog_unload(self):
        self.check_idle_tasks.cancel()

    @tasks.loop(hours=1) # Check every hour for idle tasks
    async def check_idle_tasks(self):
        now = datetime.utcnow()
        task_board = self.bot.get_channel(self.config.TASK_BOARD_CHANNEL)
        if not task_board:
            print(f"Warning: TASK_BOARD_CHANNEL {self.config.TASK_BOARD_CHANNEL} not found.")
            return

        for stage, hours in self.config.IDLE_THRESHOLDS.items():
            idle_tasks = self.db.get_idle_tasks(stage, hours)

            for task in idle_tasks:
                assigned_user_id = task["assigned_to"]
                if assigned_user_id:
                    try:
                        # Create a simple alert embed
                        embed = discord.Embed(
                            title="⚠️ Idle Task Alert",
                            description=f"**{task['project']} {task['chapter']} - {task['stage']}** has been inactive for over {hours} hours.",
                            color=discord.Color.orange()
                        )
                        embed.add_field(name="Assigned To", value=f"<@{assigned_user_id}>", inline=True)
                        embed.add_field(name="Last Updated", value=task['updated_at'], inline=True)

                        # Try to DM the user
                        user = self.bot.get_user(int(assigned_user_id))
                        if user:
                            try:
                                dm_embed = discord.Embed(
                                    title="⚠️ Your Task is Idle",
                                    description=f"Your task **{task['project']} {task['chapter']} - {task['stage']}** has not been updated in over {hours} hours.",
                                    color=discord.Color.orange()
                                )
                                dm_embed.add_field(name="Task Board", value=f"<#{self.config.TASK_BOARD_CHANNEL}>", inline=False)
                                await user.send(embed=dm_embed)
                            except discord.Forbidden:
                                pass # User has DMs disabled

                        # Send alert to task board
                        await task_board.send(content=f"<@{assigned_user_id}>", embed=embed, allowed_mentions=discord.AllowedMentions(users=True))
                    except Exception as e:
                        print(f"Error sending idle alert for task {task['task_id']}: {e}")

    @check_idle_tasks.before_loop
    async def before_check_idle_tasks(self):
        await self.bot.wait_until_ready()
        print("Idle task checker started.")

async def setup(bot):
    await bot.add_cog(NotificationCog(bot))

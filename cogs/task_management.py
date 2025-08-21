# cogs/task_management.py
import discord
from discord import app_commands
from discord.ext import commands
import re
from datetime import datetime
from database.models import Database
from utils.parsers import parse_submission, parse_assignment
from utils.embeds import create_task_embed
from config import Config

class TaskManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.config = Config

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id == self.config.ASSIGNMENTS_CHANNEL:
            await self.process_assignment(message)
        elif message.channel.id == self.config.SUBMISSION_CHANNEL:
            await self.process_submission(message)

    async def process_assignment(self, message):
        result, error = parse_assignment(message)
        if error:
            await message.reply(error)
            return

        user_id = result["user_id"]
        project = result["project"]
        chapter = result["chapter"]
        channel_id = result["channel_id"]
        stage = result["stage"]

        existing_task = self.db.get_task(project=project, chapter=chapter, stage=stage)
        if existing_task:
            self.db.update_task(existing_task["task_id"], assigned_to=user_id, status="InProgress", source_channel=channel_id)
            action = "updated"
        else:
            self.db.add_task(project=project, chapter=chapter, stage=stage, assigned_to=user_id, status="InProgress", source_channel=channel_id)
            action = "created"

        log_channel = self.bot.get_channel(self.config.LOGS_CHANNEL)
        if log_channel:
            await log_channel.send(
                f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] "
                f"<@{message.author.id}> {action} assignment: {project} {chapter} - {stage} → <@{user_id}>"
            )

        confirmation = (
            f"✅ **Assignment {action}**\n"
            f"{project} {chapter} - {stage} → <@{user_id}>\n"
            f"Work channel: <#{channel_id}>"
        )
        await message.reply(confirmation)

        try:
            user = await self.bot.fetch_user(int(user_id))
            user_data = self.db.get_user(user_id)
            user_tz = user_data["timezone"] if user_data else "UTC"

            dm_message = (
                f"📌 You've been assigned **{project} {chapter} - {stage}**\n"
                f"Work here: <#{channel_id}>\n"
                f"Please begin when ready."
            )
            await user.send(dm_message)
        except Exception as e:
            print(f"Could not DM user {user_id}: {e}")
            # Optionally, log to #logs if DM fails

    async def process_submission(self, message):
        result, error = parse_submission(message)
        if error:
            await message.reply(error)
            return

        project = result["project"]
        chapter = result["chapter"]
        file_url = result["file_url"]
        stage = result["stage"]

        task = self.db.get_task(project=project, chapter=chapter, stage=stage)
        if not task:
            await message.reply(f"❌ No active task found for {project} {chapter} - {stage}")
            return

        if str(message.author.id) != task["assigned_to"]:
            await message.reply(f"❌ You're not assigned to this task.")
            return

        self.db.update_task(task["task_id"], status="Done", file_url=file_url, progress="100/100")

        log_channel = self.bot.get_channel(self.config.LOGS_CHANNEL)
        if log_channel:
            await log_channel.send(
                f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] "
                f"<@{message.author.id}> submitted: {project} {chapter} - {stage}"
            )

        confirmation = (
            f"✅ **Submission Recorded**\n"
            f"{project} {chapter} - {stage}\n"
            f"File: [Link]({file_url})"
        )
        await message.reply(confirmation)

        next_stage = None
        if stage in ["CTL", "JTL", "KTL"]:
            next_stage = "PR"
        elif stage == "PR":
            next_stage = "CLRD"
        elif stage == "CLRD":
            next_stage = "TS"
        elif stage == "TS":
            next_stage = "QC"
        elif stage == "QC":
            next_stage = "Release"

        if next_stage and task["assigned_to"]:
            if next_stage == "Release":
                guild = self.bot.get_guild(self.config.GUILD_ID)
                role = guild.get_role(self.config.ADMIN_ROLE) if guild else None
                if role:
                    await message.channel.send(f"🔜 <@&{role.id}> — {project} {chapter} is ready for release.")
                else:
                    await message.channel.send(f"🔜 {project} {chapter} is ready for release. (Admins, please finalize.)")
            else:
                await message.channel.send(f"🔜 <@{task['assigned_to']}> — you've been assigned **{next_stage}** for {project} {chapter}. Please begin.")

    @app_commands.command(name="claim", description="Claim a task for yourself")
    @app_commands.describe(project="Project name", chapter="Chapter identifier (e.g., CH 5)", stage="Workflow stage")
    async def claim(self, interaction: discord.Interaction, project: str, chapter: str, stage: str):
        await interaction.response.defer(ephemeral=True)

        if stage.upper() not in ["CTL", "JTL", "KTL", "PR", "CLRD", "TS", "QC"]:
            await interaction.followup.send("❌ Invalid stage.", ephemeral=True)
            return

        task = self.db.get_task(project=project, chapter=chapter, stage=stage.upper())
        if task and task["status"] != "Waiting":
            await interaction.followup.send(f"❌ This task is already {task['status'].lower()}.", ephemeral=True)
            return

        if not task:
            task_id = self.db.add_task(project=project, chapter=chapter, stage=stage.upper(), assigned_to=str(interaction.user.id), status="InProgress")
        else:
            self.db.update_task(task["task_id"], assigned_to=str(interaction.user.id), status="InProgress")
            task_id = task["task_id"]

        task = self.db.get_task(task_id=task_id)
        user_data = self.db.get_user(str(interaction.user.id))
        user_tz = user_data["timezone"] if user_data else "UTC"

        embed = create_task_embed(task, user_tz)
        await interaction.followup.send("✅ **Task claimed!**", embed=embed, ephemeral=True)

    @app_commands.command(name="progress", description="Update the progress of your assigned task.")
    @app_commands.describe(project="Project name", chapter="Chapter identifier", stage="Workflow stage", progress="Progress in 'done/total' format (e.g., 3/10)")
    async def progress(self, interaction: discord.Interaction, project: str, chapter: str, stage: str, progress: str):
        await interaction.response.defer(ephemeral=True)
        user_id = str(interaction.user.id)

        if stage.upper() not in ["CTL", "JTL", "KTL", "PR", "CLRD", "TS", "QC"]:
            await interaction.followup.send("❌ Invalid stage.", ephemeral=True)
            return

        # Validate progress format
        import re
        if not re.match(r'^\d+/\d+$', progress):
            await interaction.followup.send("❌ Invalid progress format. Please use 'done/total' (e.g., 3/10).", ephemeral=True)
            return

        task = self.db.get_task(project=project, chapter=chapter, stage=stage.upper())
        if not task:
            await interaction.followup.send(f"❌ No task found for {project} {chapter} - {stage.upper()}.", ephemeral=True)
            return

        if task["assigned_to"] != user_id:
            await interaction.followup.send("❌ You are not assigned to this task.", ephemeral=True)
            return

        if task["status"] == "Done":
            await interaction.followup.send("❌ This task is already marked as Done.", ephemeral=True)
            return

        try:
            self.db.update_task(task["task_id"], progress=progress, status="InProgress")
            updated_task = self.db.get_task(task_id=task["task_id"])
            user_data = self.db.get_user(user_id)
            user_tz = user_data["timezone"] if user_data else "UTC"
            embed = create_task_embed(updated_task, user_tz)
            await interaction.followup.send("✅ **Progress updated!**", embed=embed, ephemeral=True)
        except ValueError as e:
            await interaction.followup.send(f"❌ {e}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ An error occurred: {e}", ephemeral=True)


# Setup function
async def setup(bot):
    await bot.add_cog(TaskManagementCog(bot))

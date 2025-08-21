# cogs/timezone.py
import discord
from discord import app_commands
from discord.ext import commands
import pytz
from database.models import Database
from config import Config

class TimezoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.config = Config

    @app_commands.command(name="profile", description="Manage your profile settings.")
    @app_commands.choices(action=[
        app_commands.Choice(name="View Profile", value="view"),
        app_commands.Choice(name="Set Timezone", value="timezone"),
    ])
    @app_commands.describe(action="What profile setting to manage?")
    async def profile(self, interaction: discord.Interaction, action: str):
        user_id = str(interaction.user.id)
        user_data = self.db.get_user(user_id)

        if action == "view":
            if not user_data:
                await interaction.response.send_message("You have no profile yet. Use `/profile timezone` to set one.", ephemeral=True)
                return

            tz_name = user_data.get("timezone", "UTC")
            try:
                tz_obj = pytz.timezone(tz_name)
                # Note: datetime.utcnow() is naive. This is a simplified display.
                tz_display = f"{tz_name}"
            except:
                tz_display = tz_name

            embed = discord.Embed(title=f"{interaction.user.display_name}'s Profile", color=discord.Color.blurple())
            embed.add_field(name="Timezone", value=tz_display, inline=False)
            embed.add_field(name="Reminder Preference", value=user_data.get("reminder_pref", "morning"), inline=False)
            embed.add_field(name="Onboarded", value="Yes" if user_data.get("onboarded") else "No", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif action == "timezone":
            options = [
                discord.SelectOption(label=f"{tz[0]} ({tz[1]})", value=tz[1])
                for tz in self.config.COMMON_TIMEZONES
            ]
            options.append(discord.SelectOption(label="Other (Specify)", value="other", description="Enter a custom timezone."))

            view = TimezoneSelectView(self.db, options)
            await interaction.response.send_message("Please select your timezone:", view=view, ephemeral=True)

class TimezoneSelectView(discord.ui.View):
    def __init__(self, db, options):
        super().__init__(timeout=180)
        self.db = db
        self.select = discord.ui.Select(placeholder="Choose a timezone...", options=options)
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        selected_tz = self.select.values[0]

        if selected_tz == "other":
            modal = TimezoneModal(self.db)
            await interaction.response.send_modal(modal)
        else:
            try:
                pytz.timezone(selected_tz)
                self.db.update_user(user_id, timezone=selected_tz)
                await interaction.response.edit_message(content=f"✅ Your timezone has been set to **{selected_tz}**.", view=None)
            except pytz.UnknownTimeZoneError:
                await interaction.response.edit_message(content="❌ Invalid timezone selected.", view=None)

class TimezoneModal(discord.ui.Modal, title="Set Custom Timezone"):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.tz_input = discord.ui.TextInput(label="Timezone Name", placeholder="e.g., Europe/Berlin, America/Chicago", style=discord.TextStyle.short, required=True, max_length=50)
        self.add_item(self.tz_input)

    async def on_submit(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        tz_name = self.tz_input.value.strip()
        try:
            pytz.timezone(tz_name)
            self.db.update_user(user_id, timezone=tz_name)
            await interaction.response.send_message(f"✅ Your timezone has been set to **{tz_name}**.", ephemeral=True)
        except pytz.UnknownTimeZoneError:
            await interaction.response.send_message("❌ Invalid timezone name. Please use a standard IANA timezone (e.g., Europe/Berlin).", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TimezoneCog(bot))

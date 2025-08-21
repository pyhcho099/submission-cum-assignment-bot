# cogs/recruitment.py
import discord
from discord import app_commands
from discord.ext import commands
from config import Config

class RecruitmentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config

    @app_commands.command(name="recruit", description="Ping the recruitment role.")
    @app_commands.checks.has_role(Config.ADMIN_ROLE) # Only admins can use this
    async def recruit(self, interaction: discord.Interaction, message: str = "We are looking for new members!"):
        """Ping the recruitment role."""
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("❌ This command must be used in a server.", ephemeral=True)
            return

        recruit_role = guild.get_role(self.config.RECRUIT_ROLE)
        if not recruit_role:
            await interaction.response.send_message("❌ Recruitment role not found.", ephemeral=True)
            return

        await interaction.response.send_message(f"{recruit_role.mention} - {message}", allowed_mentions=discord.AllowedMentions(roles=True))

async def setup(bot):
    await bot.add_cog(RecruitmentCog(bot))

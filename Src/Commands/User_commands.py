import discord
from discord.ext import commands

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="apply")
    async def apply(self, ctx, role: str):
        role = role.upper()
        valid_roles = ['TL', 'CL', 'TS', 'QC']
        
        if role not in valid_roles:
            await ctx.send("Invalid role. Valid roles: TL, CL, TS, QC")
            return
        
        # Send application form via DM
        try:
            await ctx.author.send("Please fill out this application form and send it back:")
            await ctx.author.send(f"```\nApplication for {role} position\n\n1. Your experience:\n2. Why do you want to join?\n3. Any samples of your work:\n```")
            await ctx.send(f"Application form sent to {ctx.author.mention}")
        except:
            await ctx.send("Unable to send DM. Please enable DMs from server members.")

def setup(bot):
    bot.add_cog(UserCommands(bot))

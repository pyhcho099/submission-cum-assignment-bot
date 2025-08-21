import discord
from discord.ext import commands
from models.task_model import Task

class ProjectCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="projects", description="List all projects")
    async def projects(self, ctx):
        projects = Task.get_all_projects()
        
        if not projects:
            await ctx.respond("No projects found.")
            return
        
        response = "**Active Projects:**\n"
        for project in projects:
            response += f"• {project}\n"
        
        await ctx.respond(response)

def setup(bot):
    bot.add_cog(ProjectCommands(bot))

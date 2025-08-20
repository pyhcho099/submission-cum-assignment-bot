import os
from discord import Intents

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

# Channel IDs
ASSIGNMENTS_CHANNEL = int(os.getenv('ASSIGNMENTS_CHANNEL_ID'))
SUBMISSION_CHANNEL = int(os.getenv('SUBMISSION_CHANNEL_ID'))
TASK_BOARD_CHANNEL = int(os.getenv('TASK_BOARD_CHANNEL_ID'))
LOGS_CHANNEL = int(os.getenv('LOGS_CHANNEL_ID'))
RECRUITMENT_CHANNEL = int(os.getenv('RECRUITMENT_CHANNEL_ID'))

# Role IDs
ADMIN_ROLE = int(os.getenv('ADMIN_ROLE_ID'))
TL_ROLE = int(os.getenv('TL_ROLE_ID'))
CL_ROLE = int(os.getenv('CL_ROLE_ID'))
TS_ROLE = int(os.getenv('TS_ROLE_ID'))
QC_ROLE = int(os.getenv('QC_ROLE_ID'))

# Database
DB_PATH = 'data/tasks.db'

# Intents
intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- Discord settings ---
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD_ID = int(os.getenv("GUILD_ID"))

    # --- Channel IDs ---
    ASSIGNMENTS_CHANNEL = int(os.getenv("ASSIGNMENTS_CHANNEL"))
    SUBMISSION_CHANNEL = int(os.getenv("SUBMISSION_CHANNEL"))
    TASK_BOARD_CHANNEL = int(os.getenv("TASK_BOARD_CHANNEL"))
    LOGS_CHANNEL = int(os.getenv("LOGS_CHANNEL"))
    RECRUITMENT_CHANNEL = int(os.getenv("RECRUITMENT_CHANNEL"))
    # TIMEZONE_CHANNEL is optional for specific commands if needed

    # --- Role IDs ---
    ADMIN_ROLE = int(os.getenv("ADMIN_ROLE"))
    CHINESE_TRANSLATOR_ROLE = int(os.getenv("CHINESE_TRANSLATOR_ROLE"))
    JAPANESE_TRANSLATOR_ROLE = int(os.getenv("JAPANESE_TRANSLATOR_ROLE"))
    KOREAN_TRANSLATOR_ROLE = int(os.getenv("KOREAN_TRANSLATOR_ROLE"))
    PROOFREADER_ROLE = int(os.getenv("PROOFREADER_ROLE"))
    CLEANER_ROLE = int(os.getenv("CLEANER_ROLE"))
    TYPESETTER_ROLE = int(os.getenv("TYPESETTER_ROLE"))
    QC_ROLE = int(os.getenv("QC_ROLE"))
    RECRUIT_ROLE = int(os.getenv("RECRUIT_ROLE"))

    # --- Onboarding (for future use) ---
    # ONBOARDING_CHANNEL = int(os.getenv("ONBOARDING_CHANNEL", 0))
    # ONBOARDING_MESSAGE_ID = int(os.getenv("ONBOARDING_MESSAGE_ID", 0))

    # --- Idle thresholds (in hours) ---
    IDLE_THRESHOLDS = {
        "CTL": 72,
        "JTL": 72,
        "KTL": 72,
        "PR": 48,
        "CLRD": 48,
        "TS": 48,
        "QC": 24
    }

    # --- Common timezones for quick selection ---
    COMMON_TIMEZONES = [
        ("UTC-12", "Etc/GMT+12"),
        ("UTC-11", "Etc/GMT+11"),
        ("UTC-10", "Pacific/Honolulu"),
        ("UTC-8", "America/Los_Angeles"),
        ("UTC-5", "America/New_York"),
        ("UTC+0", "Europe/London"),
        ("UTC+1", "Europe/Paris"),
        ("UTC+5:30", "Asia/Kolkata"),
        ("UTC+8", "Asia/Singapore"),
        ("UTC+9", "Asia/Tokyo"),
        ("UTC+10", "Australia/Sydney")
    ]

    # --- Rate limiting ---
    COMMAND_RATE_LIMIT = 5 # commands per user per minute

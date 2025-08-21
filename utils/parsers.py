# utils/parsers.py
import re
import pytz
from datetime import datetime
from dateutil import parser as date_parser

def parse_submission(message):
    """
    Parse submission message
    Expected: submission - [Project] CH [num] | [link] | [stage]
    """
    content = message.content.strip()
    pattern = r"^submission\s*-\s*(.+?)\s+CH\s*(\d+)\s*\|\s*(https?://[^\s]+)\s*\|\s*(CTL|JTL|KTL|PR|CLRD|TS|QC)$"
    match = re.match(pattern, content, re.IGNORECASE) # Case-insensitive for stage

    if not match:
        return None, "Invalid format. Use: 'submission - [Project] CH [num] | [link] | [stage]'"

    project = match.group(1).strip()
    chapter = f"CH {match.group(2)}"
    file_url = match.group(3)
    stage = match.group(4).upper() # Ensure uppercase

    # Basic validation for supported file hosts
    allowed_domains = [
        "drive.google.com", "dropbox.com", "mega.nz", "onedrive.live.com"
    ]
    if not any(domain in file_url for domain in allowed_domains) or not file_url.startswith("https://"):
        return None, "Unsupported or invalid file link. Please use a link from Google Drive, Dropbox, Mega, or OneDrive."

    return {
        "project": project,
        "chapter": chapter,
        "file_url": file_url,
        "stage": stage
    }, None

def parse_assignment(message):
    """
    Parse assignment message
    Expected: assignment- <@user> | [Project] CH [num] | <#channel> | [stage]
    """
    content = message.content.strip()
    # This regex is more robust, handling both <@ID> and <@!ID> (nickname mention)
    pattern = r"^assignment-\s*<@!?(\d+)>\s*\|\s*(.+?)\s+CH\s*(\d+)\s*\|\s*<#(\d+)>\s*\|\s*(CTL|JTL|KTL|PR|CLRD|TS|QC)$"
    match = re.match(pattern, content, re.IGNORECASE) # Case-insensitive for stage

    if not match:
        return None, "Invalid format. Use: 'assignment- <@user> | [Project] CH [num] | <#channel> | [stage]'"

    return {
        "user_id": match.group(1),
        "project": match.group(2).strip(),
        "chapter": f"CH {match.group(3)}",
        "channel_id": match.group(4),
        "stage": match.group(5).upper() # Ensure uppercase
    }, None

def format_deadline_display(deadline_utc_str, user_timezone="UTC"):
    """Format deadline for display"""
    if not deadline_utc_str:
        return "Not set"
    try:
        deadline_utc = datetime.fromisoformat(deadline_utc_str)
        if deadline_utc.tzinfo is None:
            deadline_utc = pytz.UTC.localize(deadline_utc)
        user_tz = pytz.timezone(user_timezone)
        local_time = deadline_utc.astimezone(user_tz)
        utc_str = deadline_utc.strftime("%b %d, %I:%M %p UTC")
        local_str = local_time.strftime("%b %d, %I:%M %p")
        tz_abbr = local_time.tzname()
        return f"{local_str} ({tz_abbr}) / {utc_str}"
    except Exception:
        # Fallback if any conversion fails
        return deadline_utc_str if deadline_utc_str else "Not set"

```markdown
# Psyflixs Staff Bot

[![Discord](https://img.shields.io/discord/000000000000000000?color=7289da&label=Discord&logo=discord&logoColor=ffffff&style=for-the-badge)](YOUR_INVITE_LINK_HERE)
[![License](https://img.shields.io/github/license/yourusername/psyflixs-staff-bot?style=for-the-badge)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge)

An advanced, enterprise-grade Discord bot meticulously engineered for managing complex, distributed scanlation workflows with precision. Built to the exact specifications of Psyflixs Scans, it automates task tracking, enforces structured communication, and ensures workflow continuity.

## 🚀 Features

*   **Structured Workflow Engine:** Automates the full lifecycle: TL (CTL/JTL/KTL) → PR → CLRD → TS → QC → Release.
*   **Individual Assignments:** Tasks are assigned to specific users, eliminating noisy role pings. Notifications are direct and targeted.
*   **External File Link Support:** Seamlessly integrates with Google Drive, Dropbox, Mega, and OneDrive. No Discord file size limits.
*   **Progress Tracking:** Users can update task progress (e.g., `3/10 pages`) for real-time visibility.
*   **Rich Task Embeds:** Provides a clear, visual overview of each task's status, assignee, progress, and deadlines directly in Discord.
*   **Proactive Idle Detection:** Monitors tasks and automatically alerts assigned users if work stalls beyond stage-specific thresholds (e.g., 72h for TL, 24h for QC).
*   **Timezone Awareness:** Respects global team members. Users can set their timezone for accurate local time displays on deadlines and future reminders.
*   **Automated Workflow Advancement:** Upon submission, the bot automatically assigns the next stage (e.g., PR after JTL) to the same user or the next role.
*   **Comprehensive Logging:** All critical actions (assignments, submissions, claims) are timestamped and logged to a dedicated channel for transparency and audit.
*   **Staff Recruitment:** Admins can easily ping a designated recruitment role to find new team members.
*   **Secure & Compliant:** Designed with data minimization in mind. Stores only essential Discord IDs and user preferences. GDPR considerations are built-in.

## 🛠️ Setup & Deployment

### Prerequisites

*   **Python 3.8 or higher**
*   A Discord account and a server where you have administrative privileges.

### 1. Create a Discord Bot Application

1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Click "New Application". Give it a name (e.g., `Psyflixs Staff Bot`) and click "Create".
3.  Navigate to the "Bot" tab on the left sidebar.
4.  Click "Add Bot" and confirm.
5.  Under "Token", click "Reset Token" and copy the new token. **Keep this token secret.**
6.  Under "Privileged Gateway Intents", enable `MESSAGE CONTENT INTENT` and `SERVER MEMBERS INTENT`.
7.  Save your changes.

### 2. Configure Bot Permissions & Add to Server

1.  In the Developer Portal, go to "OAuth2" -> "URL Generator".
2.  In the "Scopes" section, check `bot` and `applications.commands`.
3.  In the "Bot Permissions" section, select the following permissions:
    *   `Send Messages`
    *   `Send Messages in Threads`
    *   `Manage Messages` (Optional, for cleaning up commands if needed)
    *   `Embed Links`
    *   `Attach Files` (Optional, for future features)
    *   `Read Message History`
    *   `Mention Everyone` (This bot uses individual mentions, but good to have)
    *   `Use Slash Commands`
4.  Copy the generated URL at the bottom.
5.  Paste the URL into your browser and follow the prompts to add the bot to your Psyflixs staff server.

### 3. Configure the Bot Code

1.  Clone or download this repository to your local machine or server.
    ```bash
    git clone https://github.com/yourusername/psyflixs-staff-bot.git
    cd psyflixs-staff-bot
    ```
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a file named `.env` in the project root directory.
5.  Copy the contents of `.env.example` into your new `.env` file.
6.  Open `.env` and replace all the placeholder values with your actual Discord bot token, server (guild) ID, and the IDs of the specific channels and roles you want the bot to interact with.
    *   **How to get IDs:** In Discord, enable Developer Mode (User Settings -> Advanced -> Developer Mode). Then, right-click on a channel, role, or the server name and select "Copy ID".

### 4. Run the Bot

With your virtual environment activated and `.env` configured, run the bot:
```bash
python main.py

You should see log messages indicating the bot is connecting and syncing commands. Once ready, its status will change on Discord.

## 🎮 Usage Guide

The bot primarily operates through two special channels and slash commands.

### 📜 Structured Channel Communication

The bot watches two specific channels for formatted messages. **The format is strict and must be followed exactly.**

#### `#assignments` Channel

To assign a task to a staff member, post a message in the designated `#assignments` channel using this exact format:

```
assignment- <@USER_MENTION> | [PROJECT_NAME] CH [CHAPTER_NUMBER] | <#WORK_CHANNEL> | [STAGE]
```

*   **`<@USER_MENTION>`**: The user to assign the task to (e.g., `<@123456789012345678>`).
*   **`[PROJECT_NAME]`**: The name of the project (e.g., `Fire Train`).
*   **`CH [CHAPTER_NUMBER]`**: The chapter identifier (e.g., `CH 23`). Volume formats like `Vol2-Ep8` are also supported.
*   **`<#WORK_CHANNEL>`**: The Discord channel where the work will be done (e.g., `<#987654321098765432>`).
*   **`[STAGE]`**: The workflow stage. Must be one of: `CTL`, `JTL`, `KTL`, `PR`, `CLRD`, `TS`, `QC`.

**Example:**
```
assignment- <@123456789012345678> | Fire Train CH 23 | <#987654321098765432> | JTL
```

#### `#submission` Channel

When a staff member finishes a task, they post a message in the designated `#submission` channel using this exact format:

```
submission - [PROJECT_NAME] CH [CHAPTER_NUMBER] | [EXTERNAL_FILE_LINK] | [STAGE]
```

*   **`[PROJECT_NAME]`**: The name of the project.
*   **`CH [CHAPTER_NUMBER]`**: The chapter identifier.
*   **`[EXTERNAL_FILE_LINK]`**: A direct link to the file on Google Drive, Dropbox, etc.
*   **`[STAGE]`**: The workflow stage being submitted.

**Example:**
```
submission - Fire Train CH 23 | https://drive.google.com/file/d/1a2b3c4d5e6f7g8h/view | JTL
```

### 🪄 Slash Commands (`/`)

Access these by typing `/` in any channel the bot can see.

*   **`/claim <project> <chapter> <stage>`**
    *   Allows a staff member to claim an unassigned task for themselves.
    *   Example: `/claim project:"Fire Train" chapter:"CH 23" stage:JTL`

*   **`/progress <project> <chapter> <stage> <progress>`**
    *   Allows the assigned user to update the progress of their task (e.g., `5/10`).
    *   Example: `/progress project:"Fire Train" chapter:"CH 23" stage:JTL progress:5/10`

*   **`/profile <action>`**
    *   Manage your personal settings.
    *   Actions:
        *   `view`: See your current profile (timezone, etc.).
        *   `timezone`: Set your IANA timezone for accurate local time displays.

*   **`/recruit [message]`** *(Admin Only)*
    *   Pings the designated recruitment role with a custom message (or a default one).
    *   Example: `/recruit message:"We need more JTLs!"`

## 📁 Project Structure


psyflixs-staff-bot/
├── main.py                 # Entry point to start the bot
├── config.py               # Centralized configuration loader (loads from .env)
├── requirements.txt        # List of Python dependencies
├── .env.example            # Template for environment variables
├── .gitignore              # Specifies files/folders to ignore in Git
├── README.md               # This file
├── LICENSE                 # (Add your chosen license file)
├── database/
│   ├── __init__.py
│   └── models.py           # SQLite database schema and ORM-like functions
├── cogs/
│   ├── __init__.py
│   ├── task_management.py  # Core logic for assignments, submissions, claims, progress
│   ├── timezone.py         # Profile and timezone management commands
│   ├── notifications.py    # Idle task detection and alerting system
│   └── recruitment.py      # Staff recruitment command
└── utils/
    ├── __init__.py
    ├── parsers.py          # Functions to parse assignment/submission messages
    └── embeds.py           # Functions to create rich Discord embeds for tasks

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find a bug or have a feature suggestion. Ensure your code adheres to the existing style and includes appropriate tests if applicable.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

*   Built with [discord.py](https://github.com/Rapptz/discord.py)
*   Inspired by the needs of the Psyflixs Scans team.


This `README.md` provides a comprehensive overview for anyone looking to understand, set up, or contribute to your bot. Make sure to replace `yourusername` and `YOUR_INVITE_LINK_HERE` with your actual GitHub username and a Discord invite link for your server (if public or shareable).

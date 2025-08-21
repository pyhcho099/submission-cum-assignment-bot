
# Psyflixs Staff Bot

[![Discord](https://img.shields.io/discord/000000000000000000?color=5865F2&label=Discord&logo=discord&logoColor=white&style=for-the-badge)](YOUR_DISCORD_INVITE_LINK)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&style=for-the-badge)](https://www.python.org)

> **"Where the players are"** — Discord is the central hub for communities. This bot is where the **work** gets done.

**Psyflixs Staff Bot** is an enterprise-grade workflow automation engine built for the Psyflixs Scans team. It transforms Discord from a simple chat app into a powerful, structured task management system, perfectly aligned with your unique scanlation pipeline: **TL → PR → CLRD → TS → QC → Release**.

This bot eliminates manual tracking, enforces clean communication, and ensures your projects move forward efficiently, all without a single role ping. Just as games like **World of Warcraft** and **SUPERVIVE** use Discord to build thriving communities, your team can use this bot to build a thriving *workflow*. Discord is where your staff are—this bot is where they get their work done.

## 🚀 Key Features

*   **Precision Individual Assignment:** Tasks are assigned to specific staff members. No more spamming entire roles.
*   **Google Drive & External File Integration:** Seamlessly link files hosted on Drive, Dropbox, Mega, or OneDrive. No Discord upload limits.
*   **Structured Message Parsing:** Automates task creation and submission via strict, easy-to-follow formats in dedicated channels.
*   **Automated Workflow Progression:** When a task is submitted, the next stage (e.g., PR after JTL) is automatically assigned, keeping the pipeline flowing.
*   **Proactive Idle Detection:** The bot monitors task activity and sends direct alerts to assigned users if a task stalls beyond defined thresholds (e.g., 72h for TL, 24h for QC).
*   **Rich Task Embeds:** Get a clear, visual overview of every task with status, progress bars, soft targets, and assignment details.
*   **Progress Tracking:** Staff can update their progress (e.g., `5/10 pages`) to provide real-time updates.
*   **Timezone-Aware Profiles:** Staff set their timezone so deadlines are displayed in their local time.
*   **Comprehensive Audit Logging:** Every action (assignment, submission, claim) is logged in a dedicated channel for full transparency.
*   **Staff Recruitment:** Admins can instantly ping the recruitment role to find new talent.

## 🛠️ Installation & Setup

### Prerequisites

*   **Python 3.8+** installed on your machine or server.
*   **Discord Developer Access:** You need to create a bot application on the [Discord Developer Portal](https://discord.com/developers/applications).

### Step 1: Create Your Discord Bot

1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2.  Navigate to the **Bot** tab and add a bot to your application.
3.  **Copy the Bot Token.** This is your bot's password—**keep it secure and never share it publicly.**
4.  Under **Privileged Gateway Intents**, enable `MESSAGE CONTENT INTENT` and `SERVER MEMBERS INTENT`.
5.  Save your changes.

### Step 2: Invite the Bot to Your Server

1.  In the Developer Portal, go to **OAuth2** > **URL Generator**.
2.  Select the scopes: `bot` and `applications.commands`.
3.  In the **Bot Permissions** section, grant the following:
    *   `Send Messages`, `Send Messages in Threads`, `Manage Messages`
    *   `Embed Links`, `Attach Files`, `Read Message History`
    *   `Use Slash Commands`, `Mention Everyone`
4.  Copy the generated URL, open it in a browser, and select your Psyflixs staff server to invite the bot.

### Step 3: Configure the Bot

1.  Clone this repository:
    ```bash
    git clone https://github.com/yourusername/psyflixs-staff-bot.git
    cd psyflixs-staff-bot
    ```
2.  **(Recommended)** Create a virtual environment:
    ```bash
    python -m venv venv
    # Activate on Windows:
    venv\Scripts\activate
    # Activate on macOS/Linux:
    source venv/bin/activate
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env  # On macOS/Linux
    # Or manually create a .env file on Windows
    ```
5.  Open `.env` and fill in your specific values:
    *   `DISCORD_TOKEN`: Paste the token you copied from the Developer Portal.
    *   `GUILD_ID`: The ID of your Discord server (enable Developer Mode in Discord settings to copy it).
    *   All `*_CHANNEL` and `*_ROLE` IDs: Copy the IDs of your specific channels and roles from Discord.

### Step 4: Run the Bot

With your environment activated and `.env` configured, start the bot:
```bash
python main.py
```
The bot will connect, sync its slash commands, and be ready to use.

## 🎮 How to Use

### 📜 Using `#assignments` and `#submission` Channels

The bot watches these channels for messages in a **strict format**. **Pasting the exact example is the best way to avoid errors.**

#### To Assign a Task (`#assignments`)
Post this message:
```
assignment- <@USER> | [Project Name] CH [Number] | <#Work Channel> | [Stage]
```
**Example:**
```
assignment- <@1024675887934885938> | Fire Train CH 23 | <#1365758736416772226> | JTL
```
The bot will confirm the assignment and DM the user.

#### To Submit a Task (`#submission`)
Post this message:
```
submission - [Project Name] CH [Number] | [Your Google Drive Link] | [Stage]
```
**Example:**
```
submission - Fire Train CH 23 | https://drive.google.com/file/d/1a2b3c4d5e6f7g8h/view | JTL
```
The bot will record the submission, update the task, and notify the next person in line.

### 🪄 **Full Slash Commands Reference**

Access these commands by typing `/` in any Discord channel.

#### **1. Task Management**

*   **`/claim`**
    *   **Description:** Claim an unassigned task for yourself.
    *   **Permissions:** All Staff (CTL, JTL, KTL, PR, CLRD, TS, QC)
    *   **Arguments:**
        *   `project` (Required, String): The name of the project (e.g., "Fire Train").
        *   `chapter` (Required, String): The chapter identifier (e.g., "CH 5", "Vol2-Ep8").
        *   `stage` (Required, String): The workflow stage. Must be one of: `CTL`, `JTL`, `KTL`, `PR`, `CLRD`, `TS`, `QC`.
    *   **Example:** `/claim project:"Fire Train" chapter:"CH 5" stage:JTL`

*   **`/progress`**
    *   **Description:** Update the progress of a task you are currently assigned to.
    *   **Permissions:** All Staff (CTL, JTL, KTL, PR, CLRD, TS, QC)
    *   **Arguments:**
        *   `project` (Required, String): The name of the project.
        *   `chapter` (Required, String): The chapter identifier.
        *   `stage` (Required, String): The workflow stage of the task you're updating.
        *   `progress` (Required, String): Your current progress in the format `done/total` (e.g., `3/10`).
    *   **Example:** `/progress project:"Fire Train" chapter:"CH 5" stage:PR progress:5/10`

#### **2. Profile & Settings**

*   **`/profile`**
    *   **Description:** View or manage your user profile settings.
    *   **Permissions:** All Staff
    *   **Arguments:**
        *   `action` (Required, Choice): The action to perform.
            *   `view`: View your current profile information (timezone, reminder preference).
            *   `timezone`: Open a menu to set your IANA timezone (e.g., "Asia/Tokyo", "America/New_York").
    *   **Examples:**
        *   `/profile action:view`
        *   `/profile action:timezone`

#### **3. Recruitment**

*   **`/recruit`**
    *   **Description:** Ping the designated recruitment role to announce a need for new staff.
    *   **Permissions:** Admins only
    *   **Arguments:**
        *   `message` (Optional, String): A custom message to send with the ping. Defaults to "We are looking for new members!" if not provided.
    *   **Examples:**
        *   `/recruit`
        *   `/recruit message:"We need more Chinese Translators!"`

---

### 📌 **Command Summary**

| Command | Description | Permissions |
| :--- | :--- | :--- |
| **`/claim`** | Claim an unassigned task. | All Staff |
| **`/progress`** | Update your task progress. | All Staff |
| **`/profile`** | View or set your profile. | All Staff |
| **`/recruit`** | Ping the recruitment role. | Admins |

## 📁 Project Structure

This modular structure ensures clean, maintainable code.

```
psyflixs-staff-bot/
├── main.py                 # The main entry point
├── config.py               # Loads settings from .env
├── requirements.txt        # Python dependencies
├── .env.example            # Template for configuration
├── .gitignore
├── README.md               # You are here!
├── LICENSE
├── database/
│   └── models.py           # SQLite database operations
├── cogs/
│   ├── task_management.py  # Core assignment/submission logic
│   ├── timezone.py         # User profile and timezone commands
│   ├── notifications.py    # Idle task checker
│   └── recruitment.py      # Recruit command
└── utils/
    ├── parsers.py          # Validates message formats
    └── embeds.py           # Generates Discord embeds
```

## 🤝 Contributing

Found a bug? Have a great idea? We welcome contributions! Please open an issue or submit a pull request. Let's build the best tool for scanlators together.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 💬 Get Inspired

Just as games like **World of Warcraft** and **SUPERVIVE** use Discord to build thriving communities, your team can use this bot to build a thriving *workflow*. Discord is where your staff are—this bot is where they get their work done.

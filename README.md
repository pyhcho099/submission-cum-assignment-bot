# 🎬 Psyflixs Staff Bot

A Discord bot designed to streamline task management for scanlation teams. Automate task claiming, submissions, progress tracking, and team coordination directly within Discord.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## ✨ Features

- 📥 **Claim & Submit Tasks** via commands or natural language
- 🧩 **Automated Role Pings** when tasks are completed
- 🗂️ **Task & Project Tracking** with persistent database
- 📊 **Slash Commands** for easy interaction
- 📤 **Export Data** to CSV for reporting
- 🔔 **Reminders & Notifications** for deadlines
- 📝 **Application System** for new recruits
- 🛠️ **Admin Tools** for task assignment and releases

---

## 🗂️ Project Structure

```
psyflixs-staff-bot/
├── src/
│   ├── bot.py
│   ├── config.py
│   ├── database.py
│   ├── commands/
│   │   ├── task_commands.py
│   │   ├── project_commands.py
│   │   ├── user_commands.py
│   │   └── admin_commands.py
│   ├── listeners/
│   │   ├── message_listener.py
│   │   └── button_listener.py
│   ├── models/
│   │   └── task_model.py
│   ├── utils/
│   │   ├── embed_utils.py
│   │   ├── task_utils.py
│   │   └── role_utils.py
│   └── scheduler/
│       └── reminder_scheduler.py
├── data/
│   └── tasks.db
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Create a Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the **Bot** section and add a bot
4. Enable the following intents:
   - `Server Members Intent`
   - `Message Content Intent`
5. Copy the bot token

### 2. Invite the Bot to Your Server
Use the OAuth2 URL generator with:
- Scopes: `bot`
- Permissions: `Send Messages`, `Manage Roles`, `Read Messages`, `Use Slash Commands`, etc.

### 3. Set Environment Variables
Create a `.env` file or set these in your environment:

```bash
DISCORD_TOKEN="your_bot_token"
GUILD_ID="your_server_id"
ASSIGNMENTS_CHANNEL_ID="channel_id"
SUBMISSION_CHANNEL_ID="channel_id"
TASK_BOARD_CHANNEL_ID="channel_id"
LOGS_CHANNEL_ID="channel_id"
RECRUITMENT_CHANNEL_ID="channel_id"
ADMIN_ROLE_ID="role_id"
TL_ROLE_ID="role_id"
CL_ROLE_ID="role_id"
TS_ROLE_ID="role_id"
QC_ROLE_ID="role_id"
```

> 💡 Tip: Use tools like `python-dotenv` for easier management.

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Bot
```bash
python src/bot.py
```

---

## 🤖 Commands

### User Commands
| Command | Description |
|--------|-------------|
| `/claim project chapter stage` | Claim a task (TL, CL, TS, QC) |
| `/submit project chapter stage` | Submit a completed task |
| `/tasks [user]` | View your or another user's tasks |
| `/status project chapter` | Check status of all stages for a chapter |
| `/projects` | List all active projects |
| `!apply TL/CL/TS/QC` | Apply for a team role (via DM) |

### Admin Commands
| Command | Description |
|--------|-------------|
| `/assign task_id @user` | Manually assign a task |
| `/release project chapter` | Mark a chapter as released |
| `/export` | Export all tasks to CSV |

---

## 📱 Mobile Usage

While the bot **can be used fully from mobile** via the Discord app, **development and hosting** are best done on desktop or via cloud platforms:

- ✅ Use **Replit**, **GitHub Codespaces**, or **Termux (Android)** for mobile coding
- ✅ Host on **Replit**, **Railway**, or **Render** for 24/7 uptime
- ✅ Monitor via Discord notifications

---

## 📊 Database

- Uses **SQLite** (`data/tasks.db`)
- Stores: Task ID, Project, Chapter, Stage, Assignee, Status, Deadline, Notes
- Automatically created on first run

---

## 🔄 Auto-Ping Flow

When a task is submitted:
```
TL → CL → TS → QC → Admin (Release)
```
Each stage completion automatically pings the next role in line.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙌 Support

For issues or feature requests, open an issue on GitHub or contact the developer.

> Made with ❤️ for scanlation teams

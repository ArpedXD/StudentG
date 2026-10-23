# StudentG

A simple student-focused web app that demonstrates account authentication, real-time WebSocket chat, a FastAPI backend, Pydantic validation, structured error handling, and group chat management, all backed by MySQL.

## Features

- **Accounts:** sign up and log in with username, email and password (passwords hashed with bcrypt)
- **Cookie sessions:** a random session ID is issued on login and checked on every protected request
- **Group chats:** create a group, which generates an invite code and makes you its Admin
- **Real-time messaging:** messages are pushed instantly to everyone in the group over WebSockets and saved to MySQL
- **Message history:** the latest 10 messages load first, and scrolling to the top loads older ones
- **Member management:** admins can search for users, invite them, and remove members
- **Markdown:** incoming messages are rendered with [marked](https://github.com/markedjs/marked)
- **Dashboard shell:** Home, Announcement, Assignments, Automated and Notifications sections are laid out but still placeholders

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI, Pydantic |
| Real-time | FastAPI WebSockets |
| Database | MySQL (`mysql-connector-python` with connection pooling) |
| Security | bcrypt password hashing, `HttpOnly` session cookies |
| Frontend | Plain HTML, CSS and JavaScript (no build step) |

## Project Structure

```
StudentG/
├── StudentG/                     # Backend (FastAPI)
│   ├── main.py                   # App entry point, DB pool, CORS, router setup
│   ├── api/                      # Route definitions (login, signup, chat)
│   ├── services/                 # Business logic (auth, chat, groups, websocket)
│   ├── repositories/             # All SQL queries
│   ├── schemas/                  # Pydantic request models
│   ├── core/                     # Validators and enums
│   ├── dependencies/             # Database cursor helper
│   ├── Exceptions/               # Custom exception classes
│   └── websocketAPIreference.py  # Minimal WebSocket demo endpoint
└── StudentG ( web)/              # Frontend
    ├── index.html                # Landing page
    ├── Pages/                    # forms.html (login/signup), dashboard.html
    ├── CSS/
    └── JS/
```

## How It Works

**Layered backend.** The backend is organized like a restaurant: `api/` is the waiter taking orders, `services/` is the kitchen applying the logic, and `repositories/` is the pantry where all the SQL lives. Keeping them separate means you can change a recipe without rebuilding the dining room.

**Authentication.** Signing up is like getting a wristband at a festival. The server checks your details, hashes your password with bcrypt so it's never stored readable, then hands your browser a random session ID cookie. Every later request shows that wristband, so you never resend your password.

**Validation.** Pydantic is the bouncer checking IDs at the door: if a request is missing fields or has the wrong types, it's rejected before reaching your code. A custom Validator then checks the rules Pydantic can't, like 8-character minimums and matching passwords, returning friendly messages instead of crashes.

**Real-time chat.** A normal HTTP request is like sending a letter and waiting for a reply. A WebSocket is a phone call that stays open. Once connected, the server can push a new message to everyone in a group instantly, without anyone refreshing, and each message is also saved to MySQL.

**Connection pooling.** Opening a database connection is slow, like hiring a taxi for every errand. The app keeps a pool of 10 connections warm at startup, so each request borrows one and hands it back when done. This keeps responses fast and stops the database being overwhelmed.

**Group roles.** The person who creates a group becomes its Admin, like a club president holding the guest list. Admins can open group settings to search for users, invite them, or remove members, while everyone else just chats. This keeps membership under one person's control.

## Getting Started

### Prerequisites

- Python 3.10+ (developed on 3.14)
- A running MySQL server
- A static file server for the frontend, such as the VS Code **Live Server** extension

### 1. Install dependencies

There is no `requirements.txt` yet, so install the packages directly:

```bash
pip install fastapi "uvicorn[standard]" mysql-connector-python python-dotenv bcrypt
```

### 2. Set up the database

Create a database and these tables. The schema isn't in the repo, so this is reconstructed from the queries in `repositories/`; adjust types to taste.

```sql

CREATE TABLE IF NOT EXISTS users(
	user_id int AUTO_INCREMENT PRIMARY KEY,
    username text,
    password text,
	email text,
    group_limit int
);

CREATE TABLE IF NOT EXISTS sessions(
	user_id int NOT NULL,
    session_id text,
    foreign key(user_id)
		references users(user_id)
);

CREATE TABLE IF NOT EXISTS group_chat(
	group_id int AUTO_INCREMENT PRIMARY KEY,
    group_name text,
    group_code text
);

CREATE TABLE IF NOT EXISTS group_members(
	group_id int not null,
    user_id int not null,
    foreign key(user_id)
		references users(user_id),
	foreign key(group_id)
		references group_chat(group_id)
);

CREATE TABLE IF NOT EXISTS group_messages(
	message_id int AUTO_INCREMENT PRIMARY KEY,
	group_id int not null,
    message text,
    user_id int not null,
    foreign key(user_id)
		references users(user_id),
	foreign key(group_id)
		references group_chat(group_id)
);
```

### 3. Configure environment variables

Create a `.env` file inside the `StudentG/` backend folder:

```env
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=your_database
DB_USERNAME=your_user
DB_PASSWORD=your_password
```

### 4. Run the backend

Run from inside the backend folder, since imports are relative to it:

```bash
cd StudentG
uvicorn main:app --reload
```

The API is now at `http://127.0.0.1:8000`, with interactive docs at `/docs`.

### 5. Serve the frontend

Open the `StudentG ( web)` folder with Live Server on port **5500** and visit `index.html`. The backend only allows CORS from `http://127.0.0.1:5500`, and the frontend calls the API at `http://127.0.0.1:8000`, so use those exact addresses.

## API Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/account/signup` | Create an account and start a session |
| `POST` | `/account/login` | Log in and start a session |
| `GET` | `/chat/isLoggedin` | Verify the session cookie (401 if invalid) |
| `POST` | `/chat/create` | Create a group chat (caller becomes Admin) |
| `GET` | `/chat/Groupload` | List the caller's group chats |
| `WS` | `/chat/connect?chat=<group_id>` | Real-time chat connection |
| `GET` | `/chat/load_messages?chat=&messages=&before=` | Page through message history |
| `POST` | `/chat/search_user` | Search users by name (plain-text body) |
| `GET` | `/chat/showMembers?chat=` | List a group's members |
| `GET` | `/chat/isAdmin?chat=` | Check whether the caller is the group's Admin |
| `GET` | `/chat/invite?chat=&target_user=` | Add a user to a group (Admin only) |
| `GET` | `/chat/remove?chat=&target_user=` | Remove a user from a group (Admin only) |
| `WS` | `/main/ws` | Minimal WebSocket demo endpoint |

## Before Deploying

- Add a `.gitignore` covering `.env` and `__pycache__/` so credentials and bytecode stay out of version control.
- The frontend URLs (`http://127.0.0.1:8000`) and the CORS origin in `main.py` are hard-coded for local development.
- The session cookie is set with `Secure` and `SameSite=None`, so cross-origin use expects HTTPS.

## Author

Built by [ArpedXD](https://github.com/ArpedXD).

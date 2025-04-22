# Minimalistic Task Manager

A lightweight task management system designed for small teams and developers. Built with Django, it offers project-based task tracking, filtering, status control.

## Features

- ✅ Create and manage multiple projects
- 🧩 Create tasks with types, priorities, tags, deadlines, and assignees
- 📌 Assign tasks to team members
- 🏷️ Tag tasks for easy categorization
- 🔎 Filter tasks by status, priority, or type using dynamic filters (HTMX)
- 📜 Comment system on tasks
- 🕒 Deadline tracking with color-coded urgency
- 📇 Auto-generated task numbers based on type (e.g., `B-001`, `D-002`)
- 👤 Custom user model with positions (e.g., Backend Developer, Designer)

## Technologies Used

- Django 5.x
- HTMX
- Bootstrap 5
- Crispy Forms
- SQLite (for development)

## Url:
https://minimalistic-task-manager.onrender.com

login: user | pass: user12345

## Installation

1. Clone the repository:

```bash
git clone https://github.com/d-stegantsev/task-manager.git
cd task-manager
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations and create superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Load demo data (optional):

```bash
python manage.py loaddata demo_fixture.json
```

6. Run the development server:

```bash
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

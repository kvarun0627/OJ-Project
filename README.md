# 🧠 Online Judge System

A full-stack **Online Judge platform** currently focusing on scalability — built using **Django**, **PostgreSQL**, **Docker**, **Celery**, and **Redis**. Supports user authentication, problem CRUD, secure code execution, verdict generation, and async task handling via workers.

---

## 🚀 Features

- 🔐 **User Authentication** – Register, Login, Logout, Password Reset
- 📝 **Problem Management** – Full CRUD
- 💻 **Code Submission** – Run C++ and Python code
- ✅ **Verdict System** – Automatically checks submissions against all test cases
- 🔄 **Async Execution** – Powered by **Celery** and **Redis Queue**
- 🐳 **Fully Containerized** – Docker Compose setup for dev & prod
- 🧪 **Multiple Test Case Handling** – JSON-based input/output validation

---

## 🛠️ Tech Stack

| Layer          | Tech Stack                             |
|----------------|----------------------------------------|
| 👨‍💻 Backend     | Django, Django REST Framework           |
| 🧠 Async Queue  | Celery + Redis                         |
| 🧪 Judge Engine | Python-based isolated code runners     |
| 🗄️ Database     | PostgreSQL                             |
| 📦 Containers   | Docker, Docker Compose                 |
| 🌐 Authentication   |    Django's own authentication   |

---

## ⚙️ Setup & Installation

### 1. 🔧 Clone the Repo
```bash
git clone https://github.com/kvarun0627/online-judge-django.git
cd online-judge-django

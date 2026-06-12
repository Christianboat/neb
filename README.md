<div align="center">
  <h1>🌌 Nebula Cybernetics Academy</h1>
  <p><b>Accelerating human evolution globally through innovative tech programs and AI events.</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=for-the-badge&logo=flask&logoColor=black" alt="Flask">
    <img src="https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-blue?style=for-the-badge&logo=sqlite&logoColor=white" alt="Database">
    <img src="https://img.shields.io/badge/UI-Vanilla%20CSS-blueviolet?style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
  </p>
</div>

<br/>

## 📖 Overview

**Nebula Cybernetics Academy** is a state-of-the-art web platform engineered to manage global robotics tournaments, neural interface bootcamps, quantum computing leagues, and technology expos. Built on Python & Flask, this application provides a highly customizable, dynamic content management ecosystem for educational technology institutes.

The platform includes a **comprehensive admin panel** that allows administrators to dynamically update programs, news, partnerships, metrics, and more, serving as the central hub for our Neo-Tokyo headquarters.

---

## ✨ Key Features

- 🤖 **Dynamic Program Management:** Complete CRUD capabilities for global robotics competitions, AI summits, and neural training hubs.
- 🏢 **Tech Expos & Partnerships:** Manage corporate sponsors (e.g., OmniCorp Tech), partnership tiers, and virtual exhibitions.
- 🎓 **Neural Learning Hub:** Interactive infrastructure for managing advanced cybernetics courses and AI ethics olympiads.
- 📊 **Real-time Impact Metrics:** Visually highlight "Engineers Trained," "Neural Models Deployed," and "Global Nodes" directly from the dashboard.
- 🖼️ **Media Gallery:** Built-in image upload capabilities for event highlights and futuristic tech showcases.
- 🔐 **Secure Administration:** Custom, secure, role-based authentication system built natively with Flask-Login and Werkzeug security.

---

## 🏗️ Architecture

- **Backend:** Flask, SQLAlchemy (ORM), Flask-Migrate (Database versioning)
- **Frontend:** HTML5, Vanilla CSS, Jinja2 Templating Engine
- **Security:** CSRF Protection, Password Hashing, Session Management
- **Database:** SQLite (Development) / PostgreSQL (Production ready)

---

## 🚀 Getting Started

Follow these steps to deploy and run Nebula Cybernetics Academy locally.

### Prerequisites
- Python 3.9+
- `pip` (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/Christianboat/neb.git
cd neb
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Rename the provided `.env.example` file to `.env` and configure your local settings:
```bash
SECRET_KEY=your-secure-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
```

### 5. Seed the Database
The project comes with a comprehensive seed script that generates dynamic AI content, futuristic imagery, and initial data structures.

```bash
python seed.py
```
> **Note:** If an `ADMIN_PASSWORD` is not set in `.env`, the script will automatically generate a secure temporary password and print it to the console. Save it to log in!

### 6. Run the Server
```bash
python run.py
```
Your application will be live at: [http://localhost:5000](http://localhost:5000)

---

## 💻 Admin Dashboard Access

To access the backend portal to manage the content:
1. Navigate to `http://localhost:5000/admin/login`
2. Use the `ADMIN_USERNAME` and password generated during the seeding phase.
3. Manage users, update the gallery, modify site settings, and process inquiries.

---

## 🤝 Contribution Guidelines

We welcome contributions from engineers, UI designers, and AI ethicists!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NeuralInterface`)
3. Commit your Changes (`git commit -m 'Add Neural Interface Module'`)
4. Push to the Branch (`git push origin feature/NeuralInterface`)
5. Open a Pull Request

---

## 📜 License

&copy; 2026 Nebula Cybernetics Academy. All Rights Reserved.

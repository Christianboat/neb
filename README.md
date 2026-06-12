# Nebula Cybernetics Academy

Welcome to the **Nebula Cybernetics Academy** platform! This is a state-of-the-art web application built with Flask, designed to manage global robotics tournaments, neural interface bootcamps, quantum computing leagues, and technology expos.

## Features

- **Robotics Competitions**: Manage global engineering and autonomous bot tournaments.
- **Tech Expos**: Virtual exhibition management and registration.
- **Neural Learning Hub**: Interactive courses for advanced cybernetics.
- **Admin Dashboard**: Manage students, teams, programs, news, and site settings.
- **Dynamic Content Management**: Easily update the website's gallery, testimonials, and core pages directly from the admin panel.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-new-repo-url>
   cd nebula-cybernetics-academy
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database and Seed Content:**
   ```bash
   python seed.py
   ```
   *(Note: The seed script will output a temporary admin password for the dashboard.)*

5. **Run the Application:**
   ```bash
   python run.py
   ```
   Navigate to `http://localhost:5000` in your web browser.

## Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** HTML5, Vanilla CSS, Jinja2 Templates
- **Database:** SQLite (development)

## License

&copy; 2026 Nebula Cybernetics Academy. All Rights Reserved.

# MyTech Website - Local Setup & Usage Guide

This guide will help you set up and run the MyTech website on your local computer.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Website Locally](#running-the-website-locally)
4. [Accessing the Website](#accessing-the-website)
5. [Using the Admin Panel](#using-the-admin-panel)
6. [Database Setup](#database-setup)
7. [Troubleshooting](#troubleshooting)
8. [Project Structure](#project-structure)

---

## 💻 System Requirements

Before you start, make sure you have the following installed on your computer:

### Required:
- **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
- **Git** - Download from [git-scm.com](https://git-scm.com/)
- **Code Editor** - VS Code, PyCharm, or any text editor

### Optional:
- **PostgreSQL** - For production database (SQLite is included by default)

---

## 🚀 Installation Steps

### Step 1: Clone or Download the Project

**If using Git:**
```bash
git clone <your-repository-url>
cd mytech-website
```

**If using Download:**
- Download the project as ZIP
- Extract to your desired folder
- Open terminal in that folder

### Step 2: Create a Virtual Environment

A virtual environment keeps your project dependencies separate from other Python projects.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal should show `(venv)` at the beginning of each line.

### Step 3: Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- Flask-Login (User authentication)
- Flask-SQLAlchemy (Database ORM)
- Flask-WTF (Form handling & CSRF protection)
- Pillow (Image processing)
- Python-dotenv (Environment variables)
- Email-validator (Email validation)
- Psycopg2-binary (PostgreSQL support)

### Step 4: Create Environment File

Create a `.env` file in the project root directory:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

If `.env.example` doesn't exist, create a new `.env` file with:

```
FLASK_ENV=development
FLASK_APP=app.py
SESSION_SECRET=your-secret-key-here-change-this
DATABASE_URL=sqlite:///mytech.db
```

---

## ▶️ Running the Website Locally

### Start the Flask Development Server

**With virtual environment activated:**

```bash
python app.py
```

**Or using Flask CLI:**

```bash
flask run
```

You should see output like:
```
⚠️ PostgreSQL failed... Falling back to SQLite
Admin account created! Please change password immediately after first login.
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### Keep the Terminal Running

Keep this terminal window open while developing. The server will restart automatically when you make changes.

---

## 🌐 Accessing the Website

Once the server is running:

### Public Website
- **Home:** http://localhost:5000/
- **About:** http://localhost:5000/about
- **Services:** http://localhost:5000/services
- **Portfolio:** http://localhost:5000/portfolio
- **Team:** http://localhost:5000/team
- **Blog:** http://localhost:5000/blog
- **Careers:** http://localhost:5000/careers
- **Contact:** http://localhost:5000/contact
- **Technologies:** http://localhost:5000/technologies
- **Testimonials:** http://localhost:5000/testimonials
- **FAQ:** http://localhost:5000/faq
- **Get a Quote:** http://localhost:5000/quote

### Admin Panel
- **Login:** http://localhost:5000/admin/login
- **Dashboard:** http://localhost:5000/admin

---

## 🔑 Using the Admin Panel

### Default Admin Credentials

```
Username: Shawaiz
Email: 231980079@gift.edu.pk
Password: Shawaiz231980079
```

### First Login Steps

1. Go to http://localhost:5000/admin/login
2. Enter username: `Shawaiz`
3. Enter password: `Shawaiz231980079`
4. Click "Login"
5. **IMPORTANT:** Change your password immediately!
   - Click "Profile" in the admin menu
   - Click "Change Password"
   - Enter new password
   - Save

### Adding Content

After logging in, you can manage all website content:

**Services**
- Go to Admin → Services → Add New Service
- Fill in title, description, icon image
- Save

**Projects/Portfolio**
- Go to Admin → Projects → Add New Project
- Upload multiple project images
- Add technologies and description
- Save

**Blog Posts**
- Go to Admin → Blogs → Add New Blog
- Write content, upload cover image
- Set status to "Published"
- Save

**Team Members**
- Go to Admin → Team → Add New Member
- Upload profile photo
- Add social links
- Save

**Job Postings**
- Go to Admin → Jobs → Add New Job
- Fill in job details
- Save

**View Messages**
- Go to Admin → Contact Messages
- Click "View" button to see full message
- Reply or delete as needed

**Website Settings**
- Go to Admin → Site Settings
- Update company name, logo, contact info
- Configure WhatsApp button
- Customize hero section
- Save

For detailed instructions on each feature, see **README.md**.

---

## 🗄️ Database Setup

### SQLite (Default - Recommended for Local Development)

SQLite is included by default and requires no setup.

**Database file:** `mytech.db` (automatically created in project root)

**To reset the database:**
```bash
rm mytech.db
python app.py
```

This deletes the database and creates a new one with default admin account.

### PostgreSQL (Production)

For production or advanced development:

1. **Install PostgreSQL** from [postgresql.org](https://www.postgresql.org/download/)

2. **Create a database:**
```sql
CREATE DATABASE mytech;
CREATE USER mytech_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mytech TO mytech_user;
```

3. **Update `.env` file:**
```
DATABASE_URL=postgresql://mytech_user:your_password@localhost/mytech
```

4. **Restart the application:**
```bash
python app.py
```

---

## 📁 Project Structure

```
mytech-website/
├── app.py                          # Main Flask application
├── models.py                       # Database models
├── admin_routes.py                # Admin panel routes
├── admin_routes_advanced.py        # Advanced admin features
├── utils.py                        # Utility functions
├── requirements.txt                # Python dependencies
├── README.md                       # Complete documentation
├── Useweb.md                       # This file
├── mytech.db                       # SQLite database (auto-created)
├── .env                            # Environment variables (create locally)
├── static/
│   ├── css/
│   │   ├── style.css              # Main styles with theme colors
│   │   ├── admin.css              # Admin panel styles
│   │   └── loader.css             # Loading animations
│   ├── js/
│   │   ├── theme.js               # Dark/light mode toggle
│   │   └── loader.js              # Loading effects
│   └── uploads/                    # User uploaded files
│       ├── services/
│       ├── projects/
│       ├── blog/
│       ├── team/
│       ├── testimonials/
│       └── resumes/
└── templates/
    ├── base.html                   # Base template
    ├── public/
    │   ├── index.html             # Home page
    │   ├── about.html
    │   ├── services.html
    │   ├── portfolio.html
    │   ├── team.html
    │   ├── blog.html
    │   ├── careers.html
    │   ├── contact.html
    │   ├── technologies.html
    │   ├── testimonials.html
    │   ├── faq.html
    │   └── quote.html
    └── admin/
        ├── base.html
        ├── dashboard.html
        ├── login.html
        ├── settings.html
        ├── profile.html
        ├── services.html
        ├── projects.html
        ├── blogs.html
        ├── team.html
        ├── jobs.html
        ├── messages.html
        ├── view_message.html
        └── [other admin templates...]
```

---

## 🔧 Troubleshooting

### Problem: "Command not found: python"

**Solution:** Python is not installed or not in your PATH
- Download Python from [python.org](https://www.python.org/)
- During installation, check "Add Python to PATH"
- Restart your terminal and try again

### Problem: "No module named 'flask'"

**Solution:** Virtual environment not activated or packages not installed
- Activate virtual environment first:
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

### Problem: Port 5000 already in use

**Solution:** Another application is using port 5000
```bash
# Option 1: Stop the other application
# Option 2: Use a different port
flask run --port 5001
```

### Problem: Database error on first run

**Solution:** Delete and recreate the database
```bash
rm mytech.db
python app.py
```

### Problem: Can't login to admin panel

**Solution:**
- Default username: `Shawaiz` (case-sensitive)
- Default password: `Shawaiz231980079`
- Make sure Caps Lock is off
- Clear browser cache and cookies
- Try a different browser

### Problem: File uploads not working

**Solution:**
- Check file type (PNG, JPG, GIF, WebP)
- Check file size (max 16 MB)
- Make sure `static/uploads/` folder exists
- Create missing folders if needed

### Problem: Email notifications not working

**Solution:**
- Email features require SMTP configuration
- Update `.env` with your email credentials
- Or configure email in Site Settings → Admin

### Problem: Changes not showing on website

**Solution:**
- Refresh the page (Ctrl+R or Cmd+R)
- Hard refresh to clear cache (Ctrl+Shift+R)
- Wait for Flask to restart (watch terminal)
- Check browser console for errors (F12)

---

## 🎨 Customization

### Change Website Colors

Edit `static/css/style.css`:
```css
:root {
    --primary-color: #1F9DFF;  /* Change button color */
    --heading-color: #35C9FF;   /* Change heading color */
    --bg-primary: #0E1A2A;      /* Change background */
    --text-color: #DCE3EC;      /* Change text color */
}
```

### Change Admin Credentials

1. Login to admin panel
2. Go to Profile
3. Change username and password
4. Save

### Add Custom Pages

1. Create HTML file in `templates/public/`
2. Add route in `app.py`
3. Link from navigation menu

### Configure Email Notifications

1. Go to Admin → Site Settings
2. Add email configuration
3. Save

---

## 🚀 Development Tips

### Enable Debug Mode

In `.env`:
```
FLASK_ENV=development
FLASK_DEBUG=True
```

### View Database

**Using SQLite Browser:**
- Download from [sqlitebrowser.org](https://sqlitebrowser.org/)
- Open `mytech.db` file
- Browse tables and data

### Check Application Logs

Logs appear in your terminal while the server is running. Look for:
- Error messages (red text)
- Database warnings (yellow text)
- Request logs (GET/POST requests)

### Test Locally with Phone

1. Find your computer's local IP:
   - Windows: `ipconfig` (look for IPv4)
   - macOS/Linux: `ifconfig` (look for inet)

2. In Flask app, change to:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

3. Access from phone: `http://[YOUR_IP]:5000`

---

## 📦 Deployment

To deploy this website to production:

1. **Using Replit (Recommended):**
   - Push code to Replit
   - Set up PostgreSQL database
   - Configure environment variables
   - Deploy with Replit's publish feature

2. **Using Heroku:**
   - Create Procfile: `web: gunicorn app:app`
   - Install gunicorn: `pip install gunicorn`
   - Deploy to Heroku

3. **Using VPS:**
   - Set up Ubuntu/Debian server
   - Install Python and PostgreSQL
   - Use Nginx as reverse proxy
   - Use Gunicorn as application server

---

## ✅ Quick Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] .env file created with settings
- [ ] Database initialized (mytech.db or PostgreSQL)
- [ ] Flask server running (python app.py)
- [ ] Website accessible at http://localhost:5000
- [ ] Admin panel working at http://localhost:5000/admin/login
- [ ] Default credentials working
- [ ] Password changed for security

---

## 📚 Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- SQLite: https://www.sqlite.org/
- Python: https://www.python.org/doc/

---

## 🆘 Getting Help

1. Check this file for troubleshooting
2. Review README.md for feature documentation
3. Check application terminal for error messages
4. Test in a different browser
5. Clear browser cache and cookies

---

## 🎉 You're Ready!

Your MyTech website is now set up and ready to use locally. Start adding content and customizing to match your brand!

**Happy Building! 🚀**

---

*Last Updated: December 1, 2025*
*MyTech © 2025 - All Rights Reserved*

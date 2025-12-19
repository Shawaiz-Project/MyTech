# MyTech - Company Website with Admin Panel

## Overview
MyTech is a comprehensive company website with a full-featured admin panel for managing all content. The website showcases services, projects, team members, blog posts, and more, with a modern dark/light mode theme.

## Admin Credentials (CHANGE IMMEDIATELY)
- **Username:** Shawaiz
- **Email:** 231980079@gift.edu.pk
- **Default Password:** Shawaiz231980079

**⚠️ SECURITY NOTICE:** Please change this default password immediately after your first login via the Admin Profile page.

## Security Features
- CSRF protection enabled on all forms
- Password hashing using Werkzeug (PBKDF2)
- File uploads validated by extension and saved with randomized UUID filenames
- Login required for all admin routes
- Secure session management with Flask-Login
- DELETE operations require POST method to prevent CSRF attacks

## Project Structure
```
├── app.py                 # Main Flask application
├── admin_routes.py        # Admin panel routes (CRUD operations)
├── models.py              # Database models (SQLAlchemy)
├── static/
│   ├── css/
│   │   ├── style.css      # Main styles with dark/light mode
│   │   └── admin.css      # Admin panel styles
│   ├── js/
│   │   └── theme.js       # Dark/light mode toggle
│   └── uploads/           # User uploaded files
│       ├── services/
│       ├── projects/
│       ├── blog/
│       ├── team/
│       ├── testimonials/
│       └── resumes/
└── templates/
    ├── base.html          # Public base template
    ├── public/            # Public-facing pages
    │   ├── index.html     # Home page
    │   ├── about.html     # About Us
    │   ├── services.html  # Services listing
    │   ├── portfolio.html # Projects/Portfolio
    │   ├── blog.html      # Blog listing
    │   ├── careers.html   # Job listings
    │   ├── contact.html   # Contact form
    │   ├── team.html      # Team members
    │   ├── technologies.html
    │   ├── testimonials.html
    │   ├── faq.html
    │   └── quote.html     # Get a quote form
    └── admin/             # Admin panel templates
        ├── base.html
        ├── dashboard.html
        ├── login.html
        └── [CRUD templates for all content types]
```

## Features Implemented

### Public Website (12 Pages)
1. **Home** - Hero section, services preview, featured projects, testimonials, technologies, CTA
2. **About Us** - Company overview, story, achievements, workflow
3. **Services** - Service listings with detail pages
4. **Portfolio** - Project showcase with category filtering and case studies
5. **Technologies** - Tech stack showcase
6. **Team** - Team members with social links
7. **Careers** - Job listings with application form
8. **Contact** - Contact form with office details
9. **Blog** - Blog posts with detail pages
10. **Testimonials** - Client feedback
11. **FAQ** - Frequently asked questions
12. **Get a Quote** - Quote request form

### Admin Panel Features
- **Dashboard** - Statistics widgets (projects, services, blogs, team, messages, applications)
- **Services Management** - Add, edit, delete services with image upload
- **Projects Management** - Portfolio with multiple image uploads, categories
- **Blog Management** - Rich text content, cover images, tags, draft/published status
- **Team Management** - Team members with profile images and social links
- **Jobs Management** - Job postings with applications tracking
- **Testimonials** - Client feedback with ratings
- **Technologies** - Tech stack management
- **FAQ Management** - Questions and answers
- **Contact Messages** - View, mark as read, delete messages
- **Site Settings** - Website name, SEO, social links, contact info
- **Admin Profile** - Update username, email, password

### Dark/Light Mode Theme
Custom color palettes implemented:

**Dark Mode:**
- Background: Rich Charcoal Blue (#0E1A2A)
- Headings: Aqua Blue (#35C9FF)
- Buttons: Sky Blue (#1F9DFF)
- Text: Ice Gray (#DCE3EC)

**Light Mode:**
- Background: Soft Ice White (#F2F8FD)
- Headings: Aqua Blue (#1BBEFF)
- Buttons: Royal Blue (#146CE8)
- Text: Deep Navy Black (#14202D)

## Technology Stack
- **Backend:** Flask (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF
- **Image Processing:** Pillow
- **Frontend:** HTML5, CSS3, JavaScript
- **Icons:** Font Awesome 6.4.0
- **Fonts:** Inter (Google Fonts)

## Database Models
- Admin (authentication)
- Service
- Project
- Blog
- TeamMember
- Job
- JobApplication
- Testimonial
- Technology
- FAQ
- ContactMessage
- SiteSettings

## Getting Started

1. **Access the website:** Click the webview to see the public website
2. **Admin login:** Navigate to `/admin/login`
3. **Add content:** Use the admin panel to add services, projects, blogs, etc.

## Key URLs
- **Home:** `/`
- **Admin Login:** `/admin/login`
- **Admin Dashboard:** `/admin`
- **Services:** `/services`
- **Portfolio:** `/portfolio`
- **Blog:** `/blog`
- **Contact:** `/contact`
- **Get Quote:** `/quote`

## Recent Changes (November 23, 2025)
- Initial project setup with complete website structure
- Implemented all 12 public pages
- Built comprehensive admin panel with CRUD operations
- Added dark/light mode theme with custom color palettes
- Configured PostgreSQL database
- Created default admin account (MUST be changed immediately)
- Implemented secure file upload functionality with UUID filenames
- Added CSRF protection on all forms
- Changed DELETE operations to POST method for security
- Hardened security across the application

## Notes
- The website uses PostgreSQL instead of MySQL (as MySQL is not available)
- Admin account is automatically created on first run
- File uploads are stored in `static/uploads/` subdirectories
- Theme preference is saved in browser localStorage
- All forms include CSRF protection via Flask-WTF

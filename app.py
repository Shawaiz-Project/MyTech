import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Admin, Service, Project, Blog, TeamMember, Job, JobApplication, Testimonial, Technology, FAQ, ContactMessage, SiteSettings, CustomPage, AnnouncementBar, ActivityLog, Notification, PageAnalytics, TeamEmail
from admin_routes import admin_bp
from admin_routes_advanced import adv_bp
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.register_blueprint(admin_bp)
app.register_blueprint(adv_bp)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')

# Database configuration - Use SQLite fallback if PostgreSQL unavailable
db_url = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://')
if db_url and '?sslmode=' not in db_url:
    db_url += '?sslmode=require'

# Try PostgreSQL first, fallback to SQLite
if db_url and 'postgresql' in db_url:
    try:
        from sqlalchemy import create_engine, text
        test_engine = create_engine(db_url, pool_pre_ping=True)
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        print("✅ Using PostgreSQL database")
    except Exception as e:
        print(f"⚠️ PostgreSQL failed: {str(e)[:60]}... Falling back to SQLite")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mytech.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mytech.db'
    print("ℹ️ Using SQLite database")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True,
    'pool_recycle': 3600,
}
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with app.app_context():
    try:
        db.create_all()
        
        admin = Admin.query.filter_by(username='Shawaiz').first()
        if not admin:
            admin = Admin(
                username='Shawaiz',
                email='231980079@gift.edu.pk'
            )
            admin.set_password('Shawaiz231980079')
            db.session.add(admin)
            db.session.commit()
            print("Admin account created! Please change password immediately after first login.")
        
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings(
                website_name='MyTech',
                seo_title='MyTech - Future-Ready Software Solutions',
                meta_description='MyTech delivers modern, scalable, and efficient digital solutions.',
                contact_email='contact@mytech.com',
                contact_phone='+1 (555) 123-4567',
                footer_text='© 2024 MyTech. All rights reserved.'
            )
            db.session.add(settings)
            db.session.commit()
    except Exception as e:
        print(f"Warning: Database initialization failed - {str(e)}")
        print("The application will continue with limited functionality until database is available.")


def create_notification(title, message, notification_type, related_id=None):
    notification = Notification(
        title=title,
        message=message,
        type=notification_type,
        related_id=related_id
    )
    db.session.add(notification)
    db.session.commit()

def send_contact_email(name, email, phone, subject, message, settings):
    """Send contact message to team members and admins"""
    try:
        SENDER_EMAIL = "almalm7328@gmail.com"
        SENDER_PASSWORD = "htse lefv mggi xnky"
        
        team_emails = TeamEmail.query.filter_by(status='active').all()
        if not team_emails:
            return False
        
        admin_email = Admin.query.first()
        if not admin_email:
            return False
        
        recipient_list = []
        for team in team_emails:
            if settings and settings.forward_to_admins_only:
                if team.role == 'admin':
                    recipient_list.append(team.email)
            else:
                recipient_list.append(team.email)
        
        if admin_email.email not in recipient_list:
            recipient_list.append(admin_email.email)
        
        if not recipient_list:
            return False
        
        for recipient_email in recipient_list:
            msg = MIMEMultipart('alternative')
            msg['From'] = SENDER_EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = f"New Contact Message Received – {settings.website_name if settings else 'MyTech'}"
            
            admin_link = url_for('admin_bp.messages', _external=True)
            
            html = f"""
            <html>
                <body style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
                        <h2 style="color: #1F9DFF; margin-bottom: 20px;">New Contact Message Received</h2>
                        
                        <p style="font-size: 16px; margin-bottom: 20px;">
                            A new contact message has been submitted on <strong>{settings.website_name if settings else 'MyTech'}</strong>.
                        </p>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 6px; margin: 20px 0; border-left: 4px solid #1F9DFF;">
                            <p><strong>Name:</strong> {name}</p>
                            <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                            <p><strong>Phone:</strong> {phone if phone else 'Not provided'}</p>
                            <p><strong>Subject:</strong> {subject if subject else 'No subject'}</p>
                            <p style="margin-top: 15px;"><strong>Message:</strong></p>
                            <p style="white-space: pre-wrap;">{message}</p>
                        </div>
                        
                        <p style="color: #999; font-size: 14px; margin-top: 20px;">
                            <strong>Received At:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
                        </p>
                        
                        <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                            <a href="{admin_link}" style="display: inline-block; background: #1F9DFF; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                                View in Admin Panel
                            </a>
                        </div>
                        
                        <p style="color: #999; font-size: 12px; margin-top: 20px;">
                            Regards,<br/>
                            <strong>MyTech System</strong>
                        </p>
                    </div>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def get_settings():
    """Get site settings with fallback"""
    try:
        return SiteSettings.query.first()
    except Exception:
        return None

def track_page_view(page_name, page_url):
    try:
        analytics = PageAnalytics.query.filter_by(page_url=page_url).first()
        if analytics:
            analytics.views += 1
            analytics.updated_at = datetime.utcnow()
        else:
            analytics = PageAnalytics(page_url=page_url, page_name=page_name, views=1)
            db.session.add(analytics)
        db.session.commit()
    except Exception:
        pass

@app.route('/')
def index():
    try:
        settings = get_settings()
        services = Service.query.filter_by(status='active').limit(6).all()
        projects = Project.query.filter_by(status='active').limit(6).all()
        testimonials = Testimonial.query.limit(5).all()
        technologies = Technology.query.limit(12).all()
        announcements = AnnouncementBar.query.filter_by(is_active=True).all()
        track_page_view('Home', '/')
    except Exception:
        services = []
        projects = []
        testimonials = []
        technologies = []
        announcements = []
        settings = None
    return render_template('public/index.html', settings=settings, services=services, projects=projects, testimonials=testimonials, technologies=technologies, announcements=announcements)

@app.route('/about')
def about():
    try:
        settings = get_settings()
        team = TeamMember.query.all()
    except Exception:
        settings = None
        team = []
    return render_template('public/about.html', settings=settings, team=team)

@app.route('/services')
def services():
    try:
        settings = get_settings()
        all_services = Service.query.filter_by(status='active').all()
    except Exception:
        settings = None
        all_services = []
    return render_template('public/services.html', settings=settings, services=all_services)

@app.route('/services/<int:id>')
def service_detail(id):
    try:
        settings = get_settings()
        service = Service.query.get_or_404(id)
    except Exception:
        return render_template('public/error.html', message='Service not found or database unavailable'), 404
    return render_template('public/service_detail.html', settings=settings, service=service)

@app.route('/portfolio')
def portfolio():
    try:
        settings = get_settings()
        category = request.args.get('category', 'all')
        if category == 'all':
            projects = Project.query.filter_by(status='active').all()
        else:
            projects = Project.query.filter_by(status='active', category=category).all()
    except Exception:
        settings = None
        projects = []
        category = 'all'
    return render_template('public/portfolio.html', settings=settings, projects=projects, selected_category=category)

@app.route('/portfolio/<int:id>')
def project_detail(id):
    try:
        settings = get_settings()
        project = Project.query.get_or_404(id)
    except Exception:
        return render_template('public/error.html', message='Project not found or database unavailable'), 404
    return render_template('public/project_detail.html', settings=settings, project=project)

@app.route('/technologies')
def technologies():
    try:
        settings = get_settings()
        all_technologies = Technology.query.all()
    except Exception:
        settings = None
        all_technologies = []
    return render_template('public/technologies.html', settings=settings, technologies=all_technologies)

@app.route('/team')
def team():
    try:
        settings = get_settings()
        team_members = TeamMember.query.all()
    except Exception:
        settings = None
        team_members = []
    return render_template('public/team.html', settings=settings, team=team_members)

@app.route('/careers')
def careers():
    try:
        settings = get_settings()
        jobs = Job.query.filter_by(status='active').all()
    except Exception:
        settings = None
        jobs = []
    return render_template('public/careers.html', settings=settings, jobs=jobs)

@app.route('/careers/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    try:
        job = Job.query.get_or_404(job_id)
        name = request.form.get('name')
        email = request.form.get('email')
        resume = request.files.get('resume')
        
        if resume and allowed_file(resume.filename):
            ext = resume.filename.rsplit('.', 1)[1].lower()
            import uuid
            filename = f"{uuid.uuid4().hex}.{ext}"
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', filename)
            resume.save(resume_path)
            
            application = JobApplication(
                job_id=job_id,
                name=name,
                email=email,
                resume=filename
            )
            db.session.add(application)
            db.session.commit()
            flash('Application submitted successfully!', 'success')
        else:
            flash('Invalid file format. Please upload a PDF.', 'error')
    except Exception:
        flash('Error submitting application. Please try again.', 'error')
    
    return redirect(url_for('careers'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        settings = get_settings()
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            subject = request.form.get('subject')
            message = request.form.get('message')
            
            contact_msg = ContactMessage(
                name=name, 
                email=email, 
                phone=phone, 
                subject=subject, 
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            
            if settings and settings.auto_forward_messages:
                email_sent = send_contact_email(name, email, phone, subject, message, settings)
                if email_sent:
                    contact_msg.email_forwarded = True
                    db.session.commit()
            
            flash('Message sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
    except Exception:
        settings = None
        flash('Error sending message. Please try again later.', 'error')
    
    return render_template('public/contact.html', settings=settings)

@app.route('/blog')
def blog():
    try:
        settings = get_settings()
        blogs = Blog.query.filter_by(status='published').order_by(Blog.created_at.desc()).all()
    except Exception:
        settings = None
        blogs = []
    return render_template('public/blog.html', settings=settings, blogs=blogs)

@app.route('/blog/<int:id>')
def blog_detail(id):
    try:
        settings = get_settings()
        blog_post = Blog.query.get_or_404(id)
    except Exception:
        return render_template('public/error.html', message='Blog post not found or database unavailable'), 404
    return render_template('public/blog_detail.html', settings=settings, blog=blog_post)

@app.route('/testimonials')
def testimonials():
    try:
        settings = get_settings()
        all_testimonials = Testimonial.query.all()
    except Exception:
        settings = None
        all_testimonials = []
    return render_template('public/testimonials.html', settings=settings, testimonials=all_testimonials)

@app.route('/faq')
def faq():
    try:
        settings = get_settings()
        faqs = FAQ.query.all()
    except Exception:
        settings = None
        faqs = []
    return render_template('public/faq.html', settings=settings, faqs=faqs)

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    try:
        settings = get_settings()
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            service = request.form.get('service')
            budget = request.form.get('budget')
            message_text = f"Quote Request - Service: {service}, Budget: {budget}\n\n{request.form.get('message')}"
            
            message = ContactMessage(name=name, email=email, message=message_text)
            db.session.add(message)
            db.session.commit()
            flash('Quote request submitted successfully!', 'success')
            return redirect(url_for('quote'))
    except Exception:
        settings = None
        flash('Error submitting quote request. Please try again.', 'error')
    
    return render_template('public/quote.html', settings=settings)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            admin = Admin.query.filter_by(username=username).first()
            
            if admin and admin.check_password(password):
                login_user(admin)
                flash('Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password', 'error')
        except Exception as e:
            flash('⚠️ Database is temporarily unavailable. Please try again later or check your database connection.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    try:
        total_projects = Project.query.count()
        total_services = Service.query.count()
        total_team = TeamMember.query.count()
        total_blogs = Blog.query.count()
        unread_messages = ContactMessage.query.filter_by(is_read=False).count()
        total_applications = JobApplication.query.count()
        total_technologies = Technology.query.count()
        total_page_views = db.session.query(db.func.sum(PageAnalytics.views)).scalar() or 0
        
        # Get top pages by views
        top_pages = db.session.query(PageAnalytics.page_name, PageAnalytics.views).order_by(PageAnalytics.views.desc()).limit(6).all()
        page_names = [page[0] or 'Unknown' for page in top_pages]
        page_views = [page[1] for page in top_pages]
    except Exception:
        total_projects = total_services = total_team = total_blogs = 0
        unread_messages = total_applications = total_technologies = 0
        total_page_views = 0
        page_names = ['Home', 'Projects', 'Services', 'Blog', 'Team', 'Contact']
        page_views = [0, 0, 0, 0, 0, 0]
    
    # Fill in default pages if not enough data
    default_pages = ['Home', 'Projects', 'Services', 'Blog', 'Team', 'Contact']
    if len(page_names) < 6:
        for i, page in enumerate(default_pages):
            if page not in page_names:
                page_names.append(page)
                page_views.append(0)
            if len(page_names) >= 6:
                break
    
    page_names = page_names[:6]
    page_views = page_views[:6]
    
    import json
    
    return render_template('admin/dashboard.html', 
                         total_projects=total_projects,
                         total_services=total_services,
                         total_team=total_team,
                         total_blogs=total_blogs,
                         unread_messages=unread_messages,
                         total_applications=total_applications,
                         total_technologies=total_technologies,
                         total_page_views=total_page_views,
                         page_names=json.dumps(page_names),
                         page_views=json.dumps(page_views))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Global error handlers for database connectivity
from sqlalchemy.exc import OperationalError

@app.errorhandler(OperationalError)
def handle_db_error(e):
    flash('Database connection error. Please try again later.', 'error')
    return redirect(url_for('index')), 500

@app.errorhandler(Exception)
def handle_general_error(e):
    if 'endpoint has been disabled' in str(e):
        flash('Database service temporarily unavailable. Please try again later.', 'error')
        return redirect(url_for('index')), 503
    return str(e), 500

# Favicon handler
@app.route('/favicon.ico')
def favicon():
    return '', 204

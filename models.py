from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), default='default-admin.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.Text)
    detailed_description = db.Column(db.Text)
    icon = db.Column(db.String(255))
    technologies = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(100))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    features = db.Column(db.Text)
    technologies = db.Column(db.Text)
    images = db.Column(db.Text)
    project_link = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    cover_image = db.Column(db.String(255))
    content = db.Column(db.Text)
    tags = db.Column(db.String(255))
    status = db.Column(db.String(20), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    skills = db.Column(db.Text)
    profile_image = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    job_type = db.Column(db.String(50))
    requirements = db.Column(db.Text)
    responsibilities = db.Column(db.Text)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    resume = db.Column(db.String(255))
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    job = db.relationship('Job', backref='applications')

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer, default=5)
    client_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Technology(db.Model):
    __tablename__ = 'technologies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    icon = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FAQ(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    email_forwarded = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeamEmail(db.Model):
    __tablename__ = 'team_emails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(20), default='team')
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    website_name = db.Column(db.String(100), default='MyTech')
    logo = db.Column(db.String(255))
    favicon = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    footer_text = db.Column(db.Text)
    seo_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(50))
    primary_color = db.Column(db.String(7), default='#1F9DFF')
    secondary_color = db.Column(db.String(7), default='#35C9FF')
    border_radius = db.Column(db.String(10), default='8px')
    font_family = db.Column(db.String(100), default='Inter')
    auto_forward_messages = db.Column(db.Boolean, default=True)
    forward_to_admins_only = db.Column(db.Boolean, default=False)
    whatsapp_enabled = db.Column(db.Boolean, default=True)
    whatsapp_number = db.Column(db.String(20), default='+1234567890')
    whatsapp_message = db.Column(db.Text, default='Hello! I would like to know more about your services.')
    whatsapp_position = db.Column(db.String(20), default='right')
    whatsapp_icon_size = db.Column(db.String(10), default='60px')
    hero_title = db.Column(db.String(255), default='We Build Future-Ready Software Solutions')
    hero_subtitle = db.Column(db.Text, default='MyTech delivers modern, scalable, and efficient digital solutions that transform your business and accelerate growth.')
    hero_cta_text = db.Column(db.String(100), default='Get a Quote')
    hero_cta_url = db.Column(db.String(255), default='/quote')
    hero_secondary_cta_text = db.Column(db.String(100), default='Explore Services')
    hero_secondary_cta_url = db.Column(db.String(255), default='/services')
    hero_background_image = db.Column(db.String(255))

class CustomPage(db.Model):
    __tablename__ = 'custom_pages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text)
    seo_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    status = db.Column(db.String(20), default='published')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnnouncementBar(db.Model):
    __tablename__ = 'announcement_bars'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    type = db.Column(db.String(20), default='info')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    action = db.Column(db.String(200))
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.relationship('Admin', backref='activity_logs')

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    type = db.Column(db.String(50))
    is_read = db.Column(db.Boolean, default=False)
    related_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PageAnalytics(db.Model):
    __tablename__ = 'page_analytics'
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(255))
    page_name = db.Column(db.String(100))
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Service, Project, Blog, TeamMember, Job, JobApplication, Testimonial, Technology, FAQ, ContactMessage, SiteSettings, Admin, TeamEmail
import os
import uuid
from utils import log_activity

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_DOCS = {'pdf', 'doc', 'docx'}

def allowed_file(filename, file_type='image'):
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if file_type == 'image':
            return ext in ALLOWED_EXTENSIONS
        elif file_type == 'doc':
            return ext in ALLOWED_DOCS
    return False

def save_file(file, folder):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join('static/uploads', folder, filename)
        file.save(filepath)
        return filename
    return None

@admin_bp.route('/services')
@login_required
def services():
    all_services = Service.query.all()
    return render_template('admin/services.html', services=all_services)

@admin_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        title = request.form.get('title')
        short_description = request.form.get('short_description')
        detailed_description = request.form.get('detailed_description')
        technologies = request.form.get('technologies')
        status = request.form.get('status', 'active')
        icon = request.files.get('icon')
        
        icon_filename = save_file(icon, 'services')
        
        service = Service(
            title=title,
            short_description=short_description,
            detailed_description=detailed_description,
            technologies=technologies,
            status=status,
            icon=icon_filename
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin_bp.services'))
    
    return render_template('admin/service_form.html', service=None)

@admin_bp.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.title = request.form.get('title')
        service.short_description = request.form.get('short_description')
        service.detailed_description = request.form.get('detailed_description')
        service.technologies = request.form.get('technologies')
        service.status = request.form.get('status', 'active')
        
        icon = request.files.get('icon')
        icon_filename = save_file(icon, 'services')
        if icon_filename:
            service.icon = icon_filename
        
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin_bp.services'))
    
    return render_template('admin/service_form.html', service=service)

@admin_bp.route('/services/delete/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_bp.services'))

@admin_bp.route('/projects')
@login_required
def projects():
    all_projects = Project.query.all()
    return render_template('admin/projects.html', projects=all_projects)

@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        client = request.form.get('client')
        category = request.form.get('category')
        description = request.form.get('description')
        features = request.form.get('features')
        technologies = request.form.get('technologies')
        project_link = request.form.get('project_link')
        status = request.form.get('status', 'active')
        
        images = request.files.getlist('images')
        image_filenames = []
        for img in images:
            filename = save_file(img, 'projects')
            if filename:
                image_filenames.append(filename)
        
        project = Project(
            title=title,
            client=client,
            category=category,
            description=description,
            features=features,
            technologies=technologies,
            project_link=project_link,
            status=status,
            images=','.join(image_filenames) if image_filenames else None
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin_bp.projects'))
    
    return render_template('admin/project_form.html', project=None)

@admin_bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.client = request.form.get('client')
        project.category = request.form.get('category')
        project.description = request.form.get('description')
        project.features = request.form.get('features')
        project.technologies = request.form.get('technologies')
        project.project_link = request.form.get('project_link')
        project.status = request.form.get('status', 'active')
        
        images = request.files.getlist('images')
        if images and images[0].filename:
            image_filenames = []
            for img in images:
                filename = save_file(img, 'projects')
                if filename:
                    image_filenames.append(filename)
            if image_filenames:
                project.images = ','.join(image_filenames)
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_bp.projects'))
    
    return render_template('admin/project_form.html', project=project)

@admin_bp.route('/projects/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_bp.projects'))

@admin_bp.route('/blogs')
@login_required
def blogs():
    all_blogs = Blog.query.all()
    return render_template('admin/blogs.html', blogs=all_blogs)

@admin_bp.route('/blogs/add', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        status = request.form.get('status', 'draft')
        
        cover_image = request.files.get('cover_image')
        cover_filename = save_file(cover_image, 'blog')
        
        blog = Blog(
            title=title,
            content=content,
            tags=tags,
            status=status,
            cover_image=cover_filename
        )
        db.session.add(blog)
        db.session.commit()
        flash('Blog post added successfully!', 'success')
        return redirect(url_for('admin_bp.blogs'))
    
    return render_template('admin/blog_form.html', blog=None)

@admin_bp.route('/blogs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    
    if request.method == 'POST':
        blog.title = request.form.get('title')
        blog.content = request.form.get('content')
        blog.tags = request.form.get('tags')
        blog.status = request.form.get('status', 'draft')
        
        cover_image = request.files.get('cover_image')
        cover_filename = save_file(cover_image, 'blog')
        if cover_filename:
            blog.cover_image = cover_filename
        
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin_bp.blogs'))
    
    return render_template('admin/blog_form.html', blog=blog)

@admin_bp.route('/blogs/delete/<int:id>', methods=['POST'])
@login_required
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin_bp.blogs'))

@admin_bp.route('/team')
@login_required
def team():
    team_members = TeamMember.query.all()
    return render_template('admin/team.html', team=team_members)

@admin_bp.route('/team/add', methods=['GET', 'POST'])
@login_required
def add_team():
    if request.method == 'POST':
        name = request.form.get('name')
        designation = request.form.get('designation')
        skills = request.form.get('skills')
        linkedin = request.form.get('linkedin')
        github = request.form.get('github')
        twitter = request.form.get('twitter')
        
        profile_image = request.files.get('profile_image')
        image_filename = save_file(profile_image, 'team')
        
        member = TeamMember(
            name=name,
            designation=designation,
            skills=skills,
            linkedin=linkedin,
            github=github,
            twitter=twitter,
            profile_image=image_filename
        )
        db.session.add(member)
        db.session.commit()
        flash('Team member added successfully!', 'success')
        return redirect(url_for('admin_bp.team'))
    
    return render_template('admin/team_form.html', member=None)

@admin_bp.route('/team/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    member = TeamMember.query.get_or_404(id)
    
    if request.method == 'POST':
        member.name = request.form.get('name')
        member.designation = request.form.get('designation')
        member.skills = request.form.get('skills')
        member.linkedin = request.form.get('linkedin')
        member.github = request.form.get('github')
        member.twitter = request.form.get('twitter')
        
        profile_image = request.files.get('profile_image')
        image_filename = save_file(profile_image, 'team')
        if image_filename:
            member.profile_image = image_filename
        
        db.session.commit()
        flash('Team member updated successfully!', 'success')
        return redirect(url_for('admin_bp.team'))
    
    return render_template('admin/team_form.html', member=member)

@admin_bp.route('/team/delete/<int:id>', methods=['POST'])
@login_required
def delete_team(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Team member deleted successfully!', 'success')
    return redirect(url_for('admin_bp.team'))

@admin_bp.route('/jobs')
@login_required
def jobs():
    all_jobs = Job.query.all()
    return render_template('admin/jobs.html', jobs=all_jobs)

@admin_bp.route('/jobs/add', methods=['GET', 'POST'])
@login_required
def add_job():
    if request.method == 'POST':
        title = request.form.get('title')
        job_type = request.form.get('job_type')
        requirements = request.form.get('requirements')
        responsibilities = request.form.get('responsibilities')
        description = request.form.get('description')
        status = request.form.get('status', 'active')
        
        job = Job(
            title=title,
            job_type=job_type,
            requirements=requirements,
            responsibilities=responsibilities,
            description=description,
            status=status
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('admin_bp.jobs'))
    
    return render_template('admin/job_form.html', job=None)

@admin_bp.route('/jobs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    job = Job.query.get_or_404(id)
    
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.job_type = request.form.get('job_type')
        job.requirements = request.form.get('requirements')
        job.responsibilities = request.form.get('responsibilities')
        job.description = request.form.get('description')
        job.status = request.form.get('status', 'active')
        
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('admin_bp.jobs'))
    
    return render_template('admin/job_form.html', job=job)

@admin_bp.route('/jobs/delete/<int:id>', methods=['POST'])
@login_required
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('admin_bp.jobs'))

@admin_bp.route('/applications')
@login_required
def applications():
    all_applications = JobApplication.query.all()
    return render_template('admin/applications.html', applications=all_applications)

@admin_bp.route('/applications/delete/<int:id>', methods=['POST'])
@login_required
def delete_application(id):
    application = JobApplication.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('admin_bp.applications'))

@admin_bp.route('/testimonials')
@login_required
def testimonials():
    all_testimonials = Testimonial.query.all()
    return render_template('admin/testimonials.html', testimonials=all_testimonials)

@admin_bp.route('/testimonials/add', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    if request.method == 'POST':
        client_name = request.form.get('client_name')
        feedback = request.form.get('feedback')
        rating = request.form.get('rating', 5)
        
        client_image = request.files.get('client_image')
        image_filename = save_file(client_image, 'testimonials')
        
        testimonial = Testimonial(
            client_name=client_name,
            feedback=feedback,
            rating=rating,
            client_image=image_filename
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('admin_bp.testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=None)

@admin_bp.route('/testimonials/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    
    if request.method == 'POST':
        testimonial.client_name = request.form.get('client_name')
        testimonial.feedback = request.form.get('feedback')
        testimonial.rating = request.form.get('rating', 5)
        
        client_image = request.files.get('client_image')
        image_filename = save_file(client_image, 'testimonials')
        if image_filename:
            testimonial.client_image = image_filename
        
        db.session.commit()
        flash('Testimonial updated successfully!', 'success')
        return redirect(url_for('admin_bp.testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=testimonial)

@admin_bp.route('/testimonials/delete/<int:id>', methods=['POST'])
@login_required
def delete_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Testimonial deleted successfully!', 'success')
    return redirect(url_for('admin_bp.testimonials'))

@admin_bp.route('/technologies')
@login_required
def technologies():
    all_technologies = Technology.query.all()
    return render_template('admin/technologies.html', technologies=all_technologies)

@admin_bp.route('/technologies/add', methods=['GET', 'POST'])
@login_required
def add_technology():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        icon = request.form.get('icon')
        
        technology = Technology(
            name=name,
            category=category,
            description=description,
            icon=icon
        )
        db.session.add(technology)
        db.session.commit()
        flash('Technology added successfully!', 'success')
        return redirect(url_for('admin_bp.technologies'))
    
    return render_template('admin/technology_form.html', technology=None)

@admin_bp.route('/technologies/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_technology(id):
    technology = Technology.query.get_or_404(id)
    
    if request.method == 'POST':
        technology.name = request.form.get('name')
        technology.category = request.form.get('category')
        technology.description = request.form.get('description')
        technology.icon = request.form.get('icon')
        
        db.session.commit()
        flash('Technology updated successfully!', 'success')
        return redirect(url_for('admin_bp.technologies'))
    
    return render_template('admin/technology_form.html', technology=technology)

@admin_bp.route('/technologies/delete/<int:id>', methods=['POST'])
@login_required
def delete_technology(id):
    technology = Technology.query.get_or_404(id)
    db.session.delete(technology)
    db.session.commit()
    flash('Technology deleted successfully!', 'success')
    return redirect(url_for('admin_bp.technologies'))

@admin_bp.route('/faqs')
@login_required
def faqs():
    all_faqs = FAQ.query.all()
    return render_template('admin/faqs.html', faqs=all_faqs)

@admin_bp.route('/faqs/add', methods=['GET', 'POST'])
@login_required
def add_faq():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        
        faq = FAQ(question=question, answer=answer)
        db.session.add(faq)
        db.session.commit()
        flash('FAQ added successfully!', 'success')
        return redirect(url_for('admin_bp.faqs'))
    
    return render_template('admin/faq_form.html', faq=None)

@admin_bp.route('/faqs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_faq(id):
    faq = FAQ.query.get_or_404(id)
    
    if request.method == 'POST':
        faq.question = request.form.get('question')
        faq.answer = request.form.get('answer')
        
        db.session.commit()
        flash('FAQ updated successfully!', 'success')
        return redirect(url_for('admin_bp.faqs'))
    
    return render_template('admin/faq_form.html', faq=faq)

@admin_bp.route('/faqs/delete/<int:id>', methods=['POST'])
@login_required
def delete_faq(id):
    faq = FAQ.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash('FAQ deleted successfully!', 'success')
    return redirect(url_for('admin_bp.faqs'))

@admin_bp.route('/messages')
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_messages)

@admin_bp.route('/messages/mark-read/<int:id>')
@login_required
def mark_read(id):
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    flash('Message marked as read!', 'success')
    return redirect(url_for('admin_bp.messages'))

@admin_bp.route('/messages/view/<int:id>')
@login_required
def view_message(id):
    message = ContactMessage.query.get_or_404(id)
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    return render_template('admin/view_message.html', message=message)

@admin_bp.route('/messages/delete/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin_bp.messages'))

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    site_settings = SiteSettings.query.first()
    
    if request.method == 'POST':
        site_settings.website_name = request.form.get('website_name')
        site_settings.seo_title = request.form.get('seo_title')
        site_settings.meta_description = request.form.get('meta_description')
        site_settings.contact_email = request.form.get('contact_email')
        site_settings.contact_phone = request.form.get('contact_phone')
        site_settings.facebook = request.form.get('facebook')
        site_settings.linkedin = request.form.get('linkedin')
        site_settings.instagram = request.form.get('instagram')
        site_settings.twitter = request.form.get('twitter')
        site_settings.footer_text = request.form.get('footer_text')
        site_settings.whatsapp_enabled = request.form.get('whatsapp_enabled') == 'on'
        site_settings.whatsapp_number = request.form.get('whatsapp_number', '+1234567890')
        site_settings.whatsapp_message = request.form.get('whatsapp_message', 'Hello! I would like to know more about your services.')
        site_settings.whatsapp_position = request.form.get('whatsapp_position', 'right')
        site_settings.whatsapp_icon_size = request.form.get('whatsapp_icon_size', '60px')
        site_settings.hero_title = request.form.get('hero_title', 'We Build Future-Ready Software Solutions')
        site_settings.hero_subtitle = request.form.get('hero_subtitle', 'MyTech delivers modern, scalable, and efficient digital solutions that transform your business and accelerate growth.')
        site_settings.hero_cta_text = request.form.get('hero_cta_text', 'Get a Quote')
        site_settings.hero_cta_url = request.form.get('hero_cta_url', '/quote')
        site_settings.hero_secondary_cta_text = request.form.get('hero_secondary_cta_text', 'Explore Services')
        site_settings.hero_secondary_cta_url = request.form.get('hero_secondary_cta_url', '/services')
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_bp.settings'))
    
    return render_template('admin/settings.html', settings=site_settings)

@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_bp.profile'))
    
    return render_template('admin/profile.html')

# Team Email Management Routes
@admin_bp.route('/team-emails', methods=['GET', 'POST'])
@login_required
def team_emails():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role', 'team')
        
        existing = TeamEmail.query.filter_by(email=email).first()
        if existing:
            flash('Email already exists!', 'danger')
            return redirect(url_for('admin_bp.team_emails'))
        
        team_email = TeamEmail(name=name, email=email, role=role, status='active')
        db.session.add(team_email)
        db.session.commit()
        log_activity('add', 'TeamEmail', team_email.id)
        flash('Team email added successfully!', 'success')
        return redirect(url_for('admin_bp.team_emails'))
    
    team_emails = TeamEmail.query.all()
    return render_template('admin/team_emails.html', team_emails=team_emails)

@admin_bp.route('/team-emails/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team_email(id):
    team_email = TeamEmail.query.get_or_404(id)
    
    if request.method == 'POST':
        team_email.name = request.form.get('name')
        team_email.email = request.form.get('email')
        team_email.role = request.form.get('role')
        team_email.status = request.form.get('status', 'active')
        db.session.commit()
        log_activity('edit', 'TeamEmail', id)
        flash('Team email updated successfully!', 'success')
        return redirect(url_for('admin_bp.team_emails'))
    
    return render_template('admin/edit_team_email.html', team_email=team_email)

@admin_bp.route('/team-emails/<int:id>/delete', methods=['POST'])
@login_required
def delete_team_email(id):
    team_email = TeamEmail.query.get_or_404(id)
    db.session.delete(team_email)
    db.session.commit()
    log_activity('delete', 'TeamEmail', id)
    flash('Team email deleted successfully!', 'success')
    return redirect(url_for('admin_bp.team_emails'))

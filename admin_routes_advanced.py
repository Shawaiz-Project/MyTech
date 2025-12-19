from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, CustomPage, AnnouncementBar, ActivityLog, Notification, PageAnalytics
import uuid

adv_bp = Blueprint('adv_bp', __name__, url_prefix='/admin')

@adv_bp.route('/pages')
@login_required
def pages():
    all_pages = CustomPage.query.all()
    return render_template('admin/pages.html', pages=all_pages)

@adv_bp.route('/pages/add', methods=['GET', 'POST'])
@login_required
def add_page():
    if request.method == 'POST':
        title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        seo_title = request.form.get('seo_title')
        meta_description = request.form.get('meta_description')
        status = request.form.get('status', 'published')
        
        page = CustomPage(
            title=title, slug=slug, content=content,
            seo_title=seo_title, meta_description=meta_description, status=status
        )
        db.session.add(page)
        db.session.commit()
        flash('Page created successfully!', 'success')
        return redirect(url_for('adv_bp.pages'))
    return render_template('admin/page_form.html', page=None)

@adv_bp.route('/pages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_page(id):
    page = CustomPage.query.get_or_404(id)
    if request.method == 'POST':
        page.title = request.form.get('title')
        page.slug = request.form.get('slug')
        page.content = request.form.get('content')
        page.seo_title = request.form.get('seo_title')
        page.meta_description = request.form.get('meta_description')
        page.status = request.form.get('status', 'published')
        db.session.commit()
        flash('Page updated successfully!', 'success')
        return redirect(url_for('adv_bp.pages'))
    return render_template('admin/page_form.html', page=page)

@adv_bp.route('/pages/delete/<int:id>', methods=['POST'])
@login_required
def delete_page(id):
    page = CustomPage.query.get_or_404(id)
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted successfully!', 'success')
    return redirect(url_for('adv_bp.pages'))

@adv_bp.route('/announcements')
@login_required
def announcements():
    all_announcements = AnnouncementBar.query.all()
    return render_template('admin/announcements.html', announcements=all_announcements)

@adv_bp.route('/announcements/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        announcement_type = request.form.get('type', 'info')
        is_active = request.form.get('is_active') == 'on'
        
        announcement = AnnouncementBar(
            title=title, message=message, type=announcement_type, is_active=is_active
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('adv_bp.announcements'))
    return render_template('admin/announcement_form.html', announcement=None)

@adv_bp.route('/announcements/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    announcement = AnnouncementBar.query.get_or_404(id)
    if request.method == 'POST':
        announcement.title = request.form.get('title')
        announcement.message = request.form.get('message')
        announcement.type = request.form.get('type', 'info')
        announcement.is_active = request.form.get('is_active') == 'on'
        db.session.commit()
        flash('Announcement updated successfully!', 'success')
        return redirect(url_for('adv_bp.announcements'))
    return render_template('admin/announcement_form.html', announcement=announcement)

@adv_bp.route('/announcements/delete/<int:id>', methods=['POST'])
@login_required
def delete_announcement(id):
    announcement = AnnouncementBar.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted successfully!', 'success')
    return redirect(url_for('adv_bp.announcements'))

@adv_bp.route('/notifications')
@login_required
def notifications():
    all_notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    unread_count = Notification.query.filter_by(is_read=False).count()
    return render_template('admin/notifications.html', notifications=all_notifications, unread_count=unread_count)

@adv_bp.route('/notifications/mark-read/<int:id>')
@login_required
def mark_notification_read(id):
    notification = Notification.query.get_or_404(id)
    notification.is_read = True
    db.session.commit()
    return redirect(url_for('adv_bp.notifications'))

@adv_bp.route('/notifications/delete/<int:id>', methods=['POST'])
@login_required
def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    flash('Notification deleted successfully!', 'success')
    return redirect(url_for('adv_bp.notifications'))

@adv_bp.route('/analytics')
@login_required
def analytics():
    page_stats = PageAnalytics.query.order_by(PageAnalytics.views.desc()).all()
    total_views = sum(stat.views for stat in page_stats)
    return render_template('admin/analytics.html', page_stats=page_stats, total_views=total_views)

@adv_bp.route('/activity-logs')
@login_required
def activity_logs():
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(500).all()
    return render_template('admin/activity_logs.html', logs=logs)

@adv_bp.route('/theme-settings', methods=['GET', 'POST'])
@login_required
def theme_settings():
    from models import SiteSettings
    settings = SiteSettings.query.first()
    if request.method == 'POST':
        settings.primary_color = request.form.get('primary_color', settings.primary_color)
        settings.secondary_color = request.form.get('secondary_color', settings.secondary_color)
        settings.border_radius = request.form.get('border_radius', settings.border_radius)
        settings.font_family = request.form.get('font_family', settings.font_family)
        db.session.commit()
        flash('Theme updated successfully!', 'success')
        return redirect(url_for('adv_bp.theme_settings'))
    return render_template('admin/theme_settings.html', settings=settings)

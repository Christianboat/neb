from flask import Blueprint, render_template, redirect, url_for, flash, session, request, abort
from urllib.parse import urlparse
from app.models import User, Page, Section, Program, TeamMember, Partnership, NewsArticle, Testimonial, ImpactMetric, ContactInfo, SocialMedia, ContentItem, SiteSettings, Sponsor, ProgramSubContent, SponsorshipTier, GalleryItem, Inquiry
from app.forms import LoginForm, PageForm, SectionForm, ItemForm, ImpactMetricForm, SiteSettingsForm, SponsorForm, ContactInfoForm, SocialMediaForm, ProgramForm, ProgramSubContentForm, PartnershipForm, SponsorshipTierForm, TeamMemberForm, NewsArticleForm, TestimonialForm, GalleryItemForm
from app.utils import save_picture, slugify
from app import db, limiter
from functools import wraps

admin_bp = Blueprint('admin', __name__)


@admin_bp.context_processor
def inject_admin_globals():
    """Real new-inquiry count for the top bar (replaces the old fake badge)."""
    count = 0
    if session.get('logged_in'):
        count = Inquiry.query.filter_by(status='New').count()
    return {'new_inquiry_count': count}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def is_safe_url(target):
    """Only allow redirects to relative paths on this host (prevents open
    redirect via the ?next= parameter)."""
    if not target:
        return False
    ref = urlparse(request.host_url)
    test = urlparse(target)
    return test.scheme in ('', 'http', 'https') and (
        test.netloc == '' or ref.netloc == test.netloc)

@admin_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('10 per minute; 50 per hour', methods=['POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['logged_in'] = True
            session['user_id'] = user.id
            session.permanent = True
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'pages': Page.query.count(),
        'programs': Program.query.count(),
        'partnerships': Partnership.query.count(),
        'team': TeamMember.query.count(),
        'sponsors': Sponsor.query.count(),
        'inquiries': Inquiry.query.filter_by(status='New').count()
    }
    recent_news = NewsArticle.query.order_by(NewsArticle.date_published.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_news=recent_news)

# --- PAGES ---
@admin_bp.route('/pages')
@login_required
def list_pages():
    pages = Page.query.all()
    return render_template('admin/pages_list.html', pages=pages)

@admin_bp.route('/pages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_page(id):
    page = Page.query.get_or_404(id)
    form = PageForm(obj=page)
    if form.validate_on_submit():
        form.populate_obj(page)
        db.session.commit()
        flash('Page updated.', 'success')
        return redirect(url_for('admin.list_pages'))
    sections = page.sections.order_by(Section.order.asc()).all()
    return render_template('admin/page_edit.html', form=form, page=page, sections=sections)

# --- SECTIONS ---
@admin_bp.route('/pages/<int:page_id>/sections')
@login_required
def list_sections(page_id):
    page = Page.query.get_or_404(page_id)
    sections = page.sections.order_by(Section.order).all()
    return render_template('admin/sections_list.html', page=page, sections=sections)

@admin_bp.route('/pages/<int:page_id>/sections/new', methods=['GET', 'POST'])
@login_required
def create_section(page_id):
    page = Page.query.get_or_404(page_id)
    form = SectionForm()
    if form.validate_on_submit():
        section = Section(page_id=page.id)
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='sections')
            section.image_filename = picture_file
        form.populate_obj(section)
        db.session.add(section)
        db.session.commit()
        flash('Section created.', 'success')
        return redirect(url_for('admin.edit_page', id=page.id))
    return render_template('admin/section_edit.html', form=form, legend=f"Add Section to {page.slug}")

@admin_bp.route('/sections/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_section(id):
    section = Section.query.get_or_404(id)
    form = SectionForm(obj=section)
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='sections')
            section.image_filename = picture_file
        
        # Explicitly save video_url to ensure it persist
        section.video_url = form.video_url.data
        
        form.populate_obj(section)
        db.session.commit()
        flash('Section updated.', 'success')
        return redirect(url_for('admin.edit_page', id=section.page_id))
    return render_template('admin/section_edit.html', form=form, section=section, legend="Edit Section")

@admin_bp.route('/sections/<int:id>/delete', methods=['POST'])
@login_required
def delete_section(id):
    section = Section.query.get_or_404(id)
    page_id = section.page_id
    db.session.delete(section)
    db.session.commit()
    flash('Section deleted.', 'success')
    return redirect(url_for('admin.edit_page', id=page_id))

# --- ITEMS ---
@admin_bp.route('/sections/<int:section_id>/items')
@login_required
def list_items(section_id):
    section = Section.query.get_or_404(section_id)
    items = section.items.order_by(ContentItem.order).all()
    return render_template('admin/items_list.html', section=section, items=items)

@admin_bp.route('/sections/<int:section_id>/items/new', methods=['GET', 'POST'])
@login_required
def create_item(section_id):
    section = Section.query.get_or_404(section_id)
    form = ItemForm()
    if form.validate_on_submit():
        item = ContentItem(section_id=section.id)
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='items')
            item.image_filename = picture_file
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Item created.', 'success')
        return redirect(url_for('admin.list_items', section_id=section.id))
    return render_template('admin/item_edit.html', form=form, legend=f"Add Item to {section.section_key}")

@admin_bp.route('/items/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    item = ContentItem.query.get_or_404(id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='items')
            item.image_filename = picture_file
        form.populate_obj(item)
        db.session.commit()
        flash('Item updated.', 'success')
        return redirect(url_for('admin.list_items', section_id=item.section_id))
    return render_template('admin/item_edit.html', form=form, item=item, legend="Edit Item")

@admin_bp.route('/items/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item = ContentItem.query.get_or_404(id)
    section_id = item.section_id
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted.', 'success')
    return redirect(url_for('admin.list_items', section_id=section_id))

# --- IMPACT METRICS ---
@admin_bp.route('/metrics')
@login_required
def list_metrics():
    metrics = ImpactMetric.query.order_by(ImpactMetric.order).all()
    return render_template('admin/metrics_list.html', metrics=metrics)

@admin_bp.route('/metrics/new', methods=['GET', 'POST'])
@login_required
def create_metric():
    form = ImpactMetricForm()
    if form.validate_on_submit():
        metric = ImpactMetric()
        form.populate_obj(metric)
        db.session.add(metric)
        db.session.commit()
        flash('Metric created.', 'success')
        return redirect(url_for('admin.list_metrics'))
    return render_template('admin/metric_edit.html', form=form)

@admin_bp.route('/metrics/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_metric(id):
    metric = ImpactMetric.query.get_or_404(id)
    form = ImpactMetricForm(obj=metric)
    if form.validate_on_submit():
        form.populate_obj(metric)
        db.session.commit()
        flash('Metric updated.', 'success')
        return redirect(url_for('admin.list_metrics'))
    return render_template('admin/metric_edit.html', form=form)

@admin_bp.route('/metrics/<int:id>/delete', methods=['POST'])
@login_required
def delete_metric(id):
    metric = ImpactMetric.query.get_or_404(id)
    db.session.delete(metric)
    db.session.commit()
    flash('Metric deleted.', 'success')
    return redirect(url_for('admin.list_metrics'))

# Home Highlights (Flagship Programs) Management

# Program Catalog Management
@admin_bp.route('/programs')
@login_required
def list_programs():
    programs = Program.query.order_by(Program.order.asc()).all()
    return render_template('admin/programs_list.html', programs=programs)

@admin_bp.route('/programs/new', methods=['GET', 'POST'])
@login_required
def create_program():
    form = ProgramForm()
    if form.validate_on_submit():
        program = Program()
        if form.image.data:
            picture_file = save_picture(form.image.data, folder='programs')
            program.image_filename = picture_file
        
        # Auto-slug if blank
        if not form.slug.data:
            form.slug.data = slugify(form.name.data)
            
        form.populate_obj(program)
        db.session.add(program)
        db.session.commit()
        flash('Program created.', 'success')
        return redirect(url_for('admin.list_programs'))
    
    if form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('admin/program_edit.html', form=form, legend="Create Program")

@admin_bp.route('/programs/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_program(id):
    program = Program.query.get_or_404(id)
    form = ProgramForm(obj=program, original_slug=program.slug)
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data, folder='programs')
            program.image_filename = picture_file
        
        form.populate_obj(program)
        db.session.commit()
        flash('Program updated.', 'success')
        return redirect(url_for('admin.list_programs'))
    
    if form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    
    # Get subcontents to show in the edit page (simplified inline)
    subcontents = program.subcontents.order_by(ProgramSubContent.order.asc()).all()
    return render_template('admin/program_edit.html', form=form, program=program, subcontents=subcontents, legend="Edit Program")

@admin_bp.route('/programs/<int:id>/delete', methods=['POST'])
@login_required
def delete_program(id):
    program = Program.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    flash('Program deleted.', 'success')
    return redirect(url_for('admin.list_programs'))

# Program SubContent Management
@admin_bp.route('/programs/<int:program_id>/subcontents')
@login_required
def list_program_subcontents(program_id):
    program = Program.query.get_or_404(program_id)
    subcontents = program.subcontents.order_by(ProgramSubContent.order.asc()).all()
    return render_template('admin/subcontents_list.html', program=program, subcontents=subcontents)

@admin_bp.route('/programs/<int:program_id>/subcontents/new', methods=['GET', 'POST'])
@login_required
def create_program_subcontent(program_id):
    parent = Program.query.get_or_404(program_id)
    redirect_url = url_for('admin.edit_program', id=program_id)
    legend = f"Add Subcontent to Program: {parent.name}"
        
    form = ProgramSubContentForm()
    if form.validate_on_submit():
        subcontent = ProgramSubContent(program_id=parent.id)
        form.populate_obj(subcontent)
        db.session.add(subcontent)
        db.session.commit()
        flash('Subcontent added successfully.', 'success')
        return redirect(redirect_url)
    
    if form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                
    return render_template('admin/subcontent_edit.html', form=form, parent=parent, cancel_url=redirect_url, legend=legend)

@admin_bp.route('/subcontents/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_program_subcontent(id):
    subcontent = ProgramSubContent.query.get_or_404(id)
    form = ProgramSubContentForm(obj=subcontent)
    
    # Determine the parent to redirect back to
    parent_name = subcontent.program.name
    redirect_url = url_for('admin.edit_program', id=subcontent.program_id)

    if form.validate_on_submit():
        form.populate_obj(subcontent)
        db.session.commit()
        flash('Subcontent updated successfully.', 'success')
        return redirect(redirect_url)
    
    if form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('admin/subcontent_edit.html', form=form, cancel_url=redirect_url, legend=f"Edit Subcontent for {parent_name}")

@admin_bp.route('/subcontents/<int:id>/delete', methods=['POST'])
@login_required
def delete_program_subcontent(id):
    subcontent = ProgramSubContent.query.get_or_404(id)
    redirect_url = url_for('admin.edit_program', id=subcontent.program_id)
        
    db.session.delete(subcontent)
    db.session.commit()
    flash('Subcontent deleted.', 'success')
    return redirect(redirect_url)



@admin_bp.route('/partnerships')
@login_required
def list_partnerships():
    partnerships = Partnership.query.all()
    return render_template('admin/partnerships_list.html', partnerships=partnerships)

@admin_bp.route('/partnerships/new', methods=['GET', 'POST'])
@login_required
def create_partnership():
    form = PartnershipForm()
    if form.validate_on_submit():
        partner = Partnership()
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='partners')
            partner.image_filename = picture_file
        form.populate_obj(partner)
        db.session.add(partner)
        db.session.commit()
        flash('Partnership created.', 'success')
        return redirect(url_for('admin.list_partnerships'))
    return render_template('admin/partnership_edit.html', form=form, legend="Create Partnership")

@admin_bp.route('/partnerships/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_partnership(id):
    partner = Partnership.query.get_or_404(id)
    form = PartnershipForm(obj=partner)
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='partners')
            partner.image_filename = picture_file
        form.populate_obj(partner)
        db.session.commit()
        flash('Partnership updated.', 'success')
        return redirect(url_for('admin.list_partnerships'))
    
    tiers = partner.tiers.order_by(SponsorshipTier.order.asc()).all()
    return render_template('admin/partnership_edit.html', form=form, partner=partner, tiers=tiers, legend="Edit Partnership")

@admin_bp.route('/partnerships/<int:partnership_id>/tiers/new', methods=['GET', 'POST'])
@login_required
def create_tier(partnership_id):
    partner = Partnership.query.get_or_404(partnership_id)
    form = SponsorshipTierForm()
    if form.validate_on_submit():
        tier = SponsorshipTier(partnership_id=partner.id)
        form.populate_obj(tier)
        db.session.add(tier)
        db.session.commit()
        flash('Sponsorship tier added.', 'success')
        return redirect(url_for('admin.edit_partnership', id=partner.id))
    return render_template('admin/tier_edit.html', form=form, partner=partner, legend=f"Add Tier to {partner.title}")

@admin_bp.route('/tiers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tier(id):
    tier = SponsorshipTier.query.get_or_404(id)
    partner = tier.partnership
    form = SponsorshipTierForm(obj=tier)
    if form.validate_on_submit():
        form.populate_obj(tier)
        db.session.commit()
        flash('Sponsorship tier updated.', 'success')
        return redirect(url_for('admin.edit_partnership', id=partner.id))
    return render_template('admin/tier_edit.html', form=form, partner=partner, legend="Edit Sponsorship Tier")

@admin_bp.route('/tiers/<int:id>/delete', methods=['POST'])
@login_required
def delete_tier(id):
    tier = SponsorshipTier.query.get_or_404(id)
    partnership_id = tier.partnership_id
    db.session.delete(tier)
    db.session.commit()
    flash('Sponsorship tier removed.', 'success')
    return redirect(url_for('admin.edit_partnership', id=partnership_id))

@admin_bp.route('/partnerships/<int:id>/delete', methods=['POST'])
@login_required
def delete_partnership(id):
    partner = Partnership.query.get_or_404(id)
    db.session.delete(partner)
    db.session.commit()
    flash('Partnership deleted.', 'success')
    return redirect(url_for('admin.list_partnerships'))

@admin_bp.route('/team')
@login_required
def list_team():
    team = TeamMember.query.order_by(TeamMember.order).all()
    return render_template('admin/team_list.html', team=team)

@admin_bp.route('/team/new', methods=['GET', 'POST'])
@login_required
def create_team():
    form = TeamMemberForm()
    if form.validate_on_submit():
        member = TeamMember()
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='team')
            member.image_filename = picture_file
        form.populate_obj(member)
        db.session.add(member)
        db.session.commit()
        flash('Team Member added.', 'success')
        return redirect(url_for('admin.list_team'))
    return render_template('admin/team_edit.html', form=form, legend="Add Team Member")

@admin_bp.route('/team/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    member = TeamMember.query.get_or_404(id)
    form = TeamMemberForm(obj=member)
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='team')
            member.image_filename = picture_file
        form.populate_obj(member)
        db.session.commit()
        flash('Team Member updated.', 'success')
        return redirect(url_for('admin.list_team'))
    return render_template('admin/team_edit.html', form=form, member=member, legend="Edit Team Member")

@admin_bp.route('/team/<int:id>/delete', methods=['POST'])
@login_required
def delete_team(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Team Member deleted.', 'success')
    return redirect(url_for('admin.list_team'))

@admin_bp.route('/news')
@login_required
def list_news():
    news = NewsArticle.query.order_by(NewsArticle.date_published.desc()).all()
    return render_template('admin/news_list.html', news=news)

@admin_bp.route('/news/new', methods=['GET', 'POST'])
@login_required
def create_news():
    form = NewsArticleForm()
    if form.validate_on_submit():
        article = NewsArticle()
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='news')
            article.image_filename = picture_file
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        flash('News Article created.', 'success')
        return redirect(url_for('admin.list_news'))
    return render_template('admin/news_edit.html', form=form, legend="Create Article")

@admin_bp.route('/news/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    article = NewsArticle.query.get_or_404(id)
    form = NewsArticleForm(obj=article)
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='news')
            article.image_filename = picture_file
        form.populate_obj(article)
        db.session.commit()
        flash('News Article updated.', 'success')
        return redirect(url_for('admin.list_news'))
    return render_template('admin/news_edit.html', form=form, article=article, legend="Edit Article")

@admin_bp.route('/news/<int:id>/delete', methods=['POST'])
@login_required
def delete_news(id):
    article = NewsArticle.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('Article deleted.', 'success')
    return redirect(url_for('admin.list_news'))

@admin_bp.route('/testimonials')
@login_required
def list_testimonials():
    testimonials = Testimonial.query.all()
    return render_template('admin/testimonials_list.html', testimonials=testimonials)

@admin_bp.route('/testimonials/new', methods=['GET', 'POST'])
@login_required
def create_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        t = Testimonial()
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='testimonials')
            t.image_filename = picture_file
        form.populate_obj(t)
        db.session.add(t)
        db.session.commit()
        flash('Testimonial created.', 'success')
        return redirect(url_for('admin.list_testimonials'))
    return render_template('admin/testimonial_edit.html', form=form, legend="Create Testimonial")

@admin_bp.route('/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    form = TestimonialForm(obj=t)
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='testimonials')
            t.image_filename = picture_file
        form.populate_obj(t)
        db.session.commit()
        flash('Testimonial updated.', 'success')
        return redirect(url_for('admin.list_testimonials'))
    return render_template('admin/testimonial_edit.html', form=form, testimonial=t, legend="Edit Testimonial")

@admin_bp.route('/testimonials/<int:id>/delete', methods=['POST'])
@login_required
def delete_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    flash('Testimonial deleted.', 'success')
    return redirect(url_for('admin.list_testimonials'))



@admin_bp.route('/contact')
@login_required
def list_contact():
    contact_info = ContactInfo.query.all()
    social_media = SocialMedia.query.all()
    return render_template('admin/contact_list.html', contact_info=contact_info, social_media=social_media)

@admin_bp.route('/contact/new', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = ContactInfoForm()
    if form.validate_on_submit():
        c = ContactInfo()
        form.populate_obj(c)
        db.session.add(c)
        db.session.commit()
        flash('Contact Info added.', 'success')
        return redirect(url_for('admin.list_contact'))
    return render_template('admin/contact_edit.html', form=form, legend="Add Contact Info")

@admin_bp.route('/contact/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    c = ContactInfo.query.get_or_404(id)
    form = ContactInfoForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.commit()
        flash('Contact Info updated.', 'success')
        return redirect(url_for('admin.list_contact'))
    return render_template('admin/contact_edit.html', form=form, legend="Edit Contact Info")

@admin_bp.route('/contact/<int:id>/delete', methods=['POST'])
@login_required
def delete_contact(id):
    c = ContactInfo.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Contact Info deleted.', 'success')
    return redirect(url_for('admin.list_contact'))

# Social Media Routes
@admin_bp.route('/social/new', methods=['GET', 'POST'])
@login_required
def create_social():
    form = SocialMediaForm()
    if form.validate_on_submit():
        s = SocialMedia()
        form.populate_obj(s)
        db.session.add(s)
        db.session.commit()
        flash('Social Link added.', 'success')
        return redirect(url_for('admin.list_contact'))
    return render_template('admin/social_edit.html', form=form, legend="Add Social Link")

@admin_bp.route('/social/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_social(id):
    s = SocialMedia.query.get_or_404(id)
    form = SocialMediaForm(obj=s)
    if form.validate_on_submit():
        form.populate_obj(s)
        db.session.commit()
        flash('Social Link updated.', 'success')
        return redirect(url_for('admin.list_contact'))
    return render_template('admin/social_edit.html', form=form, legend="Edit Social Link")

@admin_bp.route('/social/<int:id>/delete', methods=['POST'])
@login_required
def delete_social(id):
    s = SocialMedia.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Social Link deleted.', 'success')
    return redirect(url_for('admin.list_contact'))

# Site Settings Route
@admin_bp.route('/site-settings', methods=['GET', 'POST'])
@login_required
def edit_site_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    
    form = SiteSettingsForm(obj=settings)
    if form.validate_on_submit():
        form.populate_obj(settings)
        db.session.commit()
        flash('Site settings updated.', 'success')
        return redirect(url_for('admin.edit_site_settings'))
    return render_template('admin/site_settings.html', form=form, legend="General Site Settings")

# Sponsor Ticker Routes
@admin_bp.route('/sponsors')
@login_required
def list_sponsors():
    sponsors = Sponsor.query.order_by(Sponsor.order).all()
    return render_template('admin/sponsors_list.html', sponsors=sponsors)

@admin_bp.route('/sponsors/new', methods=['GET', 'POST'])
@login_required
def create_sponsor():
    form = SponsorForm()
    if form.validate_on_submit():
        sponsor = Sponsor()
        if form.logo_file.data:
            picture_file = save_picture(form.logo_file.data, folder='sponsors')
            sponsor.logo_filename = picture_file
        form.populate_obj(sponsor)
        db.session.add(sponsor)
        db.session.commit()
        flash('Sponsor added.', 'success')
        return redirect(url_for('admin.list_sponsors'))
    return render_template('admin/sponsor_edit.html', form=form, legend="Add New Sponsor")

@admin_bp.route('/sponsors/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_sponsor(id):
    sponsor = Sponsor.query.get_or_404(id)
    form = SponsorForm(obj=sponsor)
    if form.validate_on_submit():
        if form.logo_file.data:
            picture_file = save_picture(form.logo_file.data, folder='sponsors')
            sponsor.logo_filename = picture_file
        form.populate_obj(sponsor)
        db.session.commit()
        flash('Sponsor updated.', 'success')
        return redirect(url_for('admin.list_sponsors'))
    return render_template('admin/sponsor_edit.html', form=form, sponsor=sponsor, legend="Edit Sponsor")

@admin_bp.route('/sponsors/<int:id>/delete', methods=['POST'])
@login_required
def delete_sponsor(id):
    sponsor = Sponsor.query.get_or_404(id)
    db.session.delete(sponsor)
    db.session.commit()
    flash('Sponsor removed.', 'success')
    return redirect(url_for('admin.list_sponsors'))

# --- GALLERY ---
@admin_bp.route('/gallery')
@login_required
def list_gallery():
    items = GalleryItem.query.order_by(GalleryItem.order.asc(), GalleryItem.created_at.desc()).all()
    return render_template('admin/gallery_list.html', items=items)

@admin_bp.route('/gallery/new', methods=['GET', 'POST'])
@login_required
def create_gallery_item():
    form = GalleryItemForm()
    if form.validate_on_submit():
        item = GalleryItem()
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='gallery')
            item.image_filename = picture_file
        
        # Handle program_id=0 as None
        p_id = form.program_id.data
        item.program_id = p_id if p_id > 0 else None
        
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Gallery item added successfully.', 'success')
        return redirect(url_for('admin.list_gallery'))
    return render_template('admin/gallery_edit.html', form=form, legend="Add Gallery Item")

@admin_bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    form = GalleryItemForm(obj=item)
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, folder='gallery')
            item.image_filename = picture_file
        
        p_id = form.program_id.data
        item.program_id = p_id if p_id > 0 else None
        
        form.populate_obj(item)
        db.session.commit()
        flash('Gallery item updated.', 'success')
        return redirect(url_for('admin.list_gallery'))
    
    # Pre-select program_id
    if item.program_id:
        form.program_id.data = item.program_id
    else:
        form.program_id.data = 0
        
    return render_template('admin/gallery_edit.html', form=form, item=item, legend="Edit Gallery Item")

@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
@login_required
def delete_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Gallery item deleted.', 'success')
    return redirect(url_for('admin.list_gallery'))

# --- INQUIRIES ---
@admin_bp.route('/inquiries')
@login_required
def list_inquiries():
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiry_list.html', inquiries=inquiries)

@admin_bp.route('/inquiries/<int:id>/status', methods=['POST'])
@login_required
def update_inquiry_status(id):
    inquiry = Inquiry.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['New', 'Replied', 'Closed']:
        inquiry.status = new_status
        db.session.commit()
        flash(f'Inquiry status updated to {new_status}.', 'success')
    return redirect(url_for('admin.list_inquiries'))

@admin_bp.route('/inquiries/<int:id>/delete', methods=['POST'])
@login_required
def delete_inquiry(id):
    inquiry = Inquiry.query.get_or_404(id)
    db.session.delete(inquiry)
    db.session.commit()
    flash('Inquiry deleted.', 'success')
    return redirect(url_for('admin.list_inquiries'))


from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
import time
from datetime import datetime
from app.models import Page, Section, Program, TeamMember, Partnership, NewsArticle, Testimonial, ImpactMetric, ContactInfo, InquiryType, SocialMedia, SiteSettings, Sponsor, ProgramSubContent, GalleryItem, Inquiry
from app import db

main = Blueprint('main', __name__)


@main.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        'social_media': SocialMedia.query.all(),
        'global_contact_info': ContactInfo.query.first(),
        'site_settings': SiteSettings.query.first(),
        'sponsors': Sponsor.query.order_by('order').all(),
        'ProgramSubContent': ProgramSubContent
    }


class _SectionMap(dict):
    """Dict that returns None for missing section keys instead of raising,
    so a page never crashes if an admin removes or renames a section."""

    def __missing__(self, key):
        return None


def get_page_data(slug):
    """Helper to fetch page and its sections."""
    page = Page.query.filter_by(slug=slug).first()
    sections = _SectionMap()
    if page:
        for section in page.sections:
            sections[section.section_key] = section
    return page, sections


@main.route('/')
def index():
    page, sections = get_page_data('home')
    # Fetch programs marked as featured for the highlights section
    programs = Program.query.filter_by(
        is_featured=True).order_by(
        Program.order.asc()).all()
    return render_template(
        'index.html',
        page=page,
        sections=sections,
        programs=programs)


@main.route('/about')
def about():
    page, sections = get_page_data('about')
    team_members = TeamMember.query.all()
    return render_template(
        'about.html',
        page=page,
        sections=sections,
        team_members=team_members)


@main.route('/programs')
def programs():
    page, sections = get_page_data('programs')
    # Simple list of all Programs for the listing page
    programs = Program.query.order_by(Program.order.asc()).all()
    return render_template(
        'programs.html',
        page=page,
        sections=sections,
        programs=programs)


@main.route('/programs/<slug>')
@main.route('/program/<slug>')
def program_detail(slug):
    program = Program.query.filter_by(slug=slug).first_or_404()
    related_programs = Program.query.filter(
        Program.type == program.type,
        Program.id != program.id
    ).limit(3).all()
    # Fetch gallery items linked to this program
    gallery_items = program.gallery_items.order_by(
        GalleryItem.order.asc()).all()
    return render_template(
        'program_detail.html',
        program=program,
        related_programs=related_programs,
        gallery_items=gallery_items)


@main.route('/digital')
def digital():
    page, sections = get_page_data('digital')
    return render_template('digital.html', page=page, sections=sections)


@main.route('/partnerships')
def partnerships():
    page, sections = get_page_data('partnerships')
    partnerships = Partnership.query.all()
    return render_template(
        'partnerships.html',
        page=page,
        sections=sections,
        partnerships=partnerships)


@main.route('/join')
def join():
    page, sections = get_page_data('join')
    # "Join Categories" are currently static in template or could be Sections
    return render_template('join.html', page=page, sections=sections)


@main.route('/gallery')
def gallery():
    page, sections = get_page_data('gallery')  # Optional page data
    gallery_items = GalleryItem.query.order_by(GalleryItem.order.asc()).all()
    gallery_programs = Program.query.join(GalleryItem).distinct().all()
    return render_template(
        'gallery.html',
        page=page,
        sections=sections,
        gallery_items=gallery_items,
        gallery_programs=gallery_programs)


@main.route('/news-impact')
def news_impact():
    page, sections = get_page_data('news-impact')
    page_num = request.args.get('page', 1, type=int)
    news_pagination = NewsArticle.query.order_by(
        NewsArticle.date_published.desc()).paginate(
        page=page_num, per_page=9, error_out=False)
    news_articles = news_pagination.items
    impact_metrics = ImpactMetric.query.all()
    testimonials = Testimonial.query.all()
    gallery_items = GalleryItem.query.order_by(
        GalleryItem.order.asc()).limit(6).all()
    # Get only programs that have gallery items for the filter
    gallery_programs = Program.query.join(GalleryItem).distinct().all()
    return render_template(
        'news-impact.html',
        page=page,
        sections=sections,
        news_articles=news_articles,
        news_pagination=news_pagination,
        impact_metrics=impact_metrics,
        testimonials=testimonials,
        gallery_items=gallery_items,
        gallery_programs=gallery_programs)


@main.route('/news-impact/<int:article_id>')
def news_detail(article_id):
    article = NewsArticle.query.get_or_404(article_id)
    # Get 3 recent articles excluding current one for sidebar/related
    recent_articles = NewsArticle.query.filter(
        NewsArticle.id != article.id).order_by(
        NewsArticle.date_published.desc()).limit(3).all()

    # Get unique categories and counts for sidebar
    categories_data = db.session.query(
        NewsArticle.category, db.func.count(
            NewsArticle.id)).group_by(
        NewsArticle.category).all()
    categories = [{'name': cat, 'count': count}
                  for cat, count in categories_data if cat]

    return render_template(
        'news_detail.html',
        article=article,
        recent_articles=recent_articles,
        categories=categories)


@main.route('/contact', methods=['GET', 'POST'], strict_slashes=False)
def contact():
    page, sections = get_page_data('contact')
    contact_info = ContactInfo.query.first()
    inquiry_types = InquiryType.query.all()

    # Handle pre-selection from URL
    selected_type_id = request.args.get('type_id', type=int)
    # Also support slug-like value if id is unknown
    selected_type_val = request.args.get('type')
    selected_program = request.args.get('program')

    if request.method == 'POST':
        # Spam Protection: Honeypot check
        if request.form.get('website_field'):
            # Silent fail for bots
            return redirect(url_for('main.contact', _anchor='contact-status'))

        # Spam Protection: Timestamp check (prevent too-fast submissions)
        try:
            form_time = int(request.form.get('form_timestamp', 0))
            current_time = int(time.time() * 1000)
            # If submitted in less than 3 seconds, likely a bot
            if current_time - form_time < 3000:
                flash(
                    "Submission too fast. Please wait a moment and try again.",
                    "warning")
                return redirect(
                    url_for(
                        'main.contact',
                        _anchor='contact-status'))
        except (ValueError, TypeError):
            pass

        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        organization = request.form.get('organization')
        inquiry_type_id = request.form.get('inquiry_type')
        message = request.form.get('message')

        new_inquiry = Inquiry(
            name=name,
            email=email,
            phone=phone,
            organization=organization,
            inquiry_type_id=inquiry_type_id if inquiry_type_id and inquiry_type_id.isdigit() else None,
            message=message)

        try:
            db.session.add(new_inquiry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(
                "An error occurred while saving your inquiry. Please try again.",
                "danger")
            return redirect(url_for('main.contact', _anchor='contact-status'))

        # Get type name for flashy message
        type_obj = InquiryType.query.get(
            inquiry_type_id) if inquiry_type_id and inquiry_type_id.isdigit() else None
        subject = type_obj.name if type_obj else "General Inquiry"

        flash(
            f'Thank you, {name}! Your inquiry about "{subject}" has been received.',
            'success')
        return redirect(url_for('main.contact', _anchor='contact-status'))

    return render_template(
        'contact.html',
        page=page,
        sections=sections,
        contact_info=contact_info,
        inquiry_types=inquiry_types,
        selected_type_id=selected_type_id,
        selected_type_val=selected_type_val,
        selected_program=selected_program)


@main.route('/robots.txt')
def robots():
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        f'Sitemap: {url_for("main.sitemap", _external=True)}',
    ]
    return Response('\n'.join(lines), mimetype='text/plain')


@main.route('/sitemap.xml')
def sitemap():
    """Generate a sitemap of all public, indexable pages."""
    static_endpoints = [
        'main.index', 'main.about', 'main.programs', 'main.digital',
        'main.partnerships', 'main.join', 'main.gallery',
        'main.news_impact', 'main.contact',
    ]
    urls = []
    today = datetime.utcnow().strftime('%Y-%m-%d')
    for endpoint in static_endpoints:
        urls.append({'loc': url_for(endpoint, _external=True),
                     'lastmod': today, 'priority': '0.8'})

    for program in Program.query.all():
        urls.append({
            'loc': url_for('main.program_detail', slug=program.slug,
                           _external=True),
            'lastmod': today, 'priority': '0.6'})

    for article in NewsArticle.query.all():
        lastmod = (article.date_published.strftime('%Y-%m-%d')
                   if article.date_published else today)
        urls.append({
            'loc': url_for('main.news_detail', article_id=article.id,
                           _external=True),
            'lastmod': lastmod, 'priority': '0.5'})

    xml = render_template('sitemap.xml', urls=urls)
    return Response(xml, mimetype='application/xml')

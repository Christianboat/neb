from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    hero_title = db.Column(db.String(255))
    hero_subtitle = db.Column(db.String(255))
    hero_description = db.Column(db.Text)
    meta_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    is_coming_soon = db.Column(db.Boolean, default=False)
    sections = db.relationship('Section', backref='page', lazy='dynamic')


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    section_key = db.Column(db.String(64), nullable=False)  # e.g. "who_we_are"
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    image_filename = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    excerpt = db.Column(db.String(250))
    description = db.Column(db.Text)
    # competitions, training, recognition, awards, trade_fairs, custom
    type = db.Column(db.String(64))
    # youth_competitions, professional_dev, etc. (deprecated but kept for
    # compat)
    category = db.Column(db.String(64))
    icon = db.Column(db.String(64))
    image_filename = db.Column(db.String(255))
    cta_url = db.Column(db.String(255))
    cta_text = db.Column(db.String(64), default="Learn More")
    is_featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)

    # Relationships
    gallery_items = db.relationship(
        'GalleryItem',
        backref='program',
        lazy='dynamic',
        cascade='all, delete-orphan')

    @property
    def detail_url(self):
        from flask import url_for
        return url_for('main.program_detail', slug=self.slug)


class ProgramSubContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(
        db.Integer,
        db.ForeignKey('program.id'),
        nullable=True)
    title = db.Column(db.String(255))
    # For storing lists (newline separated) or descriptions
    content = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

    # Relationships
    program = db.relationship(
        'Program',
        backref=db.backref(
            'subcontents',
            lazy='dynamic',
            cascade='all, delete-orphan'))


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128))
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    image_filename = db.Column(db.String(255))  # Local upload
    order = db.Column(db.Integer, default=0)


class Partnership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))  # schools, corporate, etc.
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    benefits = db.Column(db.Text)  # JSON or list
    logo_url = db.Column(db.String(255))
    image_filename = db.Column(db.String(255))  # Looking for this first
    order = db.Column(db.Integer, default=0)
    tiers = db.relationship(
        'SponsorshipTier',
        backref='partnership',
        lazy='dynamic')

    @property
    def benefits_list(self):
        """Returns benefits split by newline."""
        if self.benefits:
            return [
                b.strip() for b in self.benefits.replace(
                    '\r\n', '\n').split('\n') if b.strip()]
        return []


class SponsorshipTier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partnership_id = db.Column(
        db.Integer,
        db.ForeignKey('partnership.id'),
        nullable=False)
    tier_name = db.Column(db.String(128))
    benefits = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)


class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(64))
    date_published = db.Column(db.Date, default=datetime.utcnow)
    featured_image_url = db.Column(db.String(255))
    image_filename = db.Column(db.String(255))
    excerpt = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(128))
    author_role = db.Column(db.String(128))
    author_photo_url = db.Column(db.String(255))
    image_filename = db.Column(db.String(255))
    content = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)


class ImpactMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(128))
    value = db.Column(db.String(64))
    icon = db.Column(db.String(64))  # FontAwesome class
    order = db.Column(db.Integer, default=0)


class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info_type = db.Column(db.String(64))  # headquarters, regional, etc.
    location_department = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    address = db.Column(db.Text)
    hours = db.Column(db.String(128))


class InquiryType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    value = db.Column(db.String(128))
    order = db.Column(db.Integer, default=0)


class SocialMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(64))
    url = db.Column(db.String(255))

    @property
    def icon_class(self):
        icons = {
            'LinkedIn': 'fab fa-linkedin-in',
            'Facebook': 'fab fa-facebook-f',
            'Instagram': 'fab fa-instagram',
            'YouTube': 'fab fa-youtube',
            'Twitter': 'fab fa-twitter',
            'X': 'fab fa-twitter'
        }
        return icons.get(self.platform, 'fas fa-link')


class ContentItem(db.Model):
    """Generic item for lists within a section (e.g. cards, slides)."""
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(
        db.Integer,
        db.ForeignKey('section.id'),
        nullable=False)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text)
    image_filename = db.Column(db.String(255))  # Local upload
    icon = db.Column(db.String(64))  # FontAwesome class or similar
    link_url = db.Column(db.String(255))
    link_text = db.Column(db.String(64))
    order = db.Column(db.Integer, default=0)

    # Relationship to Section
    section = db.relationship(
        'Section', backref=db.backref(
            'items', lazy='dynamic'))


class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(128), default='NEBULA')
    footer_description = db.Column(db.Text)
    copyright_text = db.Column(
        db.String(255),
        default='&copy; 2025 Nebula Cybernetics Academy. All Rights Reserved.')


class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    logo_filename = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)


class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    image_filename = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    # e.g. Competition, Event, Random
    category = db.Column(db.String(64), default='General')
    program_id = db.Column(
        db.Integer,
        db.ForeignKey('program.id'),
        nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(64))
    organization = db.Column(db.String(255))
    inquiry_type_id = db.Column(
        db.Integer,
        db.ForeignKey('inquiry_type.id'),
        nullable=True)
    message = db.Column(db.Text)
    status = db.Column(db.String(64), default='New')  # New, Replied, Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    inquiry_type = db.relationship(
        'InquiryType', backref=db.backref(
            'inquiries', lazy='dynamic'))

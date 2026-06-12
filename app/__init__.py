from flask import Flask, render_template
import os
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)


def create_app(config_name=None):
    app = Flask(__name__)

    # Resolve configuration: allow passing a name, a Config class, or fall
    # back to the FLASK_CONFIG env var (default: development).
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    if isinstance(config_name, str):
        config_obj = config[config_name]
    else:
        config_obj = config_name  # a Config class was passed directly
    app.config.from_object(config_obj)
    if hasattr(config_obj, 'init_app'):
        config_obj.init_app(app)

    # Ensure upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    from app.routes import main
    from app.admin_routes import admin_bp

    app.register_blueprint(main)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.utils import get_video_embed_url
    app.jinja_env.filters['youtube_embed'] = get_video_embed_url

    from flask import url_for

    @app.template_global()
    def asset_url(filename):
        """url_for('static', ...) with a cache-busting version based on the
        file's last-modified time, so browsers always fetch fresh CSS/JS."""
        try:
            mtime = int(os.path.getmtime(
                os.path.join(app.static_folder, filename)))
        except OSError:
            mtime = 0
        return url_for('static', filename=filename, v=mtime)

    register_error_handlers(app)
    register_security_headers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(413)
    def too_large(error):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500


def register_security_headers(app):
    @app.after_request
    def set_secure_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=()'
        )
        # Content Security Policy. Allows the external CDNs the site relies on
        # (Font Awesome, Google Fonts, Bootstrap, YouTube/Drive embeds) while
        # blocking arbitrary inline script injection vectors.
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com "
            "https://fonts.googleapis.com https://cdn.jsdelivr.net "
            "https://cdn.datatables.net; "
            "font-src 'self' https://fonts.gstatic.com "
            "https://cdnjs.cloudflare.com; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net "
            "https://code.jquery.com https://cdn.datatables.net; "
            "frame-src https://www.youtube.com https://drive.google.com; "
            "object-src 'none'; base-uri 'self'; frame-ancestors 'self'"
        )
        if app.config.get('SESSION_COOKIE_SECURE'):
            response.headers['Strict-Transport-Security'] = (
                'max-age=31536000; includeSubDomains'
            )
        return response

import os
import secrets
from PIL import Image
from flask import current_app, url_for
import re


def slugify(s):
    """
    Converts a string to a URL-safe slug.
    """
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s


class InvalidImageError(Exception):
    """Raised when an uploaded file is not a valid, safe image."""


# Pillow format -> (extension, save kwargs). Re-encoding strips any embedded
# scripts/metadata and guarantees the stored file is a real image.
_SAFE_FORMATS = {
    'JPEG': ('.jpg', {'quality': 85, 'optimize': True}),
    'PNG': ('.png', {'optimize': True}),
    'WEBP': ('.webp', {'quality': 85}),
    'GIF': ('.gif', {}),
}

# Largest dimension we keep; bigger images are downscaled to save bandwidth.
_MAX_DIMENSION = 2000


def save_picture(form_picture, folder=''):
    """
    Validate, re-encode and save an uploaded image to static/uploads/<folder>.

    The image is opened and re-saved with Pillow, which both verifies it is a
    genuine image (not a renamed script) and strips any embedded payloads or
    EXIF data. Returns the stored filename, or raises InvalidImageError.
    """
    try:
        image = Image.open(form_picture.stream)
        image.verify()  # detect truncated / corrupt / non-image files
    except Exception:
        raise InvalidImageError('The uploaded file is not a valid image.')

    # verify() leaves the image unusable; reopen for actual processing.
    form_picture.stream.seek(0)
    image = Image.open(form_picture.stream)

    fmt = (image.format or '').upper()
    if fmt not in _SAFE_FORMATS:
        raise InvalidImageError('Unsupported image format.')

    f_ext, save_kwargs = _SAFE_FORMATS[fmt]
    picture_fn = secrets.token_hex(8) + f_ext

    upload_path = os.path.join(
        current_app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_path, exist_ok=True)
    picture_path = os.path.join(upload_path, picture_fn)

    # Downscale very large images (keeps animation frames for GIF intact via
    # the save loop Pillow handles internally for the first frame only, so we
    # skip resizing animated GIFs).
    is_animated = getattr(image, 'is_animated', False)
    if not is_animated and max(image.size) > _MAX_DIMENSION:
        image.thumbnail((_MAX_DIMENSION, _MAX_DIMENSION))

    # Flatten transparency for JPEG which has no alpha channel.
    if fmt == 'JPEG' and image.mode in ('RGBA', 'P', 'LA'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        rgba = image.convert('RGBA')
        background.paste(rgba, mask=rgba.split()[-1])
        image = background

    if is_animated:
        image.save(picture_path, save_all=True)
    else:
        image.save(picture_path, **save_kwargs)

    return picture_fn


def get_image_url(filename, folder=''):
    """Returns the URL for the image."""
    if not filename:
        return None

    path = f'uploads/{folder}/{filename}' if folder else f'uploads/{filename}'
    return url_for('static', filename=path)


def get_video_embed_url(url):
    """
    Extracts the video ID from a URL and returns the embed URL.
    Supports:
    - YouTube: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID, youtube.com/shorts/ID
    - Google Drive: drive.google.com/file/d/ID/view, drive.google.com/open?id=ID
    """
    if not url:
        return None

    # Check if it's a Google Drive URL
    if 'drive.google.com' in url:
        # Extract file ID from various Google Drive URL formats
        drive_regex = r'drive\.google\.com\/(?:file\/d\/|open\?id=)([-a-zA-Z0-9_]+)'
        match = re.search(drive_regex, url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"

    # Check if it's a YouTube URL
    if 'youtube.com' in url or 'youtu.be' in url:
        # Regex to catch video ID from various YouTube URL formats
        youtube_regex = r'(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})'
        match = re.search(youtube_regex, url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"

    return url  # Return original if no match (fallback)

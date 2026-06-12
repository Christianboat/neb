import os
from app import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    # Debug is controlled by the selected config (DevelopmentConfig only).
    app.run(debug=app.config.get('DEBUG', False))

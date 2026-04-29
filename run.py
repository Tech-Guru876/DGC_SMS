import os
from dotenv import load_dotenv

# Load .env before any config or app code reads os.environ, so SECRET_KEY
# and other settings are always available even when started outside systemd.
load_dotenv()

from app import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

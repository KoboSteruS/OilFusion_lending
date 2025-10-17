"""
Root-level app entrypoint for platforms that expect 'gunicorn app:app'.
Creates the Flask app via the factory in app/__init__.py.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)



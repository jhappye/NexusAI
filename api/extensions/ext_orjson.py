from flask_orjson import OrjsonProvider

from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    """Initialize Flask-Orjson extension for faster JSON serialization"""
    app.json = OrjsonProvider(app)

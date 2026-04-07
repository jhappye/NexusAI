from configs import nexusai_config
from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    app.secret_key = nexusai_config.SECRET_KEY

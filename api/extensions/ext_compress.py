from configs import nexusai_config
from nexusai_app import NexusAIApp


def is_enabled() -> bool:
    return nexusai_config.API_COMPRESSION_ENABLED


def init_app(app: NexusAIApp):
    from flask_compress import Compress

    compress = Compress()
    compress.init_app(app)

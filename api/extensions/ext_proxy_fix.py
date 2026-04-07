from configs import nexusai_config
from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    if nexusai_config.RESPECT_XFORWARD_HEADERS_ENABLED:
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_port=1)  # type: ignore[method-assign]

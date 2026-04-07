from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    from events import event_handlers  # noqa: F401 # pyright: ignore[reportUnusedImport]

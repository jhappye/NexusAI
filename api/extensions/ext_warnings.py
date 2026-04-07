from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    import warnings

    warnings.simplefilter("ignore", ResourceWarning)

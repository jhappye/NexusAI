from core.extension.extension import Extension
from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    code_based_extension.init()


code_based_extension = Extension()

from core.hosting_configuration import HostingConfiguration

hosting_configuration = HostingConfiguration()


from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    hosting_configuration.init_app(app)

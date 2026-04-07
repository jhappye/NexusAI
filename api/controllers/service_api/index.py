from flask_restx import Resource

from configs import nexusai_config
from controllers.service_api import service_api_ns


@service_api_ns.route("/")
class IndexApi(Resource):
    def get(self):
        return {
            "welcome": "NexusAI OpenAPI",
            "api_version": "v1",
            "server_version": nexusai_config.project.version,
        }

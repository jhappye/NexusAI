import os
import time

from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    os.environ["TZ"] = "UTC"
    # windows platform not support tzset
    if hasattr(time, "tzset"):
        time.tzset()

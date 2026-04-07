from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Flask

if TYPE_CHECKING:
    from extensions.ext_login import NexusAILoginManager


class NexusAIApp(Flask):
    """Flask application type with NexusAI-specific extension attributes."""

    login_manager: NexusAILoginManager

from nexusai_app import NexusAIApp


def init_app(app: NexusAIApp):
    import flask_migrate

    from extensions.ext_database import db

    flask_migrate.Migrate(app, db)

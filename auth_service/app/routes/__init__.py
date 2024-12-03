from app.routes.auth import auth_routes


def register_blueprints(app):

    # registro blueprint con l'applicazione Flask
    app.register_blueprint(auth_routes, url_prefix='/auth')

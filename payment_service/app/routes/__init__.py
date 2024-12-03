from app.routes.payment import payment_routes


def register_blueprints(app):

    # registro blueprint con l'applicazione Flask
    app.register_blueprint(payment_routes, url_prefix='/payment')
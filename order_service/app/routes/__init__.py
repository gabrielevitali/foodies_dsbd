from app.routes.order import order_routes


def register_blueprints(app):

    # registro blueprint con l'applicazione Flask
    app.register_blueprint(order_routes, url_prefix='/order')